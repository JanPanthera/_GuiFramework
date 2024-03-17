# GuiFramework/utilities/logging/__init__.py


from .logger import Logger, LOG_LEVEL
from .internal._logger_core import LoggerConfig

__all__ = [
    "Logger",
    "LoggerConfig",
    "LOG_LEVEL"
]
