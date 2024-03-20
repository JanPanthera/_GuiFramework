# GuiFramework/utilities/config/internal/_config_container.py
# ATTENTION: This module is for internal use only

from typing import List, Type, Any, Tuple

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.config.config_types import ConfigKey, ConfigVariable, BASIC_TYPES
from GuiFramework.utilities.config.custom_type_handler_base import CustomTypeHandlerBase
from GuiFramework.utilities.config.exceptions import (
    HandlerTypeError, HandlerValidationFailed, HandlerAlreadyExists, HandlerNotFound,
    ConfigVariableTypeError, ConfigKeyAlreadyExists, ConfigKeyNotFound
)
from GuiFramework.utilities.logging.logger import Logger


class _BaseContainer(dict):
    def __init__(self, *args, **kwargs):
        """Initialize the base container."""
        super().__init__(*args, **kwargs)
        self._logger = Logger.get_logger(FRAMEWORK_NAME)

    def _validate_type(self, instance: Any, expected_type: Type, name: str, caller: str = "") -> None:
        """Validate the type of the given instance."""
        if not isinstance(instance, expected_type):
            self._log_and_raise_error(ConfigVariableTypeError, f"{name.capitalize()} {instance} is not an instance of {expected_type.__name__}.", caller)

    def _log_and_raise_error(self, exception: Type[Exception], message: str, caller: str = "") -> None:
        """Log an error message and raise the specified exception."""
        self._logger.log_error(message, module_name=caller)
        raise exception(message)


class _ConfigVariableContainer(_BaseContainer):
    def _add_variable(self, variable: ConfigVariable) -> None:
        """Add a single configuration variable."""
        self._validate_type(variable, ConfigVariable, 'variable', caller=self.__class__.__name__ + '._add_variable')
        if variable._config_key in self:
            self._log_and_raise_error(ConfigKeyAlreadyExists, f"ConfigKey {variable._config_key} already exists.", caller=self.__class__.__name__ + '._add_variable')
        self[variable._config_key] = variable

    def _add_variables(self, variables: List[ConfigVariable]) -> None:
        """Add multiple configuration variables."""
        for variable in variables:
            self._add_variable(variable)

    def _get_variable(self, config_key: ConfigKey) -> ConfigVariable:
        """Retrieve a configuration variable by its key."""
        if config_key not in self:
            self._log_and_raise_error(ConfigKeyNotFound, f"No ConfigKey found for name {config_key.name}.", caller=self.__class__.__name__ + '._get_variable')
        return self[config_key]

    def _get_variables(self, config_keys: List[ConfigKey]) -> List[ConfigVariable]:
        """Retrieve multiple configuration variables by their keys."""
        return [self._get_variable(config_key) for config_key in config_keys]

    def _get_variable_value(self, config_key: ConfigKey) -> Any:
        """Retrieve the value of a configuration variable by its key."""
        return self._get_variable(config_key).value

    def _get_variable_values(self, config_keys: List[ConfigKey]) -> List[Any]:
        """Retrieve the values of multiple configuration variables by their keys."""
        return [self._get_variable_value(config_key) for config_key in config_keys]

    def _set_variable(self, variable: ConfigVariable) -> None:
        """Set a configuration variable."""
        if variable._config_key not in self:
            self._log_and_raise_error(ConfigKeyNotFound, f"No ConfigKey found for name {variable._config_key.name}.", caller=self.__class__.__name__ + '._set_variable')
        self[variable._config_key] = variable

    def _set_variables(self, variables: List[ConfigVariable]) -> None:
        """Set multiple configuration variables."""
        for variable in variables:
            self._set_variable(variable)

    def _set_variable_value(self, config_key: ConfigKey, value: Any) -> None:
        """Set the value of a configuration variable by its key."""
        self._get_variable(config_key).set_value(value)

    def _set_variable_values(self, config_keys: List[Tuple[ConfigKey, Any]]) -> None:
        """Set the values of multiple configuration variables by their keys."""
        for config_key, value in config_keys:
            self._set_variable_value(config_key, value)

    def _delete_variable(self, config_key: ConfigKey) -> None:
        """Delete a configuration variable by its key."""
        if config_key not in self:
            self._log_and_raise_error(ConfigKeyNotFound, f"No ConfigKey found for name {config_key.name}.", caller=self.__class__.__name__ + '._delete_variable')
        del self[config_key]

    def _delete_variables(self, config_keys: List[ConfigKey]) -> None:
        """Delete multiple configuration variables by their keys."""
        for config_key in config_keys:
            self._delete_variable(config_key)


class _TypeHandlerContainer(_BaseContainer):
    def _add_type_handler(self, handler: CustomTypeHandlerBase) -> None:
        """Add a custom type handler."""
        self._validate_type(handler, CustomTypeHandlerBase, 'handler')
        self._validate_handler(handler)
        type_ = handler.get_type()
        if self.get(type_):
            self._log_and_raise_error(HandlerAlreadyExists, f"Custom type handler for type {type_.__name__} already exists.", caller=self.__class__.__name__ + '._add_type_handler')
        self[type_] = handler

    def _add_custom_type_handlers(self, custom_type_handlers: List[CustomTypeHandlerBase]) -> None:
        """Add multiple custom type handlers."""
        for handler in custom_type_handlers:
            self._add_type_handler(handler)

    def _get_type_handler(self, type_: Type) -> CustomTypeHandlerBase:
        """Retrieve a custom type handler by type."""
        handler = self.get(type_)
        if handler is None:
            if type_ in BASIC_TYPES:
                return type_

        if handler is None:
            self._log_and_raise_error(HandlerNotFound, f"No type handler found for type {type_.__name__}.", caller=self.__class__.__name__ + '._get_type_handler')
        return handler

    def _delete_type_handler(self, type_: Type) -> None:
        """Delete a custom type handler by type."""
        if type_ in self:
            del self[type_]
        else:
            self._log_and_raise_error(HandlerNotFound, f"No type handler found for type {type_.__name__}.", caller=self.__class__.__name__ + '._delete_type_handler')

    def _has_type_handler(self, type_: Type) -> bool:
        """Check if a custom type handler exists for a given type."""
        return type_ in self

    def _validate_handler(self, handler: CustomTypeHandlerBase) -> None:
        """Validate a custom type handler."""
        try:
            handler.validate_custom_type_handler()
        except AssertionError as e:
            self._log_and_raise_error(HandlerValidationFailed, f"Validation failed for handler {handler}: {e}", caller=self.__class__.__name__ + '._validate_handler')

