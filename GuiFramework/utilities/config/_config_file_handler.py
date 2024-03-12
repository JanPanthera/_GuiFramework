# GuiFramework/utilities/config/_config_file_handler.py

import threading
import configparser

from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass, field

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import Logger
from GuiFramework.utilities.file_ops import FileOps


@dataclass
class ConfigFileHandlerConfig:
    """Configuration for the ConfigFileHandler."""
    config_path: str = "config"
    default_config_name: str = "default-config.ini"
    custom_config_name: str = "custom-config.ini"
    default_config_creator_func: Optional[Callable[[], Dict]] = None

    @property
    def default_config_path(self):
        """The full path to the default configuration file."""
        return FileOps.join_paths(self.config_path, self.default_config_name)

    @property
    def custom_config_path(self):
        """The full path to the custom configuration file."""
        return FileOps.join_paths(self.config_path, self.custom_config_name)

    def __post_init__(self):
        """Post-initialization validation."""
        if not FileOps.directory_exists(self.config_path):
            FileOps.create_directory(self.config_path)
        if not self.default_config_name.endswith(".ini"):
            raise ValueError(f"Invalid default_config_name: {self.default_config_name}")
        if not self.custom_config_name.endswith(".ini"):
            raise ValueError(f"Invalid custom_config_name: {self.custom_config_name}")
        if self.default_config_name == self.custom_config_name:
            raise ValueError(f"default_config_name and custom_config_name cannot be the same")
        if self.default_config_creator_func is not None and not callable(self.default_config_creator_func):
            raise ValueError(f"default_config_creator_func must be callable")
        if self.default_config_creator_func is not None and not isinstance(self.default_config_creator_func(), dict):
            raise ValueError(f"default_config_creator_func must return a dictionary")


@dataclass
class ConfigData:
    """Data class for configuration data."""
    default_config: configparser.ConfigParser = field(default_factory=configparser.ConfigParser, init=False)
    custom_config: configparser.ConfigParser = field(default_factory=configparser.ConfigParser, init=False)
    file_handler_config: ConfigFileHandlerConfig = field(default_factory=ConfigFileHandlerConfig)


