# GuiFramework/utilities/config/config_handler.py

from typing import Any, Dict, Optional, List, Type, Union, Tuple

from .private._config_handler import _ConfigHandler, ConfigFileHandlerConfig, CustomTypeHandlerBase, ConfigVariable


class ConfigHandler:
    """Public interface for the ConfigHandler class."""

    @staticmethod
    def add_config(config_name: str, handler_config: ConfigFileHandlerConfig, default_config: Optional[Dict[str, Dict[str, str]]] = None, custom_type_handlers: Optional[Dict[type, CustomTypeHandlerBase]] = None) -> None:
        """Register a new configuration."""
        _ConfigHandler._add_config(config_name, handler_config, default_config, custom_type_handlers)

    @staticmethod
    def add_custom_type_handler(config_name: str, handler: CustomTypeHandlerBase) -> None:
        """Register a custom type handler."""
        _ConfigHandler._add_custom_type_handler(config_name, handler)

    @staticmethod
    def add_custom_type_handlers(config_name: str, handlers: Dict[type, CustomTypeHandlerBase]) -> None:
        """Register multiple custom type handlers."""
        _ConfigHandler._add_custom_type_handlers(config_name, handlers)

    @staticmethod
    def get_custom_config(config_name: str) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire custom configuration."""
        return _ConfigHandler._get_custom_config(config_name)

    @staticmethod
    def get_default_config(config_name: str) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire default configuration."""
        return _ConfigHandler._get_default_config(config_name)

    @staticmethod
    def save_custom_config_to_file(config_name: str) -> None:
        """Save the custom configuration to file."""
        _ConfigHandler._save_custom_config_to_file(config_name)

    @staticmethod
    def load_custom_config_from_file(config_name: str) -> None:
        """Load the custom configuration from file."""
        _ConfigHandler._load_custom_config_from_file(config_name)

    @staticmethod
    def sync_default_config(config_name: str) -> None:
        """Synchronize the default configuration."""
        _ConfigHandler._sync_default_config(config_name)

    @staticmethod
    def sync_custom_config(config_name: str) -> None:
        """Synchronize the custom configuration."""
        _ConfigHandler._sync_custom_config(config_name)

    @staticmethod
    def reset_custom_config(config_name: str, auto_save: bool = True) -> None:
        """Reset the entire custom configuration to default values."""
        _ConfigHandler._reset_custom_config(config_name, auto_save)

    @staticmethod
    def save_setting(config_name: str, section: str, option: str, value: Any, auto_save: bool = True) -> None:
        """Save a single setting."""
        _ConfigHandler._save_setting(config_name, section, option, value, auto_save)

    @staticmethod
    def save_settings(config_name: str, settings: Dict[str, Any], auto_save: bool = True) -> None:
        """Save multiple settings."""
        _ConfigHandler._save_settings(config_name, settings, auto_save)

    @staticmethod
    def get_setting(config_name: str, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False, type_to_convert: Optional[Type] = None) -> Any:
        """Retrieve a single setting."""
        return _ConfigHandler._get_setting(config_name, section, option, fallback_value, force_default, type_to_convert)

    @staticmethod
    def get_settings(config_name: str, settings: Dict[str, Dict[str, Any]], force_default: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieve multiple settings."""
        return _ConfigHandler._get_settings(config_name, settings, force_default)

    @staticmethod
    def reset_setting(config_name: str, section: str, option: str, auto_save: bool = True) -> None:
        """Reset a single setting to its default value."""
        _ConfigHandler._reset_setting(config_name, section, option, auto_save)

    @staticmethod
    def reset_section(config_name: str, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        """Reset an entire section to its default values."""
        _ConfigHandler._reset_section(config_name, settings, auto_save)

    @staticmethod
    def add_variable(config_name: str, variable: ConfigVariable, auto_save: bool = True) -> None:
        """Add a variable to the dynamic store."""
        _ConfigHandler._add_variable(config_name, variable, auto_save)

    @staticmethod
    def add_variables(config_name: str, variables: List[ConfigVariable]) -> None:
        """Add multiple variables to the dynamic store."""
        _ConfigHandler._add_variables(config_name, variables)

    @staticmethod
    def set_variable(config_name: str, updated_variable: ConfigVariable) -> None:
        """Set the value of a variable."""
        _ConfigHandler._set_variable(config_name, updated_variable)

    @staticmethod
    def set_variables(config_name: str, updated_variables: List[ConfigVariable]) -> None:
        """Set multiple variables."""
        _ConfigHandler._set_variables(config_name, updated_variables)

    @staticmethod
    def get_variable(config_name: str, variable_name: str, section: Optional[str] = None) -> Optional[ConfigVariable]:
        """Retrieve the value of a variable."""
        return _ConfigHandler._get_variable(config_name, variable_name, section)

    @staticmethod
    def get_variables(config_name: str, variables: List[Union[str, Tuple[str, str]]]) -> Dict[str, Dict[str, Optional[ConfigVariable]]]:
        """Retrieve all variables."""
        return _ConfigHandler._get_variables(config_name, variables)

    @staticmethod
    def delete_variable(config_name: str, variable_name: str, section: Optional[str] = None) -> None:
        """Delete a variable."""
        _ConfigHandler._delete_variable(config_name, variable_name, section)

    @staticmethod
    def delete_variables(config_name: str, variables: List[Union[str, Tuple[str, str]]]) -> None:
        """Delete multiple variables."""
        _ConfigHandler._delete_variables(config_name, variables)
