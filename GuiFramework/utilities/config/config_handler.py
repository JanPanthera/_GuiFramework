# GuiFramework/utilities/config/config_handler.py
# Public interface for the _ConfigHandler class

from typing import Any, Dict, Optional, List, Tuple, Union

from .private._config_handler import _ConfigHandler, ConfigFileHandlerConfig, CustomTypeHandlerBase


class ConfigHandler:
    """Public interface for the ConfigHandler class."""

    @staticmethod
    def add_config(config_name: str, handler_config: ConfigFileHandlerConfig, custom_type_handlers: Optional[Dict[str, CustomTypeHandlerBase]] = None) -> None:
        """Registers a new configuration."""
        _ConfigHandler._add_config(config_name, handler_config, custom_type_handlers)

    @staticmethod
    def sync_default_config(config_name: str) -> None:
        """Synchronizes the default configuration."""
        _ConfigHandler._sync_default_config(config_name)

    @staticmethod
    def sync_custom_config(config_name: str) -> None:
        """Synchronizes the custom configuration."""
        _ConfigHandler._sync_custom_config(config_name)

    @staticmethod
    def add_custom_type_handler(config_name: str, type_: str, handler: CustomTypeHandlerBase) -> None:
        """Registers a custom type handler."""
        _ConfigHandler._add_custom_type_handler(config_name, type_, handler)

    @staticmethod
    def add_custom_type_handlers(config_name: str, handlers: Dict[str, CustomTypeHandlerBase]) -> None:
        """Registers multiple custom type handlers."""
        _ConfigHandler._add_custom_type_handlers(config_name, handlers)

    @staticmethod
    def save_setting(config_name: str, section: str, option: str, value: Any, auto_save: bool = True, skip_custom_type_handler: bool = False) -> None:
        """Saves a single setting."""
        _ConfigHandler._save_setting(config_name, section, option, value, auto_save, skip_custom_type_handler)

    @staticmethod
    def save_settings(config_name: str, settings: Dict[str, Dict[str, Any]], auto_save: bool = True, skip_custom_type_handler: bool = False) -> None:
        """Saves multiple settings."""
        _ConfigHandler._save_settings(config_name, settings, auto_save, skip_custom_type_handler)

    @staticmethod
    def get_setting(config_name: str, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False, skip_custom_type_handler: bool = False) -> Any:
        """Retrieves a single setting."""
        return _ConfigHandler._get_setting(config_name, section, option, fallback_value, force_default, skip_custom_type_handler)

    @staticmethod
    def get_settings(config_name: str, settings: Dict[str, Dict[str, Any]], force_default: bool = False, skip_custom_type_handler: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieves multiple settings."""
        return _ConfigHandler._get_settings(config_name, settings, force_default, skip_custom_type_handler)

    @staticmethod
    def get_config(config_name: str, apply_custom_type_handlers: bool = True) -> Dict[str, Dict[str, str]]:
        """Retrieves the entire configuration."""
        return _ConfigHandler._get_config(config_name, apply_custom_type_handlers)

    @staticmethod
    def reset_setting(config_name: str, section: str, option: str, auto_save: bool = True) -> None:
        """Resets a single setting to its default value."""
        _ConfigHandler._reset_setting(config_name, section, option, auto_save)

    @staticmethod
    def reset_section(config_name: str, section: str, auto_save: bool = True) -> None:
        """Resets an entire section to its default values."""
        _ConfigHandler._reset_section(config_name, section, auto_save)

    @staticmethod
    def reset_config(config_name: str, auto_save: bool = True) -> None:
        """Resets the entire configuration to default values."""
        _ConfigHandler._reset_config(config_name, auto_save)

    @staticmethod
    def save_custom_config_to_file(config_name: str) -> None:
        """Saves the custom configuration to file."""
        _ConfigHandler._save_custom_config_to_file(config_name)

    @staticmethod
    def load_custom_config_from_file(config_name: str) -> None:
        """Loads the custom configuration from file."""
        _ConfigHandler._load_custom_config_from_file(config_name)

    @staticmethod
    def add_variable(config_name: str, variable_name: str, value: Any, section: Optional[str] = None) -> None:
        """Adds a variable to the dynamic store."""
        _ConfigHandler._add_variable(config_name, variable_name, value, section)

    @staticmethod
    def add_variables(config_name: str, variables: Dict[str, Any]) -> None:
        """Adds multiple variables to the dynamic store."""
        _ConfigHandler._add_variables(config_name, variables)

    @staticmethod
    def set_variable(config_name: str, variable_name: str, value: Any, save_override: bool = False) -> None:
        """Sets the value of a variable."""
        _ConfigHandler._set_variable(config_name, variable_name, value, save_override)

    @staticmethod
    def set_variables(config_name: str, variables: Dict[str, Any]) -> None:
        """Sets multiple variables."""
        _ConfigHandler._set_variables(config_name, variables)

    @staticmethod
    def get_variable(config_name: str, variable_name: str) -> Any:
        """Retrieves the value of a variable."""
        return _ConfigHandler._get_variable(config_name, variable_name)

    @staticmethod
    def delete_variable(config_name: str, variable_name: str) -> None:
        """Deletes a variable."""
        _ConfigHandler._delete_variable(config_name, variable_name)

    @staticmethod
    def delete_variables(config_name: str, variable_names: List[str]) -> None:
        """Deletes multiple variables."""
        _ConfigHandler._delete_variables(config_name, variable_names)

    @staticmethod
    def clear_dynamic_store(config_name: str) -> None:
        """Clears all variables from the dynamic store."""
        _ConfigHandler._clear_dynamic_store(config_name)

    @staticmethod
    def get_dynamic_store_keys(config_name: str) -> List[str]:
        """Retrieves all variable names from the dynamic store."""
        return _ConfigHandler._get_dynamic_store_keys(config_name)
