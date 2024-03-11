# GuiFramework/utilities/config/_config_file_handler.py

import configparser

from typing import Any, Dict
from dataclasses import dataclass, field
from functools import cached_property

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import Logger
from GuiFramework.utilities.file_ops import FileOps


@dataclass
class ConfigFileHandlerConfig:
    """Configuration for a configuration file handler."""
    config_path: str = "config"
    default_config_name: str = "default-config.ini"
    custom_config_name: str = "custom-config.ini"
    default_config_creator_func: Any = lambda: {}

    @cached_property
    def default_config_path(self):
        """Path to the default configuration file."""
        return FileOps.join_paths(self.config_path, self.default_config_name)

    @cached_property
    def custom_config_path(self):
        """Path to the custom configuration file."""
        return FileOps.join_paths(self.config_path, self.custom_config_name)

    def __post_init__(self):
        """Post-initialization validation of ConfigFileHandlerConfig."""
        if not FileOps.directory_exists(self.config_path):
            FileOps.create_directory(self.config_path)
        if not self.default_config_name.endswith(".ini"):
            raise ValueError(f"Invalid default_config_name: {self.default_config_name}")
        if not self.custom_config_name.endswith(".ini"):
            raise ValueError(f"Invalid custom_config_name: {self.custom_config_name}")
        if self.default_config_name == self.custom_config_name:
            raise ValueError(f"default_config_name and custom_config_name cannot be the same")
        if not callable(self.default_config_creator_func):
            raise ValueError(f"default_config_creator_func must be callable")
        config_data_test = self.default_config_creator_func()
        if not isinstance(config_data_test, dict):
            raise ValueError(f"default_config_creator_func must return a dictionary")


@dataclass
class ConfigData:
    """Dataclass for storing configuration data."""
    default_config: configparser.ConfigParser = field(default_factory=configparser.ConfigParser, init=False)
    custom_config: configparser.ConfigParser = field(default_factory=configparser.ConfigParser, init=False)
    default_config_data: Dict[str, Dict[str, str]] = field(default_factory=dict)


@dataclass
class ConfigContainer:
    """Dataclass for storing configuration data."""
    handler_config: ConfigFileHandlerConfig
    config_data: ConfigData


class _ConfigFileHandler:
    """Class for handling configuration files."""
    config_containers: Dict[str, ConfigContainer] = {}

    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig):
        """Add a new configuration to the _ConfigFileHandler."""
        if config_name in cls.config_containers:
            cls._warning(f"Config \"{config_name}\" already exists.")
            return
        config_data = cls._initialize_config_data(handler_config)
        cls.config_containers[config_name] = ConfigContainer(handler_config, config_data)

    @classmethod
    def _initialize_config_data(cls, handler_config: ConfigFileHandlerConfig):
        """Initialize the configuration data."""
        config_data = ConfigData()
        config_data.default_config_data = handler_config.default_config_creator_func()
        try:
            if not FileOps.file_exists(handler_config.default_config_path):
                cls._generate_default_config(config_data.default_config_data, handler_config.default_config_path)
            config_data.default_config.read(handler_config.default_config_path, encoding="utf-8")
            if not FileOps.file_exists(handler_config.custom_config_path):
                FileOps.copy_file(handler_config.default_config_path, handler_config.custom_config_path)
            config_data.custom_config.read(handler_config.custom_config_path, encoding="utf-8")
        except (FileNotFoundError, configparser.Error) as e:
            cls._error(f"Failed to load configuration from path \"{handler_config.custom_config_path}\": {e}")
            raise RuntimeError(f"Failed to load configuration from path \"{handler_config.custom_config_path}\": {e}")
        return config_data

    @classmethod
    def _generate_default_config(cls, default_config_data: Dict[str, Dict[str, str]], default_config_path: str):
        """Generate a default configuration file."""
        config = configparser.ConfigParser()
        for section, settings in default_config_data.items():
            config[section] = settings
        try:
            FileOps.write_file(default_config_path, config)
        except IOError as e:
            cls._error(f"Failed to write default configuration to path \"{default_config_path}\": {e}")
            raise IOError(f"Failed to write default configuration to path \"{default_config_path}\": {e}")

    # setting handling methods
    @classmethod
    def _save_setting(cls, config_name, section, option, value):
        """Save a setting to the configuration file."""
        try:
            config_container = cls.config_containers.get(config_name)
            if config_container is None:
                raise configparser.Error(f"Config \"{config_name}\" not found.")
            config_data = config_container.config_data
            handler_config = config_container.handler_config
            saver = handler_config.custom_type_handlers.get(type(value)).save
            if saver:
                value = saver(value)
            config_data.custom_config.set(section, option, value)
            cls._write_config_to_file(config_data.custom_config, handler_config.custom_config_path)
            dynamic_store_value = config_data.dynamic_store.get(option)
            if dynamic_store_value is not None:
                dynamic_store_value["value"] = value
        except configparser.Error as e:
            cls._error(f"Failed to save setting \"{option}\" in section \"{section}\": {e}")
            raise configparser.Error(f"Failed to save setting \"{option}\" in section \"{section}\": {e}")

    @classmethod
    def _get_setting(cls, config_name, section, option, fallback_value=None, force_default=False):
        """Get a setting from the configuration file."""
        try:
            config_container = cls.config_containers.get(config_name)
            if config_container is None:
                raise configparser.Error(f"Config \"{config_name}\" not found.")
            config_data = config_container.config_data
            return config_data.default_config.get(section, option) if force_default else config_data.custom_config.get(section, option, fallback=default_value)
        except configparser.NoSectionError:
            cls._error(f"Section \"{section}\" not found in configuration. Using default value.")
            raise configparser.NoSectionError(f"Section \"{section}\" not found in configuration.")
        except configparser.Error as e:
            cls._error(f"Failed to load setting \"{option}\" in section \"{section}\": {e}")
            if fallback_value is None:
                raise configparser.Error(f"No default value provided for \"{option}\" in section \"{section}\"")
            return fallback_value

    @classmethod
    def _reset_setting(cls, config_name, section, option):
        """Reset a setting to the default value."""
        try:
            config_container = cls.config_containers.get(config_name)
            config_data = config_container.config_data
            handler_config = config_container.handler_config
            default_value = config_data.default_config.get(section, option)
            config_data.custom_config.set(section, option, default_value)
            cls._write_config_to_file(config_data.custom_config, handler_config.custom_config_path)
            dynamic_store_value = config_data.dynamic_store.get(option)
            if dynamic_store_value is not None:
                creator = handler_config.custom_type_handlers.get(type(dynamic_store_value["value"])).create
                if creator:
                    default_value = creator(default_value)
                dynamic_store_value["value"] = default_value
        except configparser.NoSectionError:
            cls._error(f"Section \"{section}\" not found in default configuration.")
            raise configparser.NoSectionError(f"Section \"{section}\" not found in default configuration.")
        except configparser.NoOptionError:
            cls._error(f"Option \"{option}\" not found in section \"{section}\" of default configuration.")
            raise configparser.NoOptionError(f"Option \"{option}\" not found in section \"{section}\" of default configuration.")
        except configparser.Error as e:
            cls._error(f"Failed to reset setting \"{option}\" in section \"{section}\": {e}")
            raise configparser.Error(f"Failed to reset setting \"{option}\" in section \"{section}\": {e}")

    @classmethod
    def _reset_section(cls, config_name, section):
        """Reset a section to the default values."""
        try:
            config_container = cls.config_containers.get(config_name)
            config_data = config_container.config_data
            handler_config = config_container.handler_config
            default_settings = config_data.default_config[section]
            config_data.custom_config[section] = default_settings
            cls._write_config_to_file(config_data.custom_config, handler_config.custom_config_path)
            for option, value in default_settings.items():
                dynamic_store_value = config_data.dynamic_store.get(option)
                if dynamic_store_value is not None:
                    creator = handler_config.custom_type_handlers.get(type(dynamic_store_value["value"])).create
                    if creator:
                        value = creator(value)
                    dynamic_store_value["value"] = value
        except configparser.NoSectionError:
            cls._error(f"Section \"{section}\" not found in default configuration.")
            raise configparser.NoSectionError(f"Section \"{section}\" not found in default configuration.")
        except configparser.Error as e:
            cls._error(f"Failed to reset section \"{section}\": {e}")
            raise configparser.Error(f"Failed to reset section \"{section}\": {e}")

    @classmethod
    def reset_config(cls, config_name):
        """Reset the entire configuration to the default values."""
        config_data = cls.config_containers.get(config_name).config_data
        config_data.custom_config.clear()
        config_data.custom_config.read(cls.setup.default_config_path, encoding="utf-8")
        cls._write_config_to_file(config_data.custom_config, cls.setup.custom_config_path)

    @classmethod
    def _warning(cls, message):
        """Log a warning message."""
        Logger.warning(message, logger_name=FRAMEWORK_NAME, module_name=_ConfigFileHandler.__name__)

    @classmethod
    def _error(cls, message):
        """Log an error message."""
        Logger.error(message, logger_name=FRAMEWORK_NAME, module_name=_ConfigFileHandler.__name__)