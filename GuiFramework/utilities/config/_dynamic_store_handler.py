# GuiFramework/utilities/config/_dynamic_store_handler.py

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.utilities.logging import Logger


class _DynamicStoreHandler:
    """Class for handling dynamic stores."""
    _dynamic_stores = {}

    @classmethod
    def _add_store(cls, store_name):
        """Add a dynamic store."""
        if store_name in cls._dynamic_stores:
            cls._warning(f"Dynamic store '{store_name}' already exists")
            return
        cls._dynamic_stores.setdefault(store_name, {})

    @classmethod
    def _add_variable(cls, store_name, variable_name, value, section=""):
        """Add a variable to the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        if variable_name in store:
            cls._warning(f"Variable '{variable_name}' already exists in dynamic store '{store_name}'")
            return
        store[variable_name] = (value, section)

    @classmethod
    def _add_variables(cls, store_name, variables):
        """Add multiple variables to the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        for variable_name, (value, section) in variables.items():
            if variable_name in store:
                cls._warning(f"Variable '{variable_name}' already exists in dynamic store '{store_name}'")
                continue
            store[variable_name] = (value, section)

    @classmethod
    def _set_variable(cls, store_name, variable_name, value):
        """Set a variable in the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        if variable_name not in store:
            cls._warning(f"Variable '{variable_name}' does not exist in dynamic store '{store_name}'")
            return
        store[variable_name] = (value, store[variable_name][1])

    @classmethod
    def _set_variables(cls, store_name, variables):
        """Set multiple variables in the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        for variable_name, value in variables.items():
            if variable_name not in store:
                cls._warning(f"Variable '{variable_name}' does not exist in dynamic store '{store_name}'")
                continue
            store[variable_name] = (value, store[variable_name][1])

    @classmethod
    def _get_variable(cls, store_name, variable_name):
        """Get a variable from the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        if variable_name not in store:
            cls._warning(f"Variable '{variable_name}' does not exist in dynamic store '{store_name}'")
            return
        return store[variable_name][0]

    @classmethod
    def _delete_variable(cls, store_name, variable_name):
        """Delete a variable from the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        if variable_name not in store:
            cls._warning(f"Variable '{variable_name}' does not exist in dynamic store '{store_name}'")
            return
        del store[variable_name]

    @classmethod
    def _delete_variables(cls, store_name, variables):
        """Delete multiple variables from the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        for variable_name in variables:
            if variable_name not in store:
                cls._warning(f"Variable '{variable_name}' does not exist in dynamic store '{store_name}'")
                continue
            del store[variable_name]

    @classmethod
    def _clear_dynamic_store(cls, store_name):
        """Clear the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        store.clear()

    @classmethod
    def _get_dynamic_store_keys(cls, store_name):
        """Get the keys of the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return
        return store.keys()

    @classmethod
    def _get_variable_section(cls, store_name, variable_name):
        """Return the associated section of the variable in the dynamic store."""
        store = cls._dynamic_stores.get(store_name)
        if store is None:
            cls._error(f"Dynamic store '{store_name}' does not exist")
            return None
        return store.get(variable_name, (None, None))[1]

    @classmethod
    def _warning(cls, message):
        """Log a warning message."""
        Logger.warning(message, logger_name=FRAMEWORK_NAME, module_name=_DynamicStoreHandler.__name__)

    @classmethod
    def _error(cls, message):
        """Log an error message."""
        Logger.error(message, logger_name=FRAMEWORK_NAME, module_name=_DynamicStoreHandler.__name__)
