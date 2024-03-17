# GuiFramework/utilities/logging/logger.py

from typing import Optional
from .internal._logger_core import _LoggerCore, LOG_LEVEL, LoggerConfig


class Logger:
    """Manages logging instances."""
    _loggers: dict = {}

    def __init__(self, config: LoggerConfig, rotate_on_init: bool = False) -> None:
        """Initialize or retrieve a logger."""
        self.config: LoggerConfig = config or LoggerConfig()
        Logger.add_logger(self.config)
        if rotate_on_init:
            self.rotate_log()

    @classmethod
    def add_logger(cls, config: LoggerConfig) -> Optional['Logger']:
        """Add a new logger configuration."""
        if isinstance(config, LoggerConfig) and config.logger_name not in cls._loggers:
            cls._loggers[config.logger_name] = Logger(config)
            return cls._loggers[config.logger_name]

    @classmethod
    def get_logger(cls, logger_name: str = "default") -> 'Logger':
        """Retrieve an existing logger by name."""
        return cls._loggers.get(logger_name, ValueError(f"Logger with name '{logger_name}' not found. Please add it before getting."))

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
