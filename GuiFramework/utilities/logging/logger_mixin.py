# GuiFramework/utilities/logging/logger_mixin.py

from .logger import Logger, LOG_LEVEL
from ._logger_core import LoggerConfig


class LoggerMixin:
    def __init__(self, logger_name: str = "default", module_name: str = "", logger_config: LoggerConfig = None):
        self.logger_name = logger_name if logger_config else "default"
        self.module_name = module_name
        if logger_config:
            Logger.add_config(self.logger_name, logger_config)

    def log(self, message: str, log_level: LOG_LEVEL = LOG_LEVEL.INFO):
        Logger.log(message, log_level, logger_name=self.logger_name, module_name=self.module_name)

    def debug(self, message: str):
        self.log(message, LOG_LEVEL.DEBUG)

    def info(self, message: str):
        self.log(message, LOG_LEVEL.INFO)

    def warning(self, message: str):
        self.log(message, LOG_LEVEL.WARNING)

    def error(self, message: str):
        self.log(message, LOG_LEVEL.ERROR)

    def critical(self, message: str):
        self.log(message, LOG_LEVEL.CRITICAL)
