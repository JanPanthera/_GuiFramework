# GuiFramework/utilities/config/mixins/config_handler_mixin.py

from typing import Dict, Optional, Any, List, Union, Tuple, Type

from GuiFramework.utilities.config.config_handler import ConfigHandler, ConfigFileHandlerConfig, CustomTypeHandlerBase, ConfigVariable


class ConfigHandlerMixin:
    """Mixin for simplified ConfigHandler method calls."""

    def __init__(self, config_name: str, handler_config: ConfigFileHandlerConfig, default_config: Optional[Dict[str, Dict[str, str]]] = None, custom_type_handlers: Optional[Dict[type, CustomTypeHandlerBase]] = None) -> None:
        """Initialize with configuration name and handler configuration."""
        if not config_name:
            raise ValueError("config_name cannot be empty")
        self.config_name: str = config_name
        ConfigHandler.add_config(self.config_name, handler_config, default_config, custom_type_handlers)

    def add_custom_type_handler(self, handler: CustomTypeHandlerBase) -> None:
        """Register a custom type handler."""
        ConfigHandler.add_custom_type_handler(self.config_name, handler)

    def add_custom_type_handlers(self, handlers: Dict[type, CustomTypeHandlerBase]) -> None:
        """Register multiple custom type handlers."""
        ConfigHandler.add_custom_type_handlers(self.config_name, handlers)

    def get_custom_config(self) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire custom configuration."""
        return ConfigHandler.get_custom_config(self.config_name)

    def get_default_config(self) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire default configuration."""
        return ConfigHandler.get_default_config(self.config_name)

    def save_custom_config_to_file(self) -> None:
        """Save the custom configuration to file."""
        ConfigHandler.save_custom_config_to_file(self.config_name)

    def load_custom_config_from_file(self) -> None:
        """Load the custom configuration from file."""
        ConfigHandler.load_custom_config_from_file(self.config_name)

    def sync_default_config(self) -> None:
        """Synchronize the default configuration."""
        ConfigHandler.sync_default_config(self.config_name)

    def sync_custom_config(self) -> None:
        """Synchronize the custom configuration."""
        ConfigHandler.sync_custom_config(self.config_name)

    def reset_custom_config(self, auto_save: bool = True) -> None:
        """Reset the entire custom configuration to default values."""
        ConfigHandler.reset_custom_config(self.config_name, auto_save)

    def save_setting(self, section: str, option: str, value: Any, auto_save: bool = True) -> None:
        """Save a single setting."""
        ConfigHandler.save_setting(self.config_name, section, option, value, auto_save)

    def save_settings(self, settings: Dict[str, Any], auto_save: bool = True) -> None:
        """Save multiple settings."""
        ConfigHandler.save_settings(self.config_name, settings, auto_save)

    def get_setting(self, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False, type_to_convert: Optional[Type] = None) -> Any:
        """Retrieve a single setting."""
        return ConfigHandler.get_setting(self.config_name, section, option, fallback_value, force_default, type_to_convert)

    def get_settings(self, settings: Dict[str, Dict[str, Any]], force_default: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieve multiple settings."""
        return ConfigHandler.get_settings(self.config_name, settings, force_default)

    def reset_setting(self, section: str, option: str, auto_save: bool = True) -> None:
        """Reset a single setting to its default value."""
        ConfigHandler.reset_setting(self.config_name, section, option, auto_save)

    def reset_section(self, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        """Reset an entire section to its default values."""
        ConfigHandler.reset_section(self.config_name, settings, auto_save)

    def add_variable(self, variable: ConfigVariable, auto_save: bool = True) -> None:
        """Add a variable to the dynamic store."""
        ConfigHandler.add_variable(self.config_name, variable, auto_save)

    def add_variables(self, variables: List[ConfigVariable], auto_save: bool = True) -> None:
        """Add multiple variables to the dynamic store."""
        ConfigHandler.add_variables(self.config_name, variables, auto_save)

    def set_variable(self, updated_variable: ConfigVariable, auto_save: bool = True) -> None:
        """Set the value of a variable."""
        ConfigHandler.set_variable(self.config_name, updated_variable, auto_save)

    def set_variables(self, updated_variables: List[ConfigVariable], auto_save: bool = True) -> None:
        """Set multiple variables."""
        ConfigHandler.set_variables(self.config_name, updated_variables, auto_save)

    def get_variable(self, variable_name: str, section: Optional[str] = None) -> Optional[ConfigVariable]:
        """Retrieve the value of a variable."""
        return ConfigHandler.get_variable(self.config_name, variable_name, section)

    def get_variables(self, variables: List[Union[str, Tuple[str, str]]]) -> Dict[str, Dict[str, Optional[ConfigVariable]]]:
        """Retrieve all variables."""
        return ConfigHandler.get_variables(self.config_name, variables)

    def delete_variable(self, variable_name: str, section: Optional[str] = None) -> None:
        """Delete a variable."""
        ConfigHandler.delete_variable(self.config_name, variable_name, section)

    def delete_variables(self, variables: List[Union[str, Tuple[str, str]]]) -> None:
        """Delete multiple variables."""
        ConfigHandler.delete_variables(self.config_name, variables)
