# GuiFramework/utilities/logging/logger.py

from typing import Optional
from .internal._logger_core import _LoggerCore, LOG_LEVEL, LoggerConfig


class Logger:
    """Manages logging instances."""
    _loggers: dict = {}

    def __init__(self, config: LoggerConfig, rotate_on_init: bool = False) -> None:
        """Initialize or retrieve a logger."""
        self.config: LoggerConfig = config or LoggerConfig()
        if self.config.logger_name not in self._loggers:
            self._loggers[self.config.logger_name] = self
        if rotate_on_init:
            self.rotate_log()

    @classmethod
    def add_logger(cls, config: LoggerConfig, rotate_on_add: bool = False) -> Optional['Logger']:
        """Add a new logger configuration."""
        if isinstance(config, LoggerConfig) and config.logger_name not in cls._loggers:
            cls._loggers[config.logger_name] = Logger(config, rotate_on_add)
            return cls._loggers[config.logger_name]

    @classmethod
    def get_logger(cls, logger_name: str = "default") -> 'Logger':
        """Retrieve an existing logger by name."""
        return cls._loggers.get(logger_name, ValueError(f"Logger with name '{logger_name}' not found. Please add it before getting."))

    @classmethod
    def remove_logger(cls, logger_name: str) -> None:
        """Remove a logger by name."""
        if logger_name in cls._loggers:
            del cls._loggers[logger_name]

    @classmethod
    def get_loggers(cls) -> dict:
        """Retrieve all loggers."""
        return cls._loggers

    def rotate_log(self) -> None:
        """Rotate the log file."""
        _LoggerCore._rotate_file(self.config)

    def log(self, message: str, level: LOG_LEVEL, module_name: Optional[str] = None) -> None:
        """Log a message at a specified level."""
        _LoggerCore._log(message, level, module_name or self.config.module_name, self.config)

    def log_debug(self, message: str, module_name: Optional[str] = None) -> None:
        """Log a debug message."""
        self.log(message, LOG_LEVEL.DEBUG, module_name)

    def log_info(self, message: str, module_name: Optional[str] = None) -> None:
        """Log an info message."""
        self.log(message, LOG_LEVEL.INFO, module_name)

    def log_warning(self, message: str, module_name: Optional[str] = None) -> None:
        """Log a warning message."""
        self.log(message, LOG_LEVEL.WARNING, module_name)

    def log_error(self, message: str, module_name: Optional[str] = None) -> None:
        """Log an error message."""
        self.log(message, LOG_LEVEL.ERROR, module_name)

    def log_critical(self, message: str, module_name: Optional[str] = None) -> None:
        """Log a critical message."""
        self.log(message, LOG_LEVEL.CRITICAL, module_name)

    @staticmethod
    def slog(logger_name: str, message: str, level: LOG_LEVEL, module_name: Optional[str] = None) -> None:
        """Static method to log a message at a specified level."""
        logger = Logger.get_logger(logger_name)
        logger.log(message, level, module_name)

    @staticmethod
    def slog_debug(logger_name: str, message: str, module_name: Optional[str] = None) -> None:
        """Static method to log a debug message."""
        Logger.slog(logger_name, message, LOG_LEVEL.DEBUG, module_name)

    @staticmethod
    def slog_info(logger_name: str, message: str, module_name: Optional[str] = None) -> None:
        """Static method to log an info message."""
        Logger.slog(logger_name, message, LOG_LEVEL.INFO, module_name)

    @staticmethod
    def slog_warning(logger_name: str, message: str, module_name: Optional[str] = None) -> None:
        """Static method to log a warning message."""
        Logger.slog(logger_name, message, LOG_LEVEL.WARNING, module_name)

    @staticmethod
    def slog_error(logger_name: str, message: str, module_name: Optional[str] = None) -> None:
        """Static method to log an error message."""
        Logger.slog(logger_name, message, LOG_LEVEL.ERROR, module_name)

    @staticmethod
    def slog_critical(logger_name: str, message: str, module_name: Optional[str] = None) -> None:
        """Static method to log a critical message."""
        Logger.slog(logger_name, message, LOG_LEVEL.CRITICAL, module_name)
