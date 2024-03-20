# GuiFramework/utilities/config/internal/_config_handler.py
# ATTENTION: This module is for internal use only

from threading import RLock
from typing import Any, Dict, List, Optional, Tuple, Union


from GuiFramework.utilities.config.custom_type_handler_base import CustomTypeHandlerBase
from ._config_file_handler import _ConfigFileHandler, ConfigFileHandlerConfig

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import Logger
from GuiFramework.utilities.config.exceptions import *
from GuiFramework.utilities.config.config_types import ConfigKey, ConfigVariable, BASIC_TYPES
from GuiFramework.utilities.config.internal._config_container import _ConfigVariableContainer, _TypeHandlerContainer


class _ConfigHandler:
    _logger = Logger.get_logger(FRAMEWORK_NAME)
    _config_variables = _ConfigVariableContainer()
    _type_handler_container = _TypeHandlerContainer()
    _lock = RLock()

    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig, default_config: Optional[List[CustomTypeHandlerBase]] = None, custom_type_handlers: Optional[Dict[type, CustomTypeHandlerBase]] = None) -> None:
        """Introduces a new configuration to the system."""
        _ConfigFileHandler._add_config(config_name, handler_config, default_config)
        if custom_type_handlers:
            cls._type_handler_container._add_custom_type_handlers(custom_type_handlers)

    @classmethod
    def _get_custom_config(cls, config_name: str) -> Dict[str, Dict[str, str]]:
        """Retrieves custom configuration with optional type handling."""
        return _ConfigFileHandler._get_custom_config(config_name)

    @classmethod
    def _get_default_config(cls, config_name: str) -> Dict[str, Dict[str, str]]:
        """Retrieves the entire default configuration data."""
        return _ConfigFileHandler._get_default_config(config_name)

    @classmethod
    def _save_custom_config_to_file(cls, config_name: str) -> None:
        """Saves the custom config to the custom config file."""
        _ConfigFileHandler._save_custom_config_to_file(config_name)

    @classmethod
    def _load_custom_config_from_file(cls, config_name: str) -> None:
        """Loads the custom config from the custom config file."""
        with cls._lock:
            _ConfigFileHandler._load_custom_config_from_file(config_name)

    @classmethod
    def _sync_custom_config(cls, config_name: str) -> None:
        """Synchronizes the custom config with the custom config file."""
        with cls._lock:
            _ConfigFileHandler._sync_config(config_name, "custom")

    @classmethod
    def _sync_default_config(cls, config_name: str) -> None:
        """Synchronizes the default config with the default config file."""
        with cls._lock:
            _ConfigFileHandler._sync_config(config_name, "default")

    @classmethod
    def _reset_custom_config(cls, config_name: str, auto_save: bool = True) -> None:
        """Resets an entire configuration file to default values."""
        with cls._lock:
            _ConfigFileHandler._reset_custom_config(config_name, auto_save)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def _save_setting(cls, config_key: ConfigKey, value: str = "NoValue") -> None:
        """Saves a setting to a configuration file."""
        try:
            if not isinstance(value, str):
                serialized_value = cls._serialize(config_key, value)
                if serialized_value is not None:
                    value = serialized_value
                if not isinstance(value, str):
                    raise ValueNotSaveable(f"Expected 'str', got '{type(value).__name__}'.")
            _ConfigFileHandler._save_setting(config_key.config_name, config_key.section, config_key.name, value, config_key.auto_save)
        except Exception as e:
            cls._logger.log_error(f"Error saving setting '{config_key.name}' in [{config_key.config_name}][{config_key.section}]: {e}", "_ConfigHandler")

    @classmethod
    def _save_settings(cls, config_keys: List[Tuple[ConfigKey, Any]]) -> None:
        for config_key, value in config_keys:
            cls._save_setting(config_key, value)

    @classmethod
    def _get_setting(cls, config_key: ConfigKey, fallback_value: Any = None, force_default: bool = False) -> Any:
        """Retrieves a setting from a configuration file."""
        value = _ConfigFileHandler._get_setting(config_key.config_name, config_key.section, config_key.name, fallback_value, force_default)
        return cls._deserialize(config_key, value)

    @classmethod
    def _get_settings(cls, config_keys: List[Dict[str, Union[ConfigKey, Any, bool]]]) -> Dict[str, Dict[str, Any]]:
        """Retrieves multiple settings from a configuration file."""
        settings = {}
        for config_dict in config_keys:
            config_key = config_dict.get('config_key')
            fallback_value = config_dict.get('fallback_value', None)
            force_default = config_dict.get('force_default', False)

            if config_key is not None:
                settings.setdefault(config_key.config_name, {}).setdefault(config_key.section, []).append((config_key, fallback_value, force_default))

        result = {}
        for config_name, sections in settings.items():
            result[config_name] = {section: {option.name: cls._get_setting(option, fallback_value, force_default) for option, fallback_value, force_default in options} for section, options in sections.items()}
        return result

    @classmethod
    def _reset_setting(cls, config_name: str, section: str, option: str, auto_save: bool = True) -> None:
        """ResResets a setting in a configuration file to its default value."""
        _ConfigFileHandler._reset_setting(config_name, section, option, auto_save)

    @classmethod
    def _reset_settings(cls, config_name: str, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        """Resets multiple settings in a configuration file to their default values."""
        for section, options in settings.items():
            for option in options:
                _ConfigFileHandler._reset_setting(config_name, section, option, False)
        if auto_save:
            _ConfigFileHandler._save_custom_config_to_file(config_name)

    @classmethod
    def _reset_section(cls, config_name: str, section: str, auto_save: bool = True) -> None:
        """Resets an entire section in a configuration file to default values."""
        _ConfigFileHandler._reset_section(config_name, section, auto_save)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def _add_variable(cls, config_key: ConfigKey, value: Any, default_value: Any, init_from_file: bool = False) -> None:
        """Adds a single variable to the configuration, optionally initializing it from file."""
        with cls._lock:
            type_handler = cls._type_handler_container._get_type_handler(config_key.type_)
            variable = ConfigVariable(config_key=config_key, value=value, default_value=default_value, type_handler=type_handler)
            cls._config_variables._add_variable(variable)
            config_key = variable._config_key
            if variable.is_persistable():
                if init_from_file:
                    value = cls._get_setting(config_key=config_key)
                    variable.set_value(value)
                elif config_key.save_to_file:
                    cls._save_setting(config_key=config_key, value=variable.value)

    @classmethod
    def _add_variables(cls, variables: List[Union[ConfigVariable, Tuple[ConfigVariable, bool]]]) -> None:
        """Adds multiple variables to the configuration, with an optional flag to initialize from file."""
        for variable in variables:
            if isinstance(variable, ConfigVariable):
                init_from_file = False
            elif isinstance(variable, tuple) and len(variable) == 2 and isinstance(variable[0], ConfigVariable) and isinstance(variable[1], bool):
                variable, init_from_file = variable
            else:
                raise ConfigVariableTypeError(f"Expected ConfigVariable or (ConfigVariable, bool), got '{type(variable).__name__}'.")
            cls._add_variable(variable, init_from_file)

    @classmethod
    def _get_variable(cls, config_key: ConfigKey) -> ConfigVariable:
        """Retrieves a single variable from the configuration."""
        with cls._lock:
            return cls._config_variables._get_variable(config_key)

    @classmethod
    def _get_variables(cls, config_keys: List[ConfigKey]) -> List[ConfigVariable]:
        """Retrieves multiple variables from the configuration."""
        with cls._lock:
            return cls._config_variables._get_variables(config_keys)

    @classmethod
    def _get_variable_value(cls, config_key: ConfigKey) -> Any:
        """Retrieves the value of a single variable from the configuration."""
        with cls._lock:
            return cls._config_variables._get_variable(config_key).value

    @classmethod
    def _get_variable_values(cls, config_keys: List[ConfigKey]) -> List[Any]:
        """Retrieves the values of multiple variables from the configuration."""
        with cls._lock:
            return cls._config_variables._get_variable_values(config_keys)

    @classmethod
    def _set_variable(cls, updated_variable: ConfigVariable) -> None:
        """Updates a single variable in the configuration."""
        with cls._lock:
            cls._config_variables._set_variable(updated_variable)
            if updated_variable.config_key.save_to_file and updated_variable.config_key.auto_save:
                cls._save_setting(config_key=updated_variable.config_key, value=updated_variable.value)

    @classmethod
    def _set_variables(cls, updated_variables: List[ConfigVariable]) -> None:
        """Updates multiple variables in the configuration."""
        with cls._lock:
            cls._config_variables._set_variables(updated_variables)
            for variable in updated_variables:
                if variable._config_key.save_to_file and variable._config_key.auto_save:
                    cls._save_setting(config_key=variable._config_key, value=variable.value)

    @classmethod
    def _set_variable_value(cls, config_key: ConfigKey, new_value: Any) -> None:
        """Updates the value of a single variable in the configuration."""
        with cls._lock:
            cls._config_variables._set_variable_value(config_key, new_value)
            if config_key.save_to_file and config_key.auto_save:
                cls._save_setting(config_key=config_key, value=new_value)

    @classmethod
    def _set_variable_values(cls, config_keys: List[Tuple[ConfigKey, Any]]) -> None:
        """Updates the values of multiple variables in the configuration."""
        with cls._lock:
            cls._config_variables._set_variable_values(config_keys)
            for config_key, new_value in config_keys:
                if config_key.save_to_file and config_key.auto_save:
                    cls._save_setting(config_key=config_key, value=new_value)

    @classmethod
    def _delete_variable(cls, config_key: ConfigKey) -> None:
        """Deletes a single variable from the configuration."""
        with cls._lock:
            cls._config_variables._delete_variable(config_key)

    @classmethod
    def _delete_variables(cls, config_keys: List[ConfigKey]) -> None:
        """Deletes multiple variables from the configuration."""
        with cls._lock:
            cls._config_variables._delete_variables(config_keys)

    @classmethod
    def _deserialize(cls, config_key: ConfigKey, value: str) -> Any:
        """Deserialize a value based on its ConfigKey type."""
        handler = cls._type_handler_container._get_type_handler(config_key.type_)
        if handler and hasattr(handler, 'deserialize'):
            return handler.deserialize(value)
        elif config_key.type_ in BASIC_TYPES:
            return config_key.type_(value)
        else:
            return None

    @classmethod
    def _serialize(cls, config_key: ConfigKey, value: Any) -> str:
        """Serialize a value based on its ConfigKey type."""
        handler = cls._type_handler_container._get_type_handler(config_key.type_)
        if handler and hasattr(handler, 'serialize'):
            return handler.serialize(value)
        elif type(value) in BASIC_TYPES:
            return str(value)
        else:
            return None
