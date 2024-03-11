# GuiFramework/utilities/config/custom_type_handler_base.py

from abc import ABC, abstractmethod


class CustomTypeHandlerBase(ABC):
    """
    This is an abstract base class for creating custom type handlers.
    Custom type handlers are used to convert custom types into strings for storage in a config file and vice versa.
    """

    @abstractmethod
    def save(self, value):
        """
        Abstract method for converting a custom type into a string for storage in a config file.

        Args:
            value: The custom type value to be converted into a string.

        Raises:
            NotImplementedError: This is an abstract method that needs to be implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, value):
        """
        Abstract method for converting a string loaded from a config file into a custom type.

        Args:
            value: The string value to be converted into a custom type.

        Raises:
            NotImplementedError: This is an abstract method that needs to be implemented in a subclass.
        """
        raise NotImplementedError
