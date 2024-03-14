# GuiFramework/utilities/config/config_dynamic_store.py

from typing import Any, Dict
from .private._config_dynamic_store import _ConfigDynamicStore


class ConfigDynamicStore:

    @staticmethod
    def add_store(store_name: str) -> None:
        """Adds a new dynamic store."""
        _ConfigDynamicStore._add_store(store_name)

    @staticmethod
    def get_store(store_name: str) -> Dict[str, Any]:
        """Retrieves the specified dynamic store."""
        return _ConfigDynamicStore._get_store(store_name)

    @staticmethod
    def delete_store(store_name: str) -> None:
        """Deletes a dynamic store."""
        _ConfigDynamicStore._delete_store(store_name)

    @staticmethod
    def add_variable(store_name: str, variable_name: str, value: Any, section: str = "") -> None:
        """Adds a variable to the dynamic store."""
        _ConfigDynamicStore._add_variable(store_name, variable_name, value, section)

    @staticmethod
    def add_variables(store_name: str, variables: dict) -> None:
        """Adds multiple variables to the dynamic store."""
        _ConfigDynamicStore._add_variables(store_name, variables)

    @staticmethod
    def set_variable(store_name: str, variable_name: str, value: Any) -> None:
        """Updates a variable's value in the dynamic store."""
        _ConfigDynamicStore._set_variable(store_name, variable_name, value)

    @staticmethod
    def set_variables(store_name: str, variables: dict) -> None:
        """Updates the values of multiple variables in the dynamic store."""
        _ConfigDynamicStore._set_variables(store_name, variables)

    @staticmethod
    def get_variable(store_name: str, variable_name: str) -> Any:
        """Retrieves a variable's value from the dynamic store."""
        return _ConfigDynamicStore._get_variable(store_name, variable_name)

    @staticmethod
    def delete_variable(store_name: str, variable_name: str) -> None:
        """Removes a variable from the dynamic store."""
        _ConfigDynamicStore._delete_variable(store_name, variable_name)

    @staticmethod
    def delete_variables(store_name: str, variables: list) -> None:
        """Removes multiple variables from the dynamic store."""
        _ConfigDynamicStore._delete_variables(store_name, variables)

    @staticmethod
    def clear_dynamic_store(store_name: str) -> None:
        """Clears all variables from the dynamic store."""
        _ConfigDynamicStore._clear_dynamic_store(store_name)

    @staticmethod
    def get_dynamic_store_keys(store_name: str) -> list:
        """Retrieves all variable names within the dynamic store."""
        return _ConfigDynamicStore._get_dynamic_store_keys(store_name)

    @staticmethod
    def get_variable_section(store_name: str, variable_name: str) -> str:
        """Gets the section of a specific variable from the dynamic store."""
        return _ConfigDynamicStore._get_variable_section(store_name, variable_name)
