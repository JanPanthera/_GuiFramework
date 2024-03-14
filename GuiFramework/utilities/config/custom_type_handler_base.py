# GuiFramework/utilities/config/custom_type_handler_base.py

from abc import ABC, abstractmethod


class CustomTypeHandlerBase(ABC):
    """
    An abstract base class dedicated to the creation of custom type handlers.
    These handlers are designed to enable the conversion of custom types into strings and vice versa for the purpose of configuration file storage.
    """

    @abstractmethod
    def serialize(self, value):
        """
        Transforms a custom type value into a string suitable for configuration file storage.

        Args:
            value: The custom type value to be transformed.

        Raises:
            NotImplementedError: This method must be overridden in derived classes.
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, value):
        """
        Reverts a string from a configuration file into its original custom type.

        Args:
            value: The string value to be reverted into a custom type.

        Raises:
            NotImplementedError: This method must be overridden in derived classes.
        """
        raise NotImplementedError

    @staticmethod
    def validate_type(value, expected_type, type_name):
        """
        Ensures that the provided value matches the expected type.

        Args:
            value: The value to be checked.
            expected_type: The type that the value is expected to be.
            type_name: The human-readable name of the expected type.

        Raises:
            TypeError: If the provided value does not match the expected type.
        """
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected value to be of type {type_name}, but got type {type(value).__name__} instead.")