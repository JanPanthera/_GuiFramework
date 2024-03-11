# GuiFramework/utilities/config/_config_handler_core.py

from typing import Dict
from threading import RLock
from dataclasses import field

from .custom_type_handler_base import CustomTypeHandlerBase
from ._config_file_handler import _ConfigFileHandler, ConfigFileHandlerConfig
from ._dynamic_store_handler import _DynamicStoreHandler

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import Logger


class _ConfigHandlerCore:
    """Core class for the configuration handler."""
    custom_type_handlers: Dict[str, CustomTypeHandlerBase] = field(default_factory=dict)
    lock = RLock()

    # configuration setup methods
    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig, custom_type_handlers: Dict[str, CustomTypeHandlerBase] = None):
        """Add a configuration."""
        with cls.lock:
            _ConfigFileHandler._add_config(config_name, handler_config)
            _DynamicStoreHandler._add_store(config_name)
            if custom_type_handlers:
                cls._add_custom_type_handlers(custom_type_handlers)

    @classmethod
    def _add_custom_type_handler(cls, type_, handler):
        """Add a custom type handler."""
        if not issubclass(handler, CustomTypeHandlerBase):
            cls._warning(f"Failed to add custom type handler: {handler} is not a subclass of CustomTypeHandlerBase.")
            return
        with cls.lock:
            cls.custom_type_handlers[type_] = handler

    @classmethod
    def _add_custom_type_handlers(cls, handlers):
        """Add multiple custom type handlers."""
        with cls.lock:
            for type_, handler in handlers.items():
                cls._add_custom_type_handler(type_, handler)

    # file configuration methods
    @classmethod
    def _save_setting(cls, config_name, section, option, value):
        """Save a setting to a configuration file."""
        with cls.lock:
            _ConfigFileHandler._save_setting(config_name, section, option, value)

    @classmethod
    def _get_setting(cls, config_name, section, option, fallback_value=None, force_default=False):
        """Get a setting from a configuration file."""
        with cls.lock:
            return _ConfigFileHandler._get_setting(config_name, section, option, fallback_value, force_default)

    @classmethod
    def _reset_setting(cls, config_name, section, option):
        """Reset a setting in a configuration file."""
        with cls.lock:
            _ConfigFileHandler._reset_setting(config_name, section, option)

    @classmethod
    def _reset_section(cls, config_name, section):
        """Reset a section in a configuration file."""
        with cls.lock:
            _ConfigFileHandler._reset_section(config_name, section)

    @classmethod
    def _reset_config(cls, config_name):
        """Reset a configuration file."""
        with cls.lock:
            _ConfigFileHandler._reset_config(config_name)

    # dynamic store management methods
    @classmethod
    def _add_variable(cls, config_name, variable_name, value, section=None):
        """Add a variable to the dynamic store."""
        if value is None:
            cls._warning(f"Failed to add variable \"{variable_name}\" to dynamic store: Value cannot be None.")
            return
        with cls.lock:
            if section:
                value_from_file = _ConfigFileHandler._get_setting(config_name, section, variable_name)
                if value_from_file is not None:
                    value = cls._convert_value(value_from_file)
                else:
                    _ConfigFileHandler._save_setting(config_name, section, variable_name, cls._convert_value(value, "save"))
            _DynamicStoreHandler._add_variable(config_name, variable_name, value, section)

    @classmethod
    def _add_variables(cls, config_name, variables):
        """Add multiple variables to the dynamic store."""
        with cls.lock:
            for variable_name, value_pack in variables.items():
                value, section = cls._unpack_value_pack(value_pack)
                cls._add_variable(config_name, variable_name, value, section)

    @classmethod
    def _set_variable(cls, config_name, variable_name, value, save_override=False):
        """Set a variable in the dynamic store."""
        if value is None:
            cls._warning(f"Failed to set variable \"{variable_name}\" in dynamic store: Value cannot be None.")
            return
        with cls.lock:
            _DynamicStoreHandler._set_variable(config_name, variable_name, value)
            section = _DynamicStoreHandler._get_variable_section(config_name, variable_name)
            if section and not save_override:
                _ConfigFileHandler._save_setting(config_name, section, variable_name, cls._convert_value(value, "save"))

    @classmethod
    def _set_variables(cls, config_name, variables):
        """Set multiple variables in the dynamic store."""
        with cls.lock:
            for variable_name, value_pack in variables.items():
                value, save_override = cls._unpack_value_pack(value_pack)
                cls._set_variable(config_name, variable_name, value, save_override)

    @classmethod
    def _get_variable(cls, config_name, variable_name):
        """Get the value of a variable from the dynamic store."""
        with cls.lock:
            return _DynamicStoreHandler._get_variable(config_name, variable_name)

    @classmethod
    def _delete_variable(cls, config_name, variable_name):
        """Delete a variable from the dynamic store."""
        with cls.lock:
            _DynamicStoreHandler._delete_variable(config_name, variable_name)

    @classmethod
    def _delete_variables(cls, config_name, variable_names):
        """Delete multiple variables from the dynamic store."""
        with cls.lock:
            _DynamicStoreHandler._delete_variables(config_name, variable_names)

    @classmethod
    def _clear_dynamic_store(cls, config_name):
        """Clear the dynamic store."""
        with cls.lock:
            _DynamicStoreHandler._clear_dynamic_store(config_name)

    @classmethod
    def _get_dynamic_store_keys(cls, config_name):
        """Get the keys of the dynamic store."""
        with cls.lock:
            return _DynamicStoreHandler._get_dynamic_store_keys(config_name)

    # helper methods
    @classmethod
    def _convert_value(cls, value, direction="create"):
        handler = cls.custom_type_handlers.get(type(value))
        if handler:
            return handler.create(value) if direction == "create" else handler.save(value)
        return value

    @classmethod
    def _unpack_value_pack(cls, value_pack):
        """Unpack a value pack."""
        if isinstance(value_pack, tuple) and len(value_pack) == 2:
            return value_pack
        else:
            return value_pack, None

    @classmethod
    def _debug(cls, message):
        """Log a debug message."""
        Logger.debug(message, logger_name=FRAMEWORK_NAME, module_name=_ConfigHandlerCore.__name__)

    @classmethod
    def _warning(cls, message):
        """Log a warning message."""
        Logger.warning(message, logger_name=FRAMEWORK_NAME, module_name=_ConfigHandlerCore.__name__)

    @classmethod
    def _error(cls, message):
        """Log an error message."""
        Logger.error(message, logger_name=FRAMEWORK_NAME, module_name=_ConfigHandlerCore.__name__)
