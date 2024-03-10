# GuiFramework/utilities/logging/__init__.py


from .logger import Logger, LOG_LEVEL
from .logger_mixin import LoggerMixin
from ._logger_core import LoggerConfig
__all__ = ["Logger", "LoggerConfig", "LoggerMixin", "LOG_LEVEL"]


import GuiFramework.utilities.file_ops as f
config = LoggerConfig(
    log_name="default",
    log_directory=f.FileOps.resolve_development_path(__file__, "logs", ".root"),
    log_level=LOG_LEVEL.DEBUG,
    enabled=True,
)
Logger.add_config(logger_name="default", config=config)
Logger.rotate_file(logger_name="default")