class _ConfigFileHandler:
    """Private class for handling configuration files."""
    configs: Dict[str, ConfigData] = {}
    lock = threading.RLock()

    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig):
        """Add a new configuration to the handler."""
        with cls.lock:
            if config_name in cls.configs:
                cls._log_warning("_add_config", f"Config \"{config_name}\" already exists.")
                return
            cls.configs[config_name] = ConfigData(
                file_handler_config=handler_config
            )
            cls._sync_default_config(config_name)
            cls._sync_custom_config(config_name)

    @classmethod
    def _sync_default_config(cls, config_name: str):
        """Sync the default_config with the default_config_path file."""
        cls._sync_config(config_name, 'default')

    @classmethod
    def _sync_custom_config(cls, config_name: str):
        """Sync the custom_config with the custom_config_path file."""
        cls._sync_config(config_name, 'custom')

    @classmethod
    def _sync_config(cls, config_name: str, config_type: str):
        """Sync the config with the config_path file."""
        try:
            config_data = cls.configs[config_name]
            config = getattr(config_data, f'{config_type}_config')
            config_path = getattr(config_data.file_handler_config, f'{config_type}_config_path')
            config.read(config_path)
            if not config.sections() and config_data.file_handler_config.default_config_creator_func:
                default_values = config_data.file_handler_config.default_config_creator_func()
                cls._dic_to_config(config, default_values)
                cls._write_config_to_file(config, config_path)
        except Exception as e:
            cls._log_error("_sync_config", f"Failed to sync {config_type} config for \"{config_name}\": {e}")

    @classmethod
    def _dic_to_config(cls, config: configparser.ConfigParser, dic: Dict) -> None:
        """Convert a dictionary to a ConfigParser object."""
        config.clear()
        for section, options in dic.items():
            config[section] = options

    @classmethod
    def _write_config_to_file(cls, config_data, path):
        """Write a configuration to a file."""
        try:
            with open(path, 'w', encoding='utf-8') as config_file:
                config_data.write(config_file)
        except Exception as e:
            cls._log_error("_write_config_to_file", f"Failed to write config to {path}: {e}")
            # Critical error, so raise the exception
            raise e

    @classmethod
    def _save_setting(cls, config_name: str, section: str, option: str, value: Any) -> None:
        """Save a setting to the custom configuration file."""
        try:
            config_data = cls.configs.get(config_name)
            if config_data is None:
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            if not config_data.custom_config.has_section(section):
                config_data.custom_config.add_section(section)
            config_data.custom_config.set(section, option, value)
            cls._write_config_to_file(config_data.custom_config, config_data.file_handler_config.custom_config_path)
        except configparser.Error as e:
            cls._log_error("_save_setting", str(e))
            raise

    @ classmethod
    def _get_setting(cls, config_name: str, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False) -> Any:
        """Get a setting from the custom configuration file."""
        try:
            config_data = cls.configs.get(config_name)
            if config_data is None:
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            if force_default:
                return config_data.default_config.get(section, option)
            else:
                return config_data.custom_config.get(section, option, fallback=fallback_value)
        except configparser.Error as e:
            cls._log_error("_get_setting", str(e))
            raise

    @ classmethod
    def _reset_setting(cls, config_name: str, section: str, option: str) -> None:
        """Reset a setting to the default value."""
        try:
            config_data = cls.configs.get(config_name)
            if config_data is None:
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            default_value = config_data.default_config.get(section, option)
            config_data.custom_config.set(section, option, default_value)
            cls._write_config_to_file(config_data.custom_config, config_data.file_handler_config.custom_config_path)
        except configparser.Error as e:
            cls._log_error("_reset_setting", str(e))
            raise

    @ classmethod
    def _reset_section(cls, config_name: str, section: str) -> None:
        """Reset a section to the default settings."""
        try:
            config_data = cls.configs.get(config_name)
            if config_data is None:
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            default_settings = config_data.default_config[section]
            config_data.custom_config[section] = default_settings
            cls._write_config_to_file(config_data.custom_config, config_data.file_handler_config.custom_config_path)
        except configparser.Error as e:
            cls._log_error("_reset_section", str(e))
            raise

    @ classmethod
    def _reset_config(cls, config_name: str) -> None:
        """Reset the entire configuration to the default settings."""
        try:
            config_data = cls.configs.get(config_name)
            if config_data is None:
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            config_data.custom_config.clear()
            config_data.custom_config.read(config_data.file_handler_config.default_config_path, encoding="utf-8")
            cls._write_config_to_file(config_data.custom_config, config_data.file_handler_config.custom_config_path)
        except configparser.Error as e:
            cls._log_error("_reset_config", str(e))
            raise

    @ classmethod
    def _write_config_to_file(cls, config: configparser.ConfigParser, path: str) -> None:
        """Write a configuration to a file."""
        try:
            with cls.lock:
                with open(path, 'w', encoding='utf-8') as config_file:
                    config.write(config_file)
        except IOError as e:
            error_message = f"Failed to write configuration to path \"{path}\" due to IOError: {str(e)}"
            cls._log_error("_write_config_to_file", error_message)
            raise IOError(error_message) from e
        except configparser.Error as e:
            error_message = f"Failed to write configuration to path \"{path}\" due to configparser.Error: {str(e)}"
            cls._log_error("_write_config_to_file", error_message)
            raise configparser.Error(error_message) from e

    @ classmethod
    def _log_warning(cls, method_name: str, message: str) -> None:
        """Log a warning message."""
        full_message = f"Warning in method {method_name}: {message}"
        Logger.warning(full_message, logger_name=FRAMEWORK_NAME, module_name=_ConfigFileHandler.__name__)

    @ classmethod
    def _log_error(cls, method_name: str, message: str) -> None:
        """Log an error message."""
        full_message = f"Error in method {method_name}: {message}"
        Logger.error(full_message, logger_name=FRAMEWORK_NAME, module_name=_ConfigFileHandler.__name__)
