# GuiFramework/utilities/config/custom_type_handler_base.py

from abc import ABC, abstractmethod
from typing import Any, Type


class CustomTypeHandlerBase(ABC):
    """
    Abstract base class for custom type handlers.
    """

    @abstractmethod
    def serialize(self, value: Any) -> str:
        """
        Abstract method to serialize a value.

        :param value: The value to serialize.
        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, value: str) -> Any:
        """
        Abstract method to deserialize a value.

        :param value: The value to deserialize.
        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> Type:
        """
        Abstract method to get the type of the value.

        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def get_test_value(self) -> Any:
        """
        Abstract method to get a test value.

        :raises NotImplementedError: If the method is not implemented.
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

    @abstractmethod
    def validate_serialization(self) -> None:
        """
        Validates the serialization and deserialization methods by testing them with a test value.

        :raises AssertionError: If the deserialized value does not match the original test value.
        """
        test_value = self.get_test_value()
        serialized_value = self.serialize(test_value)
        deserialized_value = self.deserialize(serialized_value)
        assert deserialized_value == test_value, "Serialization test failed: deserialized value does not match the original"

    def validate_custom_type_handler(self) -> None:
        """
        Validates the custom type handler by checking the type of the test value and the serialization.

        :raises TypeError: If the type of the test value or the return value of get_type() is not correct.
        """
        type_ = self.get_type()
        if not isinstance(type_, type):
            raise TypeError(f"Expected get_type() to return a type object, got {type(type_).__name__} instead.")
        test_value = self.get_test_value()
        if not isinstance(test_value, type_):
            raise TypeError(f"Expected get_test_value() to return a {type_.__name__}, got {type(test_value).__name__} instead.")
        self.validate_serialization()
