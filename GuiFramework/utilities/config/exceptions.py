# GuiFramework/utilities/config/exceptions.py


class ValueNotSaveable(ValueError):
    """Raised when a value is not saveable."""
    pass


class HandlerTypeError(TypeError):
    """Raised when a handler is not an instance of CustomTypeHandlerBase."""
    pass


class HandlerValidationFailed(ValueError):
    """Raised when a handler fails validation."""
    pass


class HandlerAlreadyExists(KeyError):
    """Raised when a handler for a type already exists."""
    pass


class HandlerNotFound(KeyError):
    """Raised when no handler is found for a type."""
    pass


class ConfigKeyNotPersistable(ValueError):
    """Raised when a value is not persistable."""
    pass


class ConfigKeyTypeError(TypeError):
    """Raised when a ConfigKey type is not a type object or None."""
    pass


class ConfigKeyAlreadyExists(KeyError):
    """Raised when a ConfigKey already exists."""
    pass


class ConfigKeyNotFound(KeyError):
    """Raised when no ConfigKey is found for a name."""
    pass


class ConfigVariableTypeError(TypeError):
    """Raised when a ConfigVariable type is not a type object or None."""
    pass
