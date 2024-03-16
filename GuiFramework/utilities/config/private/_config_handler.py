# GuiFramework/utilities/config/private/_config_handler.py
# ATTENTION: This module is for internal use only

from threading import RLock
from typing import Any, Dict, List, Optional, Tuple, Union, Type

from GuiFramework.utilities.config.custom_type_handler_base import CustomTypeHandlerBase
from ._config_file_handler import _ConfigFileHandler, ConfigFileHandlerConfig

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import StaticLoggerMixin


class ConfigVariable:
    BASIC_TYPES = {str, int, float, bool}

    def __init__(self, name: str, value: Any, section: str = "Default", auto_save: bool = True, save_to_file: bool = False, type_handler: Optional[CustomTypeHandlerBase] = None):
        self.name = name
        self.value = value
        self.section = section
        self.auto_save = auto_save
        self.save_to_file = save_to_file
        self.type_ = type(value)
        self.type_handler = type_handler

    def is_persistable(self) -> bool:
        return self.type_ in self.BASIC_TYPES or self.type_handler is not None

    def serialize(self) -> str:
        if not self.is_persistable():
            raise ValueError(f"Cannot serialize '{self.name}': value is not persistable.")
        return self.type_handler.serialize(self.value) if self.type_handler else str(self.value)

    def deserialize(self, serialized_value: str) -> Any:
        if not self.is_persistable():
            raise ValueError(f"Cannot deserialize '{self.name}': original value is not persistable.")
        return self.type_handler.deserialize(serialized_value) if self.type_handler else self.type_(serialized_value)


