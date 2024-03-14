# GuiFramework/utilities/config/config_dynamic_store.py

from typing import Any, Dict, List, Optional

from .private._config_dynamic_store import _ConfigDynamicStore


class ConfigDynamicStore:
    """Public interface for the ConfigDynamicStore class."""

    @staticmethod
    def add_store(store_name: str) -> None:
        """Add a new dynamic store."""
        _ConfigDynamicStore._add_store(store_name)

    @staticmethod
    def get_store(store_name: str) -> Dict[str, Any]:
        """Retrieve the specified dynamic store."""
        return _ConfigDynamicStore._get_store(store_name)

    @staticmethod
    def delete_store(store_name: str) -> None:
        """Delete a dynamic store."""
        _ConfigDynamicStore._delete_store(store_name)

    @staticmethod
    def add_variable(store_name: str, variable_name: str, value: Any) -> None:
        """Add a variable to a dynamic store."""
        _ConfigDynamicStore._add_variable(store_name, variable_name, value)

    @staticmethod
    def add_variables(store_name: str, variables: Dict[str, Any]) -> None:
        """Add multiple variables to a dynamic store."""
        _ConfigDynamicStore._add_variables(store_name, variables)

    @staticmethod
    def set_variable(store_name: str, variable_name: str, value: Any) -> None:
        """Update a variable's value in a dynamic store."""
        _ConfigDynamicStore._set_variable(store_name, variable_name, value)

    @staticmethod
    def set_variables(store_name: str, variables: Dict[str, Any]) -> None:
        """Update values of multiple variables in a dynamic store."""
        _ConfigDynamicStore._set_variables(store_name, variables)

    @staticmethod
    def get_variable(store_name: str, variable_name: str) -> Optional[Any]:
        """Retrieve a variable's value from a dynamic store."""
        return _ConfigDynamicStore._get_variable(store_name, variable_name)

    @staticmethod
    def delete_variable(store_name: str, variable_name: str) -> None:
        """Remove a variable from a dynamic store."""
        _ConfigDynamicStore._delete_variable(store_name, variable_name)

    @staticmethod
    def delete_variables(store_name: str, variables: List[str]) -> None:
        """Remove multiple variables from a dynamic store."""
        _ConfigDynamicStore._delete_variables(store_name, variables)

    @staticmethod
    def clear_dynamic_store(store_name: str) -> None:
        """Clear all variables from a dynamic store."""
        _ConfigDynamicStore._clear_dynamic_store(store_name)

    @staticmethod
    def get_dynamic_store_keys(store_name: str) -> List[str]:
        """Retrieve all variable names within a dynamic store."""
        return _ConfigDynamicStore._get_dynamic_store_keys(store_name)
