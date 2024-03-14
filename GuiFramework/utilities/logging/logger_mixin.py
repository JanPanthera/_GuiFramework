# GuiFramework/utilities/logging/logger_mixin.py

from typing import Optional

from ._logger_core import LoggerConfig
from .logger import Logger, LOG_LEVEL


class LoggerMixin:
    def __init__(self, logger_name: str = "default", module_name: str = "", logger_config: Optional[LoggerConfig] = None):
        self.logger_name = logger_name
        self.module_name = module_name
        if logger_config:
            Logger.add_config(self.logger_name, logger_config)

    def log(self, message: str, log_level: LOG_LEVEL = LOG_LEVEL.INFO, method_name: str = "") -> None:
        formatted_message = f"{method_name}: {message}" if method_name else message
        Logger.log(formatted_message, log_level, logger_name=self.logger_name, module_name=self.module_name)

    def log_debug(self, message: str, method_name: str = "") -> None:
        self.log(message, LOG_LEVEL.DEBUG, method_name)

    def log_info(self, message: str, method_name: str = "") -> None:
        self.log(message, LOG_LEVEL.INFO, method_name)

    def log_warning(self, message: str, method_name: str = "") -> None:
        self.log(message, LOG_LEVEL.WARNING, method_name)

    def log_error(self, message: str, method_name: str = "") -> None:
        self.log(message, LOG_LEVEL.ERROR, method_name)

    def log_critical(self, message: str, method_name: str = "") -> None:
        self.log(message, LOG_LEVEL.CRITICAL, method_name)


class StaticLoggerMixin:
    logger_name = "default"
    module_name = ""

    @staticmethod
    def set_logger_details(logger_name: str, module_name: str, logger_config: Optional[LoggerConfig] = None) -> None:
        StaticLoggerMixin.logger_name = logger_name
        StaticLoggerMixin.module_name = module_name
        if logger_config:
            Logger.add_config(logger_name, logger_config)

    @staticmethod
    def log(message: str, log_level: LOG_LEVEL = LOG_LEVEL.INFO, method_name: str = "") -> None:
        formatted_message = f"{method_name}: {message}" if method_name else message
        Logger.log(formatted_message, log_level, logger_name=StaticLoggerMixin.logger_name, module_name=StaticLoggerMixin.module_name)

    @staticmethod
    def log_debug(message: str, method_name: str = "") -> None:
        StaticLoggerMixin.log(message, LOG_LEVEL.DEBUG, method_name)

    @staticmethod
    def log_info(message: str, method_name: str = "") -> None:
        StaticLoggerMixin.log(message, LOG_LEVEL.INFO, method_name)

    @staticmethod
    def log_warning(message: str, method_name: str = "") -> None:
        StaticLoggerMixin.log(message, LOG_LEVEL.WARNING, method_name)

    @staticmethod
    def log_error(message: str, method_name: str = "") -> None:
        StaticLoggerMixin.log(message, LOG_LEVEL.ERROR, method_name)

    @staticmethod
    def log_critical(message: str, method_name: str = "") -> None:
        StaticLoggerMixin.log(message, LOG_LEVEL.CRITICAL, method_name)
