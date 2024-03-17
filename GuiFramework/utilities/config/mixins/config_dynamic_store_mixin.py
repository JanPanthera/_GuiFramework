# GuiFramework/utilities/config/mixins/config_dynamic_store_mixin.py

from typing import Any, Dict, List, Optional

from GuiFramework.utilities.config.config_dynamic_store import ConfigDynamicStore


class ConfigDynamicStoreMixin:
    """Mixin for simplified ConfigDynamicStore method calls."""

    def __init__(self, config_name: str) -> None:
        """Initialize mixin with a non-empty config name."""
        if not config_name:
            raise ValueError("config_name cannot be empty")
        self.config_name: str = config_name
        ConfigDynamicStore.add_store(self.config_name)

    def get_store(self) -> Dict[str, Any]:
        """Retrieve the specified dynamic store."""
        return ConfigDynamicStore.get_store(self.config_name)

    def delete_store(self) -> None:
        """Delete the specified dynamic store."""
        ConfigDynamicStore.delete_store(self.config_name)

    def add_variable(self, variable_name: str, value: Any) -> None:
        """Add a variable to the dynamic store."""
        ConfigDynamicStore.add_variable(self.config_name, variable_name, value)

    def add_variables(self, variables: Dict[str, Any]) -> None:
        """Add multiple variables to the dynamic store."""
        ConfigDynamicStore.add_variables(self.config_name, variables)

    def set_variable(self, variable_name: str, value: Any) -> None:
        """Update a variable's value in the dynamic store."""
        ConfigDynamicStore.set_variable(self.config_name, variable_name, value)

    def set_variables(self, variables: Dict[str, Any]) -> None:
        """Update values of multiple variables in the dynamic store."""
        ConfigDynamicStore.set_variables(self.config_name, variables)

    def get_variable(self, variable_name: str) -> Optional[Any]:
        """Retrieve a variable's value from the dynamic store."""
        return ConfigDynamicStore.get_variable(self.config_name, variable_name)

    def delete_variable(self, variable_name: str) -> None:
        """Remove a variable from the dynamic store."""
        ConfigDynamicStore.delete_variable(self.config_name, variable_name)

    def delete_variables(self, variables: List[str]) -> None:
        """Remove multiple variables from the dynamic store."""
        ConfigDynamicStore.delete_variables(self.config_name, variables)

    def clear_dynamic_store(self) -> None:
        """Clear all variables from the dynamic store."""
        ConfigDynamicStore.clear_dynamic_store(self.config_name)

    def get_dynamic_store_keys(self) -> List[str]:
        """Retrieve all variable names within the dynamic store."""
        return ConfigDynamicStore.get_dynamic_store_keys(self.config_name)
