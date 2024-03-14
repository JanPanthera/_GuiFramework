# GuiFramework/utilities/config/mixins/config_file_handler_mixin.py

from typing import Any, Dict, Optional

from GuiFramework.utilities.config import ConfigFileHandler, ConfigFileHandlerConfig


class ConfigFileHandlerMixin:
    """Mixin for ConfigFileHandler method abstraction."""

    def __init__(self, config_name: str, config_file_handler: ConfigFileHandler) -> None:
        """Initialize with config name and handler."""
        if not config_name:
            raise ValueError("config_name cannot be empty")
        self.config_name: str = config_name
        ConfigFileHandler.add_config(self.config_name, config_file_handler)

    def sync_default_config(self) -> None:
        """Synchronize default configuration."""
        ConfigFileHandler.sync_default_config(self.config_name)

    def sync_custom_config(self) -> None:
        """Synchronize custom configuration."""
        ConfigFileHandler.sync_custom_config(self.config_name)

    def save_setting(self, section: str, option: str, value: Any, auto_save: bool = True) -> None:
        """Save a single setting."""
        ConfigFileHandler.save_setting(self.config_name, section, option, value, auto_save)

    def save_settings(self, settings: Dict[str, Dict[str, Any]], auto_save: bool = True) -> None:
        """Save multiple settings."""
        ConfigFileHandler.save_settings(self.config_name, settings, auto_save)

    def get_setting(self, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False) -> Any:
        """Retrieve a single setting."""
        return ConfigFileHandler.get_setting(self.config_name, section, option, fallback_value, force_default)

    def get_settings(self, settings: Dict[str, Dict[str, Any]], force_default: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieve multiple settings."""
        return ConfigFileHandler.get_settings(self.config_name, settings, force_default)

    def get_config(self) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire configuration."""
        return ConfigFileHandler.get_config(self.config_name)

    def reset_setting(self, section: str, option: str, auto_save: bool = True) -> None:
        """Reset a single setting to default."""
        ConfigFileHandler.reset_setting(self.config_name, section, option, auto_save)

    def reset_section(self, section: str, auto_save: bool = True) -> None:
        """Reset an entire section to defaults."""
        ConfigFileHandler.reset_section(self.config_name, section, auto_save)

    def reset_config(self, auto_save: bool = True) -> None:
        """Reset entire configuration to defaults."""
        ConfigFileHandler.reset_config(self.config_name, auto_save)

    def save_custom_config_to_file(self) -> None:
        """Save custom configuration to file."""
        ConfigFileHandler.save_custom_config_to_file(self.config_name)

    def load_custom_config_from_file(self) -> None:
        """Load custom configuration from file."""
        ConfigFileHandler.load_custom_config_from_file(self.config_name)
