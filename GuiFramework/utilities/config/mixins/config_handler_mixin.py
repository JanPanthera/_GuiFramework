# GuiFramework/utilities/config/mixins/config_handler_mixin.py

from typing import Dict, Optional, Any, List

from GuiFramework.utilities.config import ConfigHandler, ConfigFileHandlerConfig, CustomTypeHandlerBase


class ConfigHandlerMixin:
    """Mixin for simplified ConfigHandler method calls."""

    def __init__(self, config_name: str, handler_config: ConfigFileHandlerConfig, custom_type_handlers: Optional[Dict[str, CustomTypeHandlerBase]] = None) -> None:
        """Initialize with configuration name, handler configuration, and optional custom type handlers."""
        if not config_name:
            raise ValueError("config_name cannot be empty")
        self.config_name: str = config_name
        ConfigHandler.add_config(self.config_name, handler_config, custom_type_handlers)

    def sync_default_config(self) -> None:
        """Synchronize default configuration from file."""
        ConfigHandler.sync_default_config(self.config_name)

    def sync_custom_config(self) -> None:
        """Synchronize custom configuration from file."""
        ConfigHandler.sync_custom_config(self.config_name)

    def add_custom_type_handler(self, type_: str, handler: CustomTypeHandlerBase) -> None:
        """Register a custom type handler for configuration values."""
        ConfigHandler.add_custom_type_handler(self.config_name, type_, handler)

    def add_custom_type_handlers(self, handlers: Dict[str, CustomTypeHandlerBase]) -> None:
        """Register multiple custom type handlers for configuration values."""
        ConfigHandler.add_custom_type_handlers(self.config_name, handlers)

    def save_setting(self, section: str, option: str, value: Any, auto_save: bool = True, skip_custom_type_handler: bool = False) -> None:
        """Save a single setting to the configuration."""
        ConfigHandler.save_setting(self.config_name, section, option, value, auto_save, skip_custom_type_handler)

    def save_settings(self, settings: Dict[str, Dict[str, Any]], auto_save: bool = True, skip_custom_type_handler: bool = False) -> None:
        """Save multiple settings to the configuration."""
        ConfigHandler.save_settings(self.config_name, settings, auto_save, skip_custom_type_handler)

    def get_setting(self, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False, skip_custom_type_handler: bool = False) -> Any:
        """Retrieve a single setting from the configuration."""
        return ConfigHandler.get_setting(self.config_name, section, option, fallback_value, force_default, skip_custom_type_handler)

    def get_settings(self, settings: Dict[str, Dict[str, Any]], force_default: bool = False, skip_custom_type_handler: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieve multiple settings from the configuration."""
        return ConfigHandler.get_settings(self.config_name, settings, force_default, skip_custom_type_handler)

    def get_config(self, apply_custom_type_handlers: bool = True) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire configuration."""
        return ConfigHandler.get_config(self.config_name, apply_custom_type_handlers)

    def reset_setting(self, section: str, option: str, auto_save: bool = True) -> None:
        """Reset a single setting to its default value."""
        ConfigHandler.reset_setting(self.config_name, section, option, auto_save)

    def reset_section(self, section: str, auto_save: bool = True) -> None:
        """Reset an entire section to its default values."""
        ConfigHandler.reset_section(self.config_name, section, auto_save)

    def reset_config(self, auto_save: bool = True) -> None:
        """Reset the entire configuration to default values."""
        ConfigHandler.reset_config(self.config_name, auto_save)

    def save_custom_config_to_file(self) -> None:
        """Save the custom configuration to file."""
        ConfigHandler.save_custom_config_to_file(self.config_name)

    def load_custom_config_from_file(self) -> None:
        """Load the custom configuration from file."""
        ConfigHandler.load_custom_config_from_file(self.config_name)

    def add_variable(self, variable_name: str, value: Any, section: Optional[str] = None) -> None:
        """Add a variable to the dynamic store."""
        ConfigHandler.add_variable(self.config_name, variable_name, value, section)

    def add_variables(self, variables: Dict[str, Any]) -> None:
        """Add multiple variables to the dynamic store."""
        ConfigHandler.add_variables(self.config_name, variables)

    def set_variable(self, variable_name: str, value: Any, save_override: bool = False) -> None:
        """Set the value of a variable in the dynamic store."""
        ConfigHandler.set_variable(self.config_name, variable_name, value, save_override)

    def set_variables(self, variables: Dict[str, Any]) -> None:
        """Set multiple variables in the dynamic store."""
        ConfigHandler.set_variables(self.config_name, variables)

    def get_variable(self, variable_name: str) -> Any:
        """Retrieve the value of a variable from the dynamic store."""
        return ConfigHandler.get_variable(self.config_name, variable_name)

    def delete_variable(self, variable_name: str) -> None:
        """Delete a variable from the dynamic store."""
        ConfigHandler.delete_variable(self.config_name, variable_name)

    def delete_variables(self, variable_names: List[str]) -> None:
        """Delete multiple variables from the dynamic store."""
        ConfigHandler.delete_variables(self.config_name, variable_names)

    def clear_dynamic_store(self) -> None:
        """Clear all variables from the dynamic store."""
        ConfigHandler.clear_dynamic_store(self.config_name)

    def get_dynamic_store_keys(self) -> List[str]:
        """Retrieve all variable names from the dynamic store."""
        return ConfigHandler.get_dynamic_store_keys(self.config_name)