class _ConfigHandler(StaticLoggerMixin):
    _config_variables: Dict[str, Dict[str, List[ConfigVariable]]] = {}
    _custom_type_handlers: Dict[str, Dict[type, CustomTypeHandlerBase]] = {}
    _lock = RLock()

    StaticLoggerMixin.set_logger_details(FRAMEWORK_NAME, "_ConfigHandler")

    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig, default_config: Optional[Dict[str, Dict[str, str]]] = None, custom_type_handlers: Optional[Dict[type, CustomTypeHandlerBase]] = None) -> None:
        """Introduces a new configuration to the system."""
        _ConfigFileHandler._add_config(config_name, handler_config, default_config)
        if custom_type_handlers:
            cls._add_custom_type_handlers(config_name, custom_type_handlers)

    @classmethod
    def _add_custom_type_handler(cls, config_name: str, handler: CustomTypeHandlerBase) -> None:
        """Adds a custom type handler."""
        if not issubclass(handler.__class__, CustomTypeHandlerBase):
            cls.log_warning("_add_custom_type_handler", f"Failed to add custom type handler: {handler} is not a subclass of CustomTypeHandlerBase.")
            return
        cls._custom_type_handlers.setdefault(config_name, {})[handler.get_type()] = handler

    @classmethod
    def _add_custom_type_handlers(cls, config_name: str, handlers: Dict[type, CustomTypeHandlerBase]) -> None:
        """Add or update custom type handlers."""
        for type_, handler in handlers.items():
            cls._add_custom_type_handler(config_name, handler)

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

    @classmethod
    def _save_setting(cls, config_name: str, section: str, option: str, value: Any, auto_save: bool = True) -> None:
        """Saves a setting to a configuration file with enhanced error handling."""
        try:
            serialized_value = cls._serialize(config_name, value)
            if not isinstance(serialized_value, str):
                raise ValueError(f"Serialization failed: {serialized_value} is not a string.")
            _ConfigFileHandler._save_setting(config_name, section, option, serialized_value, auto_save)
        except Exception as e:
            cls.log_error("_save_setting", f"Error saving setting '{option}' in [{config_name}][{section}]: {e}")

    @classmethod
    def _save_settings(cls, config_name: str, settings: Dict[str, Any], auto_save: bool = True) -> None:
        """Saves multiple settings to a configuration file with enhanced error handling."""
        for section, options in settings.items():
            for option, value in options.items():
                cls._save_setting(config_name, section, option, value, False)
        if auto_save:
            _ConfigFileHandler._save_custom_config_to_file(config_name)

    @classmethod
    def _get_setting(cls, config_name: str, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False, type_to_convert: Optional[Type] = None) -> Any:
        """Retrieves a setting from a configuration file."""
        value = _ConfigFileHandler._get_setting(config_name, section, option, fallback_value, force_default)
        return cls._deserialize(config_name, value, type_to_convert) if type_to_convert else value

    @classmethod
    def _get_settings(cls, config_name: str, settings: Dict[str, Dict[str, Any]], force_default: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieves multiple settings from a configuration file."""
        config_settings = _ConfigFileHandler._get_settings(config_name, settings, force_default)
        return {section: {option: cls._get_setting(config_name, section, option, value, force_default) for option, value in options.items()} for section, options in config_settings.items()}

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

    @classmethod
    def _add_variable(cls, config_name: str, variable: ConfigVariable) -> None:
        """Add a new variable to the dynamic store."""
        if not isinstance(variable, ConfigVariable):
            cls.log_error("_add_variable", f"Failed to add variable: {variable} is not an instance of ConfigVariable.")
            raise TypeError(f"Expected variable to be of type 'ConfigVariable', got '{type(variable).__name__}' instead.")
        with cls._lock:
            section_variables = cls._config_variables.setdefault(config_name, {}).setdefault(variable.section, [])
            if variable.name in (existing_variable.name for existing_variable in section_variables):
                cls.log_warning("_add_variable", f"Failed to add variable: {variable.name} is already present in section {variable.section}.")
                return
            section_variables.append(variable)
        if variable.save_to_file and variable.is_persistable():
            value_from_file = _ConfigFileHandler._get_setting(config_name, variable.section, variable.name)
            if value_from_file is not None:
                variable.value = variable.deserialize(value_from_file)
            else:
                _ConfigFileHandler._save_setting(config_name, variable.section, variable.name, variable.serialize(), variable.auto_save)

    @classmethod
    def _add_variables(cls, config_name: str, variables: List[ConfigVariable]) -> None:
        """Add multiple new variables to the dynamic store."""
        with cls._lock:
            for variable in variables:
                cls._add_variable(config_name, variable)

    @classmethod
    def _set_variable(cls, config_name: str, updated_variable: ConfigVariable) -> None:
        """Set or update a variable in the dynamic store."""
        if not isinstance(updated_variable, ConfigVariable):
            cls.log_error("_set_variable", f"Failed to set variable: {updated_variable} is not an instance of ConfigVariable.")
            raise TypeError(f"Expected variable to be of type 'ConfigVariable', got '{type(updated_variable).__name__}' instead.")
        with cls._lock:
            section_variables = cls._config_variables.get(config_name, {}).get(updated_variable.section, [])
            for i, existing_variable in enumerate(section_variables):
                if existing_variable.name != updated_variable.name:
                    continue
                if existing_variable.type_ != updated_variable.type_:
                    section_variables[i] = updated_variable
                    cls.log_info("_set_variable", f"Variable '{updated_variable.name}' replaced due to type change from {existing_variable.type_.__name__} to {updated_variable.type_.__name__}.")
                else:
                    existing_variable.value = updated_variable.value
                    cls.log_info("_set_variable", f"Value of variable '{updated_variable.name}' updated in section '{updated_variable.section}'.")
                if existing_variable.save_to_file and existing_variable.is_persistable():
                    _ConfigFileHandler._save_setting(config_name, existing_variable.section, existing_variable.name, existing_variable.serialize(), existing_variable.auto_save)
                return
            cls.log_warning("_set_variable", f"Failed to set variable: '{updated_variable.name}' is not present in section '{updated_variable.section}'.")

    @classmethod
    def _set_variables(cls, config_name: str, updated_variables: List[ConfigVariable]) -> None:
        """Set or update multiple variables in the dynamic store."""
        with cls._lock:
            for variable in updated_variables:
                cls._set_variable(config_name, variable)

    @classmethod
    def _get_variable(cls, config_name: str, variable_name: str, section: Optional[str] = None) -> Optional[ConfigVariable]:
        """Retrieve a variable from the dynamic store."""
        with cls._lock:
            section = section or "Default"
            section_variables = cls._config_variables.get(config_name, {}).get(section, [])
            variable = next((variable for variable in section_variables if variable.name == variable_name), None)
            if variable is None:
                cls.log_warning("_get_variable", f"Variable '{variable_name}' not found in section '{section}' of config '{config_name}'.")
            return variable

    @classmethod
    def _get_variables(cls, config_name: str, variables: List[Union[str, Tuple[str, str]]]) -> Dict[str, Dict[str, Optional[ConfigVariable]]]:
        """Retrieve multiple variables from the dynamic store, allowing for optional section specification."""
        with cls._lock:
            result = {}
            for item in variables:
                variable_name, section = item if isinstance(item, tuple) else (item, "Default")
                result.setdefault(section, {})[variable_name] = cls._get_variable(config_name, variable_name, section)
            return result

    @classmethod
    def _delete_variable(cls, config_name: str, variable_name: str, section: Optional[str] = None) -> None:
        """Delete a variable from the dynamic store."""
        with cls._lock:
            section = section or "Default"
            section_variables = cls._config_variables.get(config_name, {}).get(section, [])
            updated_section_variables = [variable for variable in section_variables if variable.name != variable_name]
            if len(section_variables) == len(updated_section_variables):
                cls.log_warning("_delete_variable", f"Failed to delete variable: '{variable_name}' not found in section '{section}' of config '{config_name}'.")
            else:
                cls._config_variables[config_name][section] = updated_section_variables

    @classmethod
    def _delete_variables(cls, config_name: str, variables: List[Union[str, Tuple[str, str]]]) -> None:
        """Delete multiple variables from the dynamic store, allowing for optional section specification."""
        with cls._lock:
            for item in variables:
                variable_name, section = item if isinstance(item, tuple) else (item, "Default")
                cls._delete_variable(config_name, variable_name, section)

    @classmethod
    def _deserialize(cls, config_name: str, value: str, type_: Type) -> Any:
        """Deserialize a value."""
        handler = cls._custom_type_handlers.get(config_name, {}).get(type_.__name__)
        return handler.deserialize(value) if handler else type_(value)

    @classmethod
    def _serialize(cls, config_name: str, value: Any) -> str:
        """Serialize a value."""
        handler = cls._custom_type_handlers.get(config_name, {}).get(type(value).__name__)
        return handler.serialize(value) if handler else str(value)
