# GuiFramework/utilities/config/config_file_handler.py
# Public interface for the _ConfigFileHandler class

from typing import Any, Dict, Optional

from .private._config_file_handler import _ConfigFileHandler, ConfigFileHandlerConfig


class ConfigFileHandler:
    """Public interface for the ConfigFileHandler class."""

    @staticmethod
    def add_config(config_name: str, handler_config: ConfigFileHandlerConfig) -> None:
        """Registers a new configuration."""
        _ConfigFileHandler._add_config(config_name, handler_config)

    @staticmethod
    def sync_default_config(config_name: str) -> None:
        """Synchronizes the default configuration."""
        _ConfigFileHandler._sync_config(config_name, "default")

    @staticmethod
    def sync_custom_config(config_name: str) -> None:
        """Synchronizes the custom configuration."""
        _ConfigFileHandler._sync_config(config_name, "custom")

    @staticmethod
    def save_setting(config_name: str, section: str, option: str, value: Any, auto_save: bool = True) -> None:
        """Saves a single setting."""
        _ConfigFileHandler._save_setting(config_name, section, option, value, auto_save)

    @staticmethod
    def save_settings(config_name: str, settings: Dict[str, Dict[str, Any]], auto_save: bool = True) -> None:
        """Saves multiple settings."""
        _ConfigFileHandler._save_settings(config_name, settings, auto_save)

    @staticmethod
    def get_setting(config_name: str, section: str, option: str, fallback_value: Optional[Any] = None, force_default: bool = False) -> Any:
        """Retrieves a single setting."""
        return _ConfigFileHandler._get_setting(config_name, section, option, fallback_value, force_default)

    @staticmethod
    def get_settings(config_name: str, settings: Dict[str, Dict[str, Any]], force_default: bool = False) -> Dict[str, Dict[str, Any]]:
        """Retrieves multiple settings."""
        return _ConfigFileHandler._get_settings(config_name, settings, force_default)

    @staticmethod
    def get_config(config_name: str) -> Dict[str, Dict[str, str]]:
        """Retrieves the entire configuration."""
        return _ConfigFileHandler._get_config(config_name)

    @staticmethod
    def reset_setting(config_name: str, section: str, option: str, auto_save: bool = True) -> None:
        """Resets a single setting to its default value."""
        _ConfigFileHandler._reset_setting(config_name, section, option, auto_save)

    @staticmethod
    def reset_section(config_name: str, section: str, auto_save: bool = True) -> None:
        """Resets an entire section to its default values."""
        _ConfigFileHandler._reset_section(config_name, section, auto_save)

    @staticmethod
    def reset_config(config_name: str, auto_save: bool = True) -> None:
        """Resets the entire configuration to default values."""
        _ConfigFileHandler._reset_config(config_name, auto_save)

    @staticmethod
    def save_custom_config_to_file(config_name: str) -> None:
        """Saves the custom configuration to a file."""
        _ConfigFileHandler._save_custom_config_to_file(config_name)

    @staticmethod
    def load_custom_config_from_file(config_name: str) -> None:
        """Loads the custom configuration from a file."""
        _ConfigFileHandler._load_custom_config_from_file(config_name)
