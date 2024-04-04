# GuiFramework/utilities/config/config_handler.py

from typing import Any, Dict, Optional, List, Type, Union, Tuple

from .internal._config_handler import _ConfigHandler, ConfigFileHandlerConfig, CustomTypeHandlerBase, ConfigVariable
from .config_types import ConfigKey


class ConfigHandler:
    """Public interface for the ConfigHandler class."""

    @staticmethod
    def add_config(config_name: str, handler_config: ConfigFileHandlerConfig, default_config: Optional[List[CustomTypeHandlerBase]] = None, custom_type_handlers: Optional[Dict[type, CustomTypeHandlerBase]] = None) -> None:
        """Add a new configuration."""
        _ConfigHandler._add_config(config_name, handler_config, default_config, custom_type_handlers)

    @staticmethod
    def get_custom_config(config_name: str) -> Dict[str, Dict[str, str]]:
        """Retrieve custom configuration."""
        return _ConfigHandler._get_custom_config(config_name)

    @staticmethod
    def get_default_config(config_name: str) -> Dict[str, Dict[str, str]]:
        """Retrieve default configuration."""
        return _ConfigHandler._get_default_config(config_name)

    @staticmethod
    def save_custom_config_to_file(config_name: str) -> None:
        """Save custom configuration to file."""
        _ConfigHandler._save_custom_config_to_file(config_name)

    @staticmethod
    def load_custom_config_from_file(config_name: str) -> None:
        """Load custom configuration from file."""
        _ConfigHandler._load_custom_config_from_file(config_name)

    @staticmethod
    def sync_custom_config(config_name: str) -> None:
        """Synchronize custom configuration."""
        _ConfigHandler._sync_custom_config(config_name)

    @staticmethod
    def sync_default_config(config_name: str) -> None:
        """Synchronize default configuration."""
        _ConfigHandler._sync_default_config(config_name)

    @staticmethod
    def reset_custom_config(config_name: str, auto_save: bool = True) -> None:
        """Reset custom configuration to default."""
        _ConfigHandler._reset_custom_config(config_name, auto_save)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def save_setting(config_key: ConfigKey, value: Any) -> None:
        """Save a single setting."""
        _ConfigHandler._save_setting(config_key, value)

    @staticmethod
    def save_settings(config_keys: List[Tuple[ConfigKey, Any]]) -> None:
        """Save multiple settings."""
        _ConfigHandler._save_settings(config_keys)

    @staticmethod
    def get_setting(config_key: ConfigKey, fallback_value: Any = None, force_default: bool = False) -> Any:
        """Retrieve a single setting."""
        return _ConfigHandler._get_setting(config_key, fallback_value, force_default)

    @staticmethod
    def get_settings(config_keys: List[Dict[str, Union[ConfigKey, Any, bool]]]) -> Dict[str, Dict[str, Any]]:
        """Retrieve multiple settings."""
        return _ConfigHandler._get_settings(config_keys)

    @staticmethod
    def reset_setting(config_key: ConfigKey, auto_save: bool = None) -> None:
        """Reset a single setting to default."""
        _ConfigHandler._reset_setting(config_key, auto_save)

    @staticmethod
    def reset_settings(config_keys: List[ConfigKey]) -> None:
        """Reset multiple settings to default."""
        _ConfigHandler._reset_settings(config_keys)

    @staticmethod
    def reset_section(config_name: str, section: str, auto_save: bool = True) -> None:
        """Reset an entire section to default."""
        _ConfigHandler._reset_section(config_name, section, auto_save)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def add_variable(config_key: ConfigKey, value: Any, default_value: Any, init_from_file: bool = False) -> None:
        """Add a new variable."""
        _ConfigHandler._add_variable(config_key, value, default_value, init_from_file)

    @staticmethod
    def add_variables(variables: List[Union[ConfigVariable, Tuple[ConfigVariable, bool]]]) -> None:
        """Add multiple new variables."""
        _ConfigHandler._add_variables(variables)

    @staticmethod
    def get_variable(config_key: ConfigKey) -> ConfigVariable:
        """Retrieve a single variable."""
        return _ConfigHandler._get_variable(config_key)

    @staticmethod
    def get_variables(config_keys: List[ConfigKey]) -> List[ConfigVariable]:
        """Retrieve multiple variables."""
        return _ConfigHandler._get_variables(config_keys)

    @staticmethod
    def get_variable_value(config_key: ConfigKey) -> Any:
        """Get the value of a single variable."""
        return _ConfigHandler._get_variable_value(config_key)

    @staticmethod
    def get_variable_values(config_keys: List[ConfigKey]) -> List[Any]:
        """Get the values of multiple variables."""
        return _ConfigHandler._get_variable_values(config_keys)

    @staticmethod
    def set_variable(updated_variable: ConfigVariable) -> None:
        """Set a single variable."""
        _ConfigHandler._set_variable(updated_variable)

    @staticmethod
    def set_variables(updated_variables: List[ConfigVariable]) -> None:
        """Set multiple variables."""
        _ConfigHandler._set_variables(updated_variables)

    @staticmethod
    def set_variable_value(config_key: ConfigKey, new_value: Any) -> None:
        """Set the value of a single variable."""
        _ConfigHandler._set_variable_value(config_key, new_value)

    @staticmethod
    def set_variable_values(config_keys: List[Tuple[ConfigKey, Any]]) -> None:
        """Set the values of multiple variables."""
        _ConfigHandler._set_variable_values(config_keys)

    @staticmethod
    def delete_variable(config_key: ConfigKey) -> None:
        """Delete a single variable."""
        _ConfigHandler._delete_variable(config_key)

    @staticmethod
    def delete_variables(config_keys: List[ConfigKey]) -> None:
        """Delete multiple variables."""
        _ConfigHandler._delete_variables(config_keys)
