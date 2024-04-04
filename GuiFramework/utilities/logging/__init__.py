# GuiFramework/utilities/logging/__init__.py

from GuiFramework.utilities.file_ops import FileOps as fops

from .logger import Logger, LOG_LEVEL
from .internal._logger_core import LoggerConfig

__all__ = [
    "Logger",
    "LoggerConfig",
    "LOG_LEVEL"
]

Logger.add_logger(
    LoggerConfig(
        logger_name="GuiFramework",
        log_name="gui_framework",
        log_directory=fops.resolve_development_path(__file__, "logs", "GuiFramework"),
        log_level=LOG_LEVEL.DEBUG,  # Change this to LOG_LEVEL.INFO for production
        module_name="GuiFramework"
    ),
    rotate_on_add=True
)