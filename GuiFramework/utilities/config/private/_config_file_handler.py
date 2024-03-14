# GuiFramework/utilities/config/private/_config_file_handler.py
# ATTENTION: This module is for internal use only

import threading
import configparser

from configparser import ConfigParser
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Union

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import StaticLoggerMixin
from GuiFramework.utilities.file_ops import FileOps


@dataclass
class ConfigFileHandlerConfig:
    """Holds configuration for the ConfigFileHandler."""
    config_path: str = "config"
    default_config_name: str = "default-config.ini"
    custom_config_name: str = "custom-config.ini"
    default_config_creator_func: Optional[Callable[[], Dict]] = None

    @property
    def default_config_path(self) -> str:
        """Returns the full path to the default configuration file."""
        return FileOps.join_paths(self.config_path, self.default_config_name)

    @property
    def custom_config_path(self) -> str:
        """Returns the full path to the custom configuration file."""
        return FileOps.join_paths(self.config_path, self.custom_config_name)

    def __post_init__(self):
        """Validates the configuration after initialization."""
        self._validate_config_path()
        self._validate_config_names()
        self._validate_default_config_creator_func()

    def _validate_config_path(self):
        """Checks if the configuration path exists, creates it if not."""
        if not FileOps.directory_exists(self.config_path):
            FileOps.create_directory(self.config_path)

    def _validate_config_names(self):
        """Checks if the configuration file names are valid."""
        if not self.default_config_name.endswith(".ini"):
            raise ValueError(f"Invalid default_config_name: {self.default_config_name}")
        if not self.custom_config_name.endswith(".ini"):
            raise ValueError(f"Invalid custom_config_name: {self.custom_config_name}")
        if self.default_config_name == self.custom_config_name:
            raise ValueError("default_config_name and custom_config_name cannot be the same")

    def _validate_default_config_creator_func(self):
        """Checks if the default configuration creator function is valid."""
        if self.default_config_creator_func is not None:
            if not callable(self.default_config_creator_func):
                raise ValueError("default_config_creator_func must be callable")
            try:
                result = self.default_config_creator_func()
                if not isinstance(result, dict):
                    raise ValueError("default_config_creator_func must return a dictionary")
            except Exception as e:
                raise ValueError(f"default_config_creator_func execution error: {e}")


@dataclass
class ConfigData:
    """Holds configuration data."""
    default_config: ConfigParser = field(default_factory=ConfigParser)
    custom_config: ConfigParser = field(default_factory=ConfigParser)
    file_handler_config: ConfigFileHandlerConfig = field(default_factory=ConfigFileHandlerConfig)


