# GuiFramework/utilities/config/private/_config_handler.py
# ATTENTION: This module is for internal use only

from typing import Any, Dict, Optional
from threading import RLock

from GuiFramework.utilities.config.custom_type_handler_base import CustomTypeHandlerBase
from ._config_file_handler import _ConfigFileHandler, ConfigFileHandlerConfig
from ._config_dynamic_store import _ConfigDynamicStore

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import StaticLoggerMixin


class _ConfigHandler(StaticLoggerMixin):
    """Core class for the configuration handler."""
    custom_type_handlers: Dict[str, CustomTypeHandlerBase] = {}
    lock = RLock()

    StaticLoggerMixin.set_logger_details(FRAMEWORK_NAME, "_ConfigHandler")

    @classmethod
    def _add_config(cls, config_name: str, handler_config: ConfigFileHandlerConfig, custom_type_handlers: Optional[Dict[str, CustomTypeHandlerBase]] = None):
        """Add a configuration."""
        with cls.lock:
            _ConfigFileHandler.add_config(config_name, handler_config)
            _ConfigDynamicStore.add_store(config_name)
            if custom_type_handlers is not None:
                cls._add_custom_type_handlers(custom_type_handlers)

    @classmethod
    def _sync_default_config(cls, config_name: str):
        """Sync the default config with the default config file."""
        with cls.lock:
            _ConfigFileHandler.sync_config(config_name, "default")

    @classmethod
    def _sync_custom_config(cls, config_name: str):
        """Sync the custom config with the custom config file."""
        with cls.lock:
            _ConfigFileHandler.sync_config(config_name, "custom")

    @classmethod
    def _add_custom_type_handler(cls, type_: str, handler: CustomTypeHandlerBase):
        """Add a custom type handler."""
        if not issubclass(handler, CustomTypeHandlerBase):
            cls._log_warning("_add_custom_type_handler", f"Failed to add custom type handler: {handler} is not a subclass of CustomTypeHandlerBase.")
            return
        with cls.lock:
            cls.custom_type_handlers[type_] = handler

    @classmethod
    def _add_custom_type_handlers(cls, handlers: Dict[str, CustomTypeHandlerBase]):
        """Add custom type handlers."""
        with cls.lock:
            for type_, handler in handlers.items():
                if issubclass(handler, CustomTypeHandlerBase):
                    cls.custom_type_handlers[type_] = handler
                else:
                    cls._log_warning("_add_custom_type_handlers", f"Handler for type {type_} is not a subclass of CustomTypeHandlerBase.")

    @classmethod
    def _save_setting(cls, config_name: str, section: str, option: str, value: Any, auto_save: bool = True, skip_custom_type_handler: bool = False) -> None:
        """Save a setting to a configuration file."""
        with cls.lock:
            if not skip_custom_type_handler:
                value = cls._convert_value(value, "serialize")
            _ConfigFileHandler._save_setting(config_name, section, option, value, auto_save)

    @classmethod
    def _save_settings(cls, config_name: str, settings: Dict[str, Any], auto_save: bool = True, skip_custom_type_handler: bool = False) -> None:
        """Save settings to a configuration file."""
        with cls.lock:
            for section, options in settings.items():
                for option, value in options.items():
                    cls._save_setting(config_name, section, option, value, auto_save, skip_custom_type_handler)

    @classmethod
    def _get_setting(cls, config_name: str, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False, skip_custom_type_handler: bool = False) -> Any:
        """Retrieve a setting from a configuration file."""
        with cls.lock:
            value = _ConfigFileHandler._get_setting(config_name, section, option, fallback_value, force_default)
            return cls._convert_value(value, "deserialize") if not skip_custom_type_handler else value

    @classmethod
    def _get_settings(cls, config_name: str, settings: Dict[str, Dict[str, Any]], force_default: bool = False, skip_custom_type_handler: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieve multiple settings from a configuration file."""
        with cls.lock:
            retrieved_settings = {}
            config_settings = _ConfigFileHandler._get_settings(config_name, settings, force_default)
            for section, options in config_settings.items():
                retrieved_settings[section] = {option: cls._get_setting(config_name, section, option, value, force_default, skip_custom_type_handler) for option, value in options.items()}
            return retrieved_settings

    @classmethod
    def _get_config(cls, config_name: str, apply_custom_type_handlers: bool = True) -> Dict[str, Dict[str, str]]:
        """Get the configuration data."""
        with cls.lock:
            config = _ConfigFileHandler._get_config(config_name)
            if apply_custom_type_handlers:
                for section, options in config.items():
                    config[section] = {option: cls._convert_value(value, "deserialize") for option, value in options.items()}
            return config

    @classmethod
    def _reset_setting(cls, config_name: str, section: str, option: str, auto_save: bool = True) -> None:
        """Reset a setting in a configuration file."""
        with cls.lock:
            _ConfigFileHandler._reset_setting(config_name, section, option, auto_save)

    @classmethod
    def _reset_section(cls, config_name: str, section: str, auto_save: bool = True) -> None:
        """Reset a section in a configuration file."""
        with cls.lock:
            _ConfigFileHandler._reset_section(config_name, section, auto_save)

    @classmethod
    def _reset_config(cls, config_name: str, auto_save: bool = True) -> None:
        """Reset a configuration file."""
        with cls.lock:
            _ConfigFileHandler._reset_config(config_name, auto_save)

    @classmethod
    def _save_custom_config_to_file(cls, config_name: str) -> None:
        """Save the custom config to the custom config file."""
        with cls.lock:
            _ConfigFileHandler._save_custom_config_to_file(config_name)

    @classmethod
    def _load_custom_config_from_file(cls, config_name: str) -> None:
        """Load the custom config from the custom config file."""
        with cls.lock:
            _ConfigFileHandler._load_custom_config_from_file(config_name)

    @classmethod
    def _add_variable(cls, config_name, variable_name, value, section=None):
        """Add a variable to the dynamic store."""
        if value is None:
            cls._log_warning("_add_variable", f"Failed to add variable \"{variable_name}\" to dynamic store: Value cannot be None.")
            return
        with cls.lock:
            if section:
                value_from_file = _ConfigFileHandler._get_setting(config_name, section, variable_name)
                if value_from_file is not None:
                    value = cls._convert_value(value_from_file, "deserialize")
                else:
                    _ConfigFileHandler._save_setting(config_name, section, variable_name, cls._convert_value(value, "serialize"))
            _ConfigDynamicStore._add_variable(config_name, variable_name, value, section)

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
            _ConfigDynamicStore._set_variable(config_name, variable_name, value)
            section = _ConfigDynamicStore._get_variable_section(config_name, variable_name)
            if section and not save_override:
                _ConfigFileHandler._save_setting(config_name, section, variable_name, cls._convert_value(value, "serialize"))

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
            return _ConfigDynamicStore._get_variable(config_name, variable_name)

    @classmethod
    def _delete_variable(cls, config_name, variable_name):
        """Delete a variable from the dynamic store."""
        with cls.lock:
            _ConfigDynamicStore._delete_variable(config_name, variable_name)

    @classmethod
    def _delete_variables(cls, config_name, variable_names):
        """Delete multiple variables from the dynamic store."""
        with cls.lock:
            _ConfigDynamicStore._delete_variables(config_name, variable_names)

    @classmethod
    def _clear_dynamic_store(cls, config_name):
        """Clear the dynamic store."""
        with cls.lock:
            _ConfigDynamicStore._clear_dynamic_store(config_name)

    @classmethod
    def _get_dynamic_store_keys(cls, config_name):
        """Get the keys of the dynamic store."""
        with cls.lock:
            return _ConfigDynamicStore._get_dynamic_store_keys(config_name)

    @classmethod
    def _convert_value(cls, value, direction="serialize"):
        handler = cls.custom_type_handlers.get(type(value))
        if handler:
            return handler.serialize(value) if direction == "serialize" else handler.deserialize(value)
        return value

    @classmethod
    def _unpack_value_pack(cls, value_pack):
        """Unpack a value pack."""
        if isinstance(value_pack, tuple) and len(value_pack) == 2:
            return value_pack
        else:
            return value_pack, None
