# GuiFramework/utilities/config/private/_config_dynamic_store.py
# ATTENTION: This module is for internal use only

import threading
from typing import Any, Optional, Dict, List

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import StaticLoggerMixin


class _ConfigDynamicStore(StaticLoggerMixin):
    """Manages dynamic configuration stores."""
    _dynamic_stores: Dict[str, Dict[str, Any]] = {}
    _lock = threading.RLock()

    StaticLoggerMixin.set_logger_details(FRAMEWORK_NAME, "_ConfigDynamicStore")

    @classmethod
    def _add_store(cls, store_name: str) -> None:
        """Add a new dynamic store."""
        with cls._lock:
            if store_name not in cls._dynamic_stores:
                cls._dynamic_stores[store_name] = {}
            else:
                cls._log_warning("_add_store", f"Dynamic store '{store_name}' already exists.")

    @classmethod
    def _get_store(cls, store_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a dynamic store."""
        with cls._lock:
            return cls._dynamic_stores.get(store_name)

    @classmethod
    def _delete_store(cls, store_name: str) -> None:
        """Delete a dynamic store."""
        with cls._lock:
            if store_name in cls._dynamic_stores:
                del cls._dynamic_stores[store_name]
            else:
                cls._log_warning("_delete_store", f"Dynamic store '{store_name}' not found.")

    @classmethod
    def _add_variable(cls, store_name: str, variable_name: str, value: Any) -> None:
        """Add a new variable to a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_add_variable", f"Dynamic store '{store_name}' not found.")
                return
            if variable_name not in store:
                store[variable_name] = value
            else:
                cls._log_warning("_add_variable", f"Variable '{variable_name}' already exists in '{store_name}'.")

    @classmethod
    def _add_variables(cls, store_name: str, variables: Dict[str, Any]) -> None:
        """Add multiple variables to a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_add_variables", f"Dynamic store '{store_name}' not found.")
                return
            for variable_name, value in variables.items():
                if variable_name not in store:
                    store[variable_name] = value
                else:
                    cls._log_warning("_add_variables", f"Variable '{variable_name}' already exists in '{store_name}'.")

    @classmethod
    def _set_variable(cls, store_name: str, variable_name: str, value: Any) -> None:
        """Set the value of an existing variable in a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_set_variable", f"Dynamic store '{store_name}' not found.")
                return
            if variable_name in store:
                store[variable_name] = value
            else:
                cls._log_warning("_set_variable", f"Variable '{variable_name}' does not exist in '{store_name}'.")

    @classmethod
    def _set_variables(cls, store_name: str, variables: Dict[str, Any]) -> None:
        """Set multiple variables in a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_set_variables", f"Dynamic store '{store_name}' not found.")
                return
            for variable_name, value in variables.items():
                if variable_name in store:
                    store[variable_name] = value
                else:
                    cls._log_warning("_set_variables", f"Variable '{variable_name}' does not exist in '{store_name}'.")

    @classmethod
    def _get_variable(cls, store_name: str, variable_name: str) -> Optional[Any]:
        """Retrieve the value of a variable from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_get_variable", f"Dynamic store '{store_name}' not found.")
                return None
            if variable_name in store:
                return store[variable_name]
            else:
                cls._log_warning("_get_variable", f"Variable '{variable_name}' does not exist in '{store_name}'.")
                return None

    @classmethod
    def _delete_variable(cls, store_name: str, variable_name: str) -> None:
        """Delete a variable from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_delete_variable", f"Dynamic store '{store_name}' not found.")
                return
            if variable_name in store:
                del store[variable_name]
            else:
                cls._log_warning("_delete_variable", f"Variable '{variable_name}' does not exist in '{store_name}'.")

    @classmethod
    def _delete_variables(cls, store_name: str, variables: List[str]) -> None:
        """Delete multiple variables from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_delete_variables", f"Dynamic store '{store_name}' not found.")
                return
            for variable_name in variables:
                if variable_name in store:
                    del store[variable_name]
                else:
                    cls._log_warning("_delete_variables", f"Variable '{variable_name}' does not exist in '{store_name}'.")

    @classmethod
    def _clear_dynamic_store(cls, store_name: str) -> None:
        """Clear all variables from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_clear_dynamic_store", f"Dynamic store '{store_name}' not found.")
                return
            store.clear()

    @classmethod
    def _get_dynamic_store_keys(cls, store_name: str) -> List[str]:
        """Retrieve all variable names from a dynamic store."""
        with cls._lock:
            store = cls._dynamic_stores.get(store_name)
            if store is None:
                cls._log_error("_get_dynamic_store_keys", f"Dynamic store '{store_name}' not found.")
                return []
            return list(store.keys())
