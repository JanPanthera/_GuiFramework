# GuiFramework/utilities/config/private/_config_dynamic_store.py
# ATTENTION: This module is for internal use only

import threading

from typing import Any

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import StaticLoggerMixin


class _ConfigDynamicStore(StaticLoggerMixin):
    """Class dedicated to managing dynamic stores."""
    _dynamic_stores = {}
    _lock = threading.RLock()

    StaticLoggerMixin.set_logger_details(FRAMEWORK_NAME, "_ConfigDynamicStore")

    @classmethod
    def _add_store(cls, store_name: str) -> None:
        """Add a new dynamic store."""
        with cls._lock:
            if store_name in cls._dynamic_stores:
                cls._log_warning("_add_store", f"Dynamic store '{store_name}' already exists")
                return
            cls._dynamic_stores[store_name] = {}

    @classmethod
    def _get_store(cls, store_name: str) -> dict:
        """Retrieve a dynamic store."""
        with cls._lock:
            return cls._dynamic_stores.get(store_name)

    @classmethod
    def _delete_store(cls, store_name: str) -> None:
        """Delete a dynamic store."""
        with cls._lock:
            if store_name not in cls._dynamic_stores:
                cls._log_warning("_delete_store", f"Dynamic store '{store_name}' not found")
                return
            del cls._dynamic_stores[store_name]

    @classmethod
    def _add_variable(cls, store_name: str, variable_name: str, value: Any, section: str = "") -> None:
        """Add a new variable to a specific dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_add_variable", f"Dynamic store '{store_name}' not found")
                return
            if variable_name in store:
                cls._log_warning("_add_variable", f"Variable '{variable_name}' already exists in '{store_name}'")
                return
            store[variable_name] = (value, section)

    @classmethod
    def _add_variables(cls, store_name: str, variables: dict) -> None:
        """Add multiple variables to a specific dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_add_variables", f"Dynamic store '{store_name}' not found")
                return
            for variable_name, (value, section) in variables.items():
                if variable_name in store:
                    cls._log_warning("_add_variables", f"Variable '{variable_name}' already exists in '{store_name}'")
                    continue
                store[variable_name] = (value, section)

    @classmethod
    def _set_variable(cls, store_name: str, variable_name: str, value: Any) -> None:
        """Set the value of an existing variable in a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_set_variable", f"Dynamic store '{store_name}' not found")
                return
            if variable_name not in store:
                cls._log_warning("_set_variable", f"Variable '{variable_name}' does not exist in '{store_name}'")
                return
            store[variable_name] = (value, store[variable_name][1])

    @classmethod
    def _set_variables(cls, store_name: str, variables: dict) -> None:
        """Set multiple variables in a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_set_variables", f"Dynamic store '{store_name}' not found")
                return
            for variable_name, value in variables.items():
                if variable_name not in store:
                    cls._log_warning("_set_variables", f"Variable '{variable_name}' does not exist in '{store_name}'")
                    continue
                store[variable_name] = (value, store[variable_name][1])

    @classmethod
    def _get_variable(cls, store_name: str, variable_name: str) -> Any:
        """Retrieve the value of a variable from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_get_variable", f"Dynamic store '{store_name}' not found")
                return
            if variable_name not in store:
                cls._log_warning("_get_variable", f"Variable '{variable_name}' does not exist in '{store_name}'")
                return
            return store[variable_name][0]

    @classmethod
    def _delete_variable(cls, store_name: str, variable_name: str) -> None:
        """Delete a variable from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_delete_variable", f"Dynamic store '{store_name}' not found")
                return
            if variable_name not in store:
                cls._log_warning("_delete_variable", f"Variable '{variable_name}' does not exist in '{store_name}'")
                return
            del store[variable_name]

    @classmethod
    def _delete_variables(cls, store_name: str, variables: list) -> None:
        """Delete multiple variables from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_delete_variables", f"Dynamic store '{store_name}' not found")
                return
            for variable_name in variables:
                if variable_name not in store:
                    cls._log_warning("_delete_variables", f"Variable '{variable_name}' does not exist in '{store_name}'")
                    continue
                del store[variable_name]

    @classmethod
    def _clear_dynamic_store(cls, store_name: str) -> None:
        """Clear all variables from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_clear_dynamic_store", f"Dynamic store '{store_name}' not found")
                return
            store.clear()

    @classmethod
    def _get_dynamic_store_keys(cls, store_name: str) -> list:
        """Retrieve all variable names from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_get_dynamic_store_keys", f"Dynamic store '{store_name}' not found")
                return
            return store.keys()

    @classmethod
    def _get_variable_section(cls, store_name: str, variable_name: str) -> str:
        """Retrieve the section of a variable within a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if not store:
                cls._log_error("_get_variable_section", f"Dynamic store '{store_name}' not found")
                return None
            return store.get(variable_name, (None, None))[1]
