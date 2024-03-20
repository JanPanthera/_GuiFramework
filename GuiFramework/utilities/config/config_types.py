# GuiFramework/utilities/config/config_types.py

from threading import RLock
from functools import lru_cache
from dataclasses import dataclass
from collections import defaultdict
from typing import Any, Optional, Type, Callable, Set

from .exceptions import ConfigKeyTypeError, ConfigKeyNotPersistable
from .custom_type_handler_base import CustomTypeHandlerBase

from GuiFramework.mixins.event_mixin import EventMixin


BASIC_TYPES = (str, int, float, bool)


class ConfigKeyList:
    @classmethod
    def add_ConfigKey(cls, name, section="Default", type_=None, save_to_file=True, auto_save=True, config_name="Default"):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if hasattr(cls, name.upper()):
            raise AttributeError(f"Attribute '{name.upper()}' already exists. ConfigKeyList.add_ConfigKey({name}, ...)")
        config_key = ConfigKey(name, section, type_, save_to_file, auto_save, config_name)
        setattr(cls, name.upper(), config_key)

    @classmethod
    def get_ConfigKey(cls, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not hasattr(cls, name.upper()):
            raise AttributeError(f"Attribute '{name.upper()}' does not exist.")
        return getattr(cls, name.upper())

    @classmethod
    def get_ConfigKeys(cls):
        return [getattr(cls, attr) for attr in dir(cls) if isinstance(getattr(cls, attr), ConfigKey)]


@dataclass(frozen=True)
class ConfigKey:
    """Represents a configuration key."""
    name: str
    section: str = "Default"
    type_: Type[Any] = None
    save_to_file: bool = False
    auto_save: bool = True
    config_name: str = "Default"

    def __post_init__(self) -> None:
        """Validate type_ attribute after initialization."""
        if self.type_ is not None and not isinstance(self.type_, type):
            raise ConfigKeyTypeError(f"Expected a type object or None for 'type_', got {type(self.type_).__name__} instead.")


class ConfigVariable(EventMixin):
    """Represents a configuration variable."""

    def __init__(self, config_key: ConfigKey, value: Optional[Any] = None, default_value: Optional[Any] = None, type_handler: Optional[CustomTypeHandlerBase] = None) -> None:
        """Initialize a configuration variable."""
        self._validate_initialization_types(config_key, value, default_value)
        self._config_key = config_key
        self._value = value
        self._default_value = default_value if default_value is not None else value
        self._type_handler = type_handler
        self._subscribers = defaultdict(set)
        self._lock = RLock()

    def _validate_initialization_types(self, config_key: ConfigKey, value: Any, default_value: Any) -> None:
        """Validate types during initialization."""
        self._validate_type(config_key, ConfigKey, 'config_key')
        self._validate_type(value, config_key.type_, 'value')
        self._validate_type(default_value, config_key.type_, 'default_value')

    def _validate_type(self, value: Any, expected_type: Type[Any], name: str) -> None:
        """Validate the type of the given value."""
        if value is not None and not isinstance(value, expected_type):
            raise ConfigKeyTypeError(f"Expected a {expected_type.__name__} object for '{name}', got {type(value).__name__} instead.")

    def get_value(self) -> Any:
        """Get the current value of the configuration variable."""
        return self._value

    def get_default_value(self) -> Any:
        """Get the default value of the configuration variable."""
        return self._default_value

    def set_value(self, value: Any) -> None:
        """Set the value of the configuration variable."""
        self._validate_type(value, self._config_key.type_, 'value')
        self._value = value
        self.notify('value_changed', new_value=value)

    @lru_cache(maxsize=None)
    def is_persistable(self) -> bool:
        """Check if the configuration variable is persistable."""
        return self._config_key.type_ in BASIC_TYPES or bool(self._type_handler)

    def serialize(self) -> str:
        """Serialize the configuration variable for storage."""
        if not self.is_persistable():
            raise ValueError(f"Cannot serialize '{self._config_key.name}': value is not persistable.")
        return self._type_handler.serialize(self._value) if self._type_handler else str(self._value)

    def deserialize(self, serialized_value: str) -> Any:
        """Deserialize the configuration variable from storage."""
        if not self.is_persistable():
            raise ValueError(f"Cannot deserialize '{self._config_key.name}': original value is not persistable.")
        return self._type_handler.deserialize(serialized_value) if self._type_handler else self._config_key.type_(serialized_value)
