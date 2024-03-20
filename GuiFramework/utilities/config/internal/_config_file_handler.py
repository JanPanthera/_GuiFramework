# GuiFramework/utilities/config/internal/_config_file_handler.py
# ATTENTION: This module is for internal use only

import threading
import configparser

from configparser import ConfigParser
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import Logger
from GuiFramework.utilities.file_ops import FileOps

@dataclass
class ConfigFileHandlerConfig:
    """Configuration for the ConfigFileHandler."""
    config_path: str = "config"
    default_config_name: str = "default-config.ini"
    custom_config_name: str = "custom-config.ini"

    @property
    def default_config_path(self) -> str:
        """Returns path to the default configuration file."""
        return FileOps.join_paths(self.config_path, self.default_config_name)

    @property
    def custom_config_path(self) -> str:
        """Returns path to the custom configuration file."""
        return FileOps.join_paths(self.config_path, self.custom_config_name)

    def __post_init__(self) -> None:
        """Validates configuration after initialization."""
        self._validate_config_path()
        self._validate_config_names()

    def _validate_config_path(self) -> None:
        """Ensures configuration path exists, creates it if not."""
        if not FileOps.directory_exists(self.config_path):
            FileOps.create_directory(self.config_path)

    def _validate_config_names(self) -> None:
        """Ensures configuration file names are valid."""
        if not self.default_config_name.endswith(".ini"):
            raise ValueError(f"Invalid default_config_name: {self.default_config_name}")
        if not self.custom_config_name.endswith(".ini"):
            raise ValueError(f"Invalid custom_config_name: {self.custom_config_name}")
        if self.default_config_name == self.custom_config_name:
            raise ValueError("default_config_name and custom_config_name cannot be the same")


@dataclass
class ConfigData:
    """Holds configuration data."""
    file_handler_config: ConfigFileHandlerConfig = field(default_factory=ConfigFileHandlerConfig)
    default_config: Optional[Dict[str, Dict[str, str]]] = None
    default_config_parser: ConfigParser = field(default_factory=ConfigParser)
    custom_config_parser: ConfigParser = field(default_factory=ConfigParser)

    def __post_init__(self) -> None:
        self._validate_default_config()

    def _validate_default_config(self) -> None:
        """Ensures default configuration is valid."""
        if not isinstance(self.default_config, (dict, type(None))):
            raise ValueError("default_config must be a dictionary or None")
        if self.default_config is not None:
            for section, options in self.default_config.items():
                if not isinstance(options, dict):
                    raise ValueError(f"Invalid options for section {section} in default_config")
                for option, value in options.items():
                    if not isinstance(option, str) or not isinstance(value, str):
                        raise ValueError(f"Invalid option or value for section {section} in default_config")