class _ConfigFileHandler(StaticLoggerMixin):
    """Handles configuration files."""
    configs: Dict[str, ConfigData] = {}
    lock = threading.RLock()

    StaticLoggerMixin.set_logger_details(FRAMEWORK_NAME, "_ConfigFileHandler")

    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig):
        """Add a new configuration."""
        with cls.lock:
            if config_name in cls.configs:
                cls._log_warning("_add_config", f"Configuration \"{config_name}\" already exists.")
                return
            cls.configs[config_name] = ConfigData(file_handler_config=handler_config)
            cls._sync_config(config_name, 'default')
            cls._sync_config(config_name, 'custom')

    @classmethod
    def _sync_config(cls, config_name: str, config_type: str):
        """Synchronize a configuration."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_sync_config", f"Configuration \"{config_name}\" not found.")
                return
            try:
                attr_name = f'{config_type}_config'
                config = getattr(config_data, attr_name)
                config_path = getattr(config_data.file_handler_config, attr_name + '_path')
                config.read(config_path)
                if not config.sections() and config_data.file_handler_config.default_config_creator_func:
                    default_values = config_data.file_handler_config.default_config_creator_func()
                    for section, options in default_values.items():
                        if not config.has_section(section):
                            config.add_section(section)
                        for option, value in options.items():
                            config.set(section, option, value)
                    cls._save_config_to_file(config, config_path)
            except Exception as e:
                cls._log_error("_sync_config", f"Failed to synchronize {config_type} configuration for \"{config_name}\": {e}")

    @classmethod
    def _repopulate_config(cls, config: ConfigParser, values: Union[Dict[str, Dict[str, str]], ConfigParser]) -> None:
        """Repopulate a configuration with new values."""
        with cls.lock:
            config.clear()
            if isinstance(values, dict):
                for section, options in values.items():
                    if not config.has_section(section):
                        config.add_section(section)
                    for option, value in options.items():
                        config.set(section, option, value)
            elif isinstance(values, ConfigParser):
                for section in values.sections():
                    if not config.has_section(section):
                        config.add_section(section)
                    for option, value in values.items(section):
                        config.set(section, option, value)

    @classmethod
    def _save_config_to_file(cls, config: ConfigParser, config_path: str) -> None:
        """Save a configuration to a file."""
        with cls.lock:
            try:
                FileOps.ensure_directory_exists(config_path)
                with open(config_path, 'w', encoding='utf-8') as config_file:
                    config.write(config_file)
            except Exception as e:
                cls._log_error("_save_config_to_file", f"Failed to write config to {config_path}: {e}")

    @classmethod
    def _save_setting(cls, config_name: str, section: str, option: str, value: Any, auto_save: bool = True) -> None:
        """Save a specific setting to the configuration."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_save_setting", f"Config \"{config_name}\" is missing.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" is missing.")
            try:
                config_data.custom_config.setdefault(section, {})[option] = str(value)
                if auto_save:
                    cls._save_config_to_file(config_data.custom_config, config_data.file_handler_config.custom_config_path)
            except configparser.Error as e:
                cls._log_error("_save_setting", f"Failed to save setting {option} in section {section} for config {config_name}: {str(e)}")
                raise ValueError(f"Failed to save setting {option} in section {section} for config {config_name}: {str(e)}")

    @classmethod
    def _save_settings(cls, config_name: str, settings: Dict[str, Dict[str, Any]], auto_save: bool = True) -> None:
        """Save multiple settings to the configuration."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_save_settings", f"Config \"{config_name}\" is missing.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" is missing.")
            try:
                for section, options in settings.items():
                    if not config_data.custom_config.has_section(section):
                        config_data.custom_config.add_section(section)
                    for option, value in options.items():
                        config_data.custom_config.set(section, option, str(value))
                if auto_save:
                    cls._save_config_to_file(config_data.custom_config, config_data.file_handler_config.custom_config_path)
            except configparser.Error as e:
                cls._log_error("_save_settings", f"Failed to save settings for config {config_name}: {str(e)}")
                raise ValueError(f"Failed to save settings for config {config_name}: {str(e)}")

    @classmethod
    def _get_setting(cls, config_name: str, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False) -> Any:
        """Retrieve a specific setting from the configuration."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_get_setting", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            try:
                if not force_default:
                    value = config_data.custom_config.get(section, {}).get(option)
                    if value is not None:
                        return value
                value = config_data.default_config.get(section, {}).get(option)
                return value if value is not None else (fallback_value or "NoDefaultValue")
            except configparser.Error as e:
                cls._log_error("_get_setting", f"Failed to get setting {option} in section {section} for config {config_name}: {str(e)}")
                return fallback_value or "NoDefaultValue"

    @classmethod
    def _get_settings(cls, config_name: str, settings: Dict[str, Dict[str, Any]], force_default: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieve multiple settings from the configuration."""
        with cls.lock:
            result = {}
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_get_settings", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            try:
                for section, options in settings.items():
                    result.setdefault(section, {})
                    for option, fallback_value in options.items():
                        result[section][option] = cls._get_setting(config_name, section, option, fallback_value, force_default)
            except configparser.Error as e:
                cls._log_error("_get_settings", f"Failed to get settings for config {config_name}: {str(e)}")
            return result

    @classmethod
    def _get_config(cls, config_name: str) -> Dict[str, Dict[str, str]]:
        """Get the configuration data."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_get_config", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            return config_data.custom_config._sections

    @classmethod
    def _reset_setting(cls, config_name: str, section: str, option: str, auto_save: bool = True) -> None:
        """Reset a specific setting to its default value."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_reset_setting", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            try:
                default_value = config_data.default_config.get(section, {}).get(option, "NoDefaultValue")
                config_data.custom_config.setdefault(section, {})[option] = default_value
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls._log_error("_reset_setting", f"Failed to reset setting {option} in section {section} for config {config_name}: {str(e)}")
                raise ValueError(f"Failed to reset setting {option} in section {section} for config {config_name}: {str(e)}")

    @classmethod
    def _reset_section(cls, config_name: str, section: str, auto_save: bool = True) -> None:
        """Reset all settings in a section to their default values."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_reset_section", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            try:
                if section in config_data.default_config:
                    config_data.custom_config[section] = {k: v for k, v in config_data.default_config[section].items()}
                elif section in config_data.custom_config:
                    del config_data.custom_config[section]
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls._log_error("_reset_section", f"Failed to reset section {section} for config {config_name}: {str(e)}")
                raise ValueError(f"Failed to reset section {section} for config {config_name}: {str(e)}")

    @classmethod
    def _reset_config(cls, config_name: str, auto_save: bool = True) -> None:
        """Reset all settings to their default values."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_reset_config", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            try:
                config_data.custom_config = {section: dict(options) for section, options in config_data.default_config.items()}
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls._log_error("_reset_config", f"Failed to reset config {config_name}: {str(e)}")
                raise ValueError(f"Failed to reset config {config_name}: {str(e)}")

    @classmethod
    def _save_custom_config_to_file(cls, config_name: str) -> None:
        """Save the custom configuration to a file."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_save_custom_config_to_file", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            cls._save_config_to_file(config_data.custom_config, config_data.file_handler_config.custom_config_path)

    @classmethod
    def _load_custom_config_from_file(cls, config_name: str) -> None:
        """Load the custom configuration from a file."""
        with cls.lock:
            config_data = cls.configs.get(config_name)
            if not config_data:
                cls._log_error("_load_custom_config_from_file", f"Config \"{config_name}\" not found.")
                raise configparser.NoSectionError(f"Config \"{config_name}\" not found.")
            try:
                config_data.custom_config.read(config_data.file_handler_config.custom_config_path)
            except configparser.Error as e:
                cls._log_error("_load_custom_config_from_file", f"Failed to load config from {config_data.file_handler_config.custom_config_path}: {e}")
                raise ValueError(f"Failed to load config from {config_data.file_handler_config.custom_config_path}: {e}")
