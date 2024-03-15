# GuiFramework/utilities/config/mixins/config_file_handler_mixin.py

from typing import Dict, List, Optional

from GuiFramework.utilities.config.config_file_handler import ConfigFileHandler, ConfigFileHandlerConfig


class ConfigFileHandlerMixin:
    """Mixin for ConfigFileHandler method abstraction."""

    def __init__(self, config_name: str, handler_config: ConfigFileHandlerConfig, default_config: Optional[Dict[str, Dict[str, str]]] = None) -> None:
        """Initialize with config name and handler."""
        self.config_name: str = config_name
        ConfigFileHandler.add_config(self.config_name, handler_config, default_config)

    def get_custom_config(self) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire configuration."""
        return ConfigFileHandler.get_custom_config(self.config_name)

    def get_default_config(self) -> Dict[str, Dict[str, str]]:
        """Retrieve the entire default configuration."""
        return ConfigFileHandler.get_default_config(self.config_name)

    def save_custom_config_to_file(self) -> None:
        """Save custom configuration to file."""
        ConfigFileHandler.save_custom_config_to_file(self.config_name)

    def load_custom_config_from_file(self) -> None:
        """Load custom configuration from file."""
        ConfigFileHandler.load_custom_config_from_file(self.config_name)

    def sync_custom_config(self) -> None:
        """Synchronize custom configuration."""
        ConfigFileHandler.sync_custom_config(self.config_name)

    def sync_default_config(self) -> None:
        """Synchronize default configuration."""
        ConfigFileHandler.sync_default_config(self.config_name)

    def reset_custom_config(self, auto_save: bool = True) -> None:
        """Reset entire custom configuration to defaults."""
        ConfigFileHandler.reset_custom_config(self.config_name, auto_save)

    def save_setting(self, section: str, option: str, value: str, auto_save: bool = True) -> None:
        """Save a single setting."""
        ConfigFileHandler.save_setting(self.config_name, section, option, value, auto_save)

    def save_settings(self, settings: Dict[str, Dict[str, str]], auto_save: bool = True) -> None:
        """Save multiple settings."""
        ConfigFileHandler.save_settings(self.config_name, settings, auto_save)

    def get_setting(self, section: str, option: str, fallback_value: Optional[str] = None, force_default: bool = False) -> str:
        """Retrieve a single setting."""
        return ConfigFileHandler.get_setting(self.config_name, section, option, fallback_value, force_default)

    def get_settings(self, settings: Dict[str, Dict[str, str]], force_default: bool = False) -> Dict[str, Dict[str, str]]:
        """Retrieve multiple settings."""
        return ConfigFileHandler.get_settings(self.config_name, settings, force_default)

    def reset_setting(self, section: str, option: str, auto_save: bool = True) -> None:
        """Reset a single setting to default."""
        ConfigFileHandler.reset_setting(self.config_name, section, option, auto_save)

    def reset_settings(self, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        """Reset multiple settings to default."""
        ConfigFileHandler.reset_settings(self.config_name, settings, auto_save)

    def reset_section(self, section: str, auto_save: bool = True) -> None:
        """Reset an entire section to defaults."""
        ConfigFileHandler.reset_section(self.config_name, section, auto_save)