class _ConfigFileHandler():
    """Manages configuration files."""
    configs: Dict[str, ConfigData] = {}
    lock: threading.RLock = threading.RLock()
    logger = Logger.get_logger(FRAMEWORK_NAME)

    # Methods for the public interface
    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig, default_config: Optional[Dict[str, Dict[str, str]]] = None) -> None:
        """Adds a new configuration."""
        with cls.lock:
            if not config_name:
                raise ValueError("config_name must be set")
            if config_name in cls.configs:
                cls.logger.log_warning(f"Configuration \"{config_name}\" already exists.", "_ConfigFileHandler._add_config")
                return
            cls.configs[config_name] = ConfigData(file_handler_config=handler_config, default_config=default_config)
            cls._sync_default_config(config_name)
            cls._sync_custom_config(config_name)

    @classmethod
    def _get_custom_config(cls, config_name: str) -> Dict[str, Dict[str, str]]:
        """Gets the entire configuration data."""
        with cls.lock:
            cls._ensure_config_exists(config_name, "_get_config")
            return cls.configs[config_name].custom_config_parser._sections

    @classmethod
    def _get_default_config(cls, config_name: str) -> Dict[str, Dict[str, str]]:
        """Gets the entire default configuration data."""
        with cls.lock:
            cls._ensure_config_exists(config_name, "_get_default_config")
            return cls.configs[config_name].default_config_parser._sections

    @classmethod
    def _save_custom_config_to_file(cls, config_name: str) -> None:
        """Saves the custom configuration to a file."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_save_custom_config_to_file")
            cls._save_config_to_file(config_data.custom_config_parser, config_data.file_handler_config.custom_config_path)

    @classmethod
    def _load_custom_config_from_file(cls, config_name: str) -> None:
        """Loads the custom configuration from a file."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_load_custom_config_from_file")
            cls._load_config_from_file(config_data.custom_config_parser, config_data.file_handler_config.custom_config_path)

    @classmethod
    def _sync_custom_config(cls, config_name: str) -> None:
        """Synchronizes the custom configuration."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_sync_custom_config")
            try:
                try:
                    cls._load_config_from_file(config_data.custom_config_parser, config_data.file_handler_config.custom_config_path)
                except FileNotFoundError:
                    cls._repopulate_config(config_data.custom_config_parser, config_data.default_config_parser)
                    cls._save_config_to_file(config_data.custom_config_parser, config_data.file_handler_config.custom_config_path)
            except Exception as e:
                cls.logger.log_error(f"Failed to synchronize custom configuration for {config_name}: {str(e)}", "_ConfigFileHandler._sync_custom_config")
                raise ValueError(f"Failed to synchronize custom configuration for {config_name}: {str(e)}")

    @classmethod
    def _sync_default_config(cls, config_name: str) -> None:
        """Synchronizes the default configuration with file or dictionary."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_sync_default_config")
            try:
                try:
                    cls._load_config_from_file(config_data.default_config_parser, config_data.file_handler_config.default_config_path)
                except FileNotFoundError:
                    if config_data.default_config:
                        cls._repopulate_config(config_data.default_config_parser, config_data.default_config)
                    cls._save_config_to_file(config_data.default_config_parser, config_data.file_handler_config.default_config_path)
            except Exception as e:
                cls.logger.log_error(f"Failed to synchronize default configuration for {config_name}: {str(e)}", "_ConfigFileHandler._sync_default_config")
                raise ValueError(f"Failed to synchronize default configuration for {config_name}: {str(e)}")

    @classmethod
    def _reset_custom_config(cls, config_name: str, auto_save: bool = True) -> None:
        """Resets all custom settings to their default values."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_reset_config")
            try:
                cls._repopulate_config(config_data.custom_config_parser, config_data.default_config_parser)
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to reset config {config_name}: {str(e)}", "_ConfigFileHandler._reset_config")
                raise ValueError(f"Failed to reset config {config_name}: {str(e)}")

    @classmethod
    def _save_setting(cls, config_name: str, section: str, option: str, value: str, auto_save: bool = True) -> None:
        """Saves a specific setting to the configuration."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_save_setting")
            try:
                if not config_data.custom_config_parser.has_section(section):
                    config_data.custom_config_parser.add_section(section)
                config_data.custom_config_parser.set(section, option, value)
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to save setting {option} in section {section} for config {config_name}: {str(e)}", "_ConfigFileHandler._save_setting")
                raise ValueError(f"Failed to save setting {option} in section {section} for config {config_name}: {str(e)}")

    @classmethod
    def _save_settings(cls, config_name: str, settings: Dict[str, Dict[str, str]], auto_save: bool = True) -> None:
        """Saves multiple settings to the configuration."""
        with cls.lock:
            try:
                for section, options in settings.items():
                    for option, value in options.items():
                        cls._save_setting(config_name, section, option, value, auto_save=False)
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to save settings for config {config_name}: {str(e)}", "_ConfigFileHandler._save_settings")
                raise ValueError(f"Failed to save settings for config {config_name}: {str(e)}")

    @classmethod
    def _get_setting(cls, config_name: str, section: str, option: str, fallback_value: Optional[str] = None, force_default: bool = False) -> str:
        """Retrieves a specific setting from the configuration."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_get_setting")
            try:
                if not force_default:
                    if config_data.custom_config_parser.has_option(section, option):
                        return config_data.custom_config_parser.get(section, option)
                if config_data.default_config_parser.has_option(section, option):
                    return config_data.default_config_parser.get(section, option)
                return fallback_value if fallback_value is not None else "NoDefaultValue"
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to get setting {option} in section {section} for config {config_name}: {str(e)}", "_ConfigFileHandler._get_setting")
                raise ValueError(f"Failed to get setting {option} in section {section} for config {config_name}: {str(e)}")

    @classmethod
    def _get_settings(cls, config_name: str, settings: Dict[str, Dict[str, str]], force_default: bool = False) -> Dict[str, Dict[str, str]]:
        """Retrieves multiple settings from the configuration."""
        with cls.lock:
            result: Dict[str, Dict[str, str]] = {}
            try:
                for section, options in settings.items():
                    result_section = result.setdefault(section, {})
                    for option, fallback_value in options.items():
                        result_section[option] = cls._get_setting(config_name, section, option, fallback_value, force_default)
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to get settings for config {config_name}: {str(e)}", "_ConfigFileHandler._get_settings")
                raise ValueError(f"Failed to get settings for config {config_name}: {str(e)}")
            return result

    @classmethod
    def _reset_setting(cls, config_name: str, section: str, option: str, auto_save: bool = True) -> None:
        """Resets a specific setting to its default value."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_reset_setting")
            try:
                if config_data.default_config_parser.has_section(section) and option in config_data.default_config_parser[section]:
                    config_data.custom_config_parser.setdefault(section, {})[option] = config_data.default_config_parser[section][option]
                elif config_data.custom_config_parser.has_section(section):
                    del config_data.custom_config_parser[section][option]
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to reset setting {option} in section {section} for config {config_name}: {str(e)}", "_ConfigFileHandler._reset_setting")
                raise ValueError(f"Failed to reset setting {option} in section {section} for config {config_name}: {str(e)}")

    @classmethod
    def _reset_settings(cls, config_name: str, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        """Resets multiple settings to their default values."""
        with cls.lock:
            try:
                for section, options in settings.items():
                    for option in options:
                        cls._reset_setting(config_name, section, option, auto_save=False)
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to reset settings for config {config_name}: {str(e)}", "_ConfigFileHandler._reset_settings")
                raise ValueError(f"Failed to reset settings for config {config_name}: {str(e)}")

    @classmethod
    def _reset_section(cls, config_name: str, section: str, auto_save: bool = True) -> None:
        """Resets all settings in a section to their default values."""
        with cls.lock:
            config_data = cls._ensure_config_exists(config_name, "_reset_section")
            try:
                if section in config_data.default_config_parser:
                    config_data.custom_config_parser[section] = {k: v for k, v in config_data.default_config_parser[section].items()}
                elif section in config_data.custom_config_parser:
                    del config_data.custom_config_parser[section]
                if auto_save:
                    cls._save_custom_config_to_file(config_name)
            except configparser.Error as e:
                cls.logger.log_error(f"Failed to reset section {section} for config {config_name}: {str(e)}", "_ConfigFileHandler._reset_section")
                raise ValueError(f"Failed to reset section {section} for config {config_name}: {str(e)}")

    # Methods for internal use
    @classmethod
    def _ensure_config_exists(cls, config_name: str, caller_method_name: str) -> Optional[ConfigData]:
        """Checks if configuration exists; returns config data or None."""
        config_data = cls.configs.get(config_name, None)
        if config_data is None:
            cls.logger.log_error(f"Config {config_name} does not exist in {cls.configs}.", "_ConfigFileHandler._ensure_config_exists")
            raise ValueError(f"Config {config_name} does not exist in {cls.configs}.")
        return config_data

    @classmethod
    def _load_config_from_file(cls, config: ConfigParser, config_path: str) -> None:
        """Reads configuration from specified file."""
        with cls.lock:
            try:
                with open(config_path, 'r', encoding="utf-8") as f:
                    config.read_file(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Config file {config_path} does not exist")
            except configparser.Error as e:
                raise ValueError(f"Failed to load config from {config_path}: {e}")

    @classmethod
    def _save_config_to_file(cls, config: ConfigParser, config_path: str) -> None:
        """Writes configuration to specified file."""
        with cls.lock:
            try:
                with open(config_path, 'w', encoding="utf-8") as f:
                    config.write(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Config file {config_path} does not exist")
            except configparser.Error as e:
                raise ValueError(f"Failed to save config to {config_path}: {e}")

    @classmethod
    def _repopulate_config(cls, config: ConfigParser, values: Union[Dict[str, Dict[str, str]], ConfigParser]) -> None:
        """Repopulates a configuration with new values."""
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
