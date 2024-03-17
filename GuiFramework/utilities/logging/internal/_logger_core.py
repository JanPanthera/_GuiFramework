# GuiFramework/utilities/logging/internal/_logger_core.py
# ATTENTION: This module is for internal use only

import shutil

from enum import Enum
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from GuiFramework.core.constants import FILE_SIZES


class LOG_LEVEL(Enum):
    """Defines log levels."""
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


@dataclass
class LoggerConfig:
    """Configuration for logger."""
    logger_name: str = "default"
    log_name: str = "log_file"
    log_extension: str = "log"
    log_directory: Path = Path("logs")

    module_name: str = ""  # e.g. "TestClass" or "TestModule", parameter overrides this value
    log_level: LOG_LEVEL = LOG_LEVEL.NOTSET

    enabled: bool = True
    enabled_file: bool = True
    enabled_console: bool = True

    auto_newline_file: bool = True
    auto_newline_console: bool = True

    datetime_format_file: str = "%Y-%m-%d %H:%M:%S.%f"
    datetime_format_console: str = "%Y-%m-%d %H:%M:%S.%f"
    datetime_format_rotation: str = "%Y-%m-%d_%H-%M-%S"

    backup_count: int = 1
    max_file_size: int = FILE_SIZES.MB * 10  # 10 MB

    def __post_init__(self) -> None:
        """Initializes logger configuration and creates log directory."""
        self.log_directory = Path(self.log_directory) if not isinstance(self.log_directory, Path) else self.log_directory
        self.log_directory.mkdir(parents=True, exist_ok=True)

    @property
    def log_path(self) -> Path:
        """Returns the path to the log file."""
        if not hasattr(self, "_log_path"):
            self._log_path = self.log_directory / f"{self.log_name}.{self.log_extension}"
        return self._log_path


class _LoggerCore:

    @staticmethod
    def _log(message: str, level: LOG_LEVEL = LOG_LEVEL.INFO, module_name: str = "", config: LoggerConfig = None) -> None:
        """Logs a message."""
        if isinstance(config, LoggerConfig) and config.enabled:
            if config.enabled_console:
                _LoggerCore._log_console(message, level, module_name, config)
            if config.enabled_file:
                _LoggerCore._log_file(message, level, module_name, config)

    @staticmethod
    def _log_file(message: str, level: LOG_LEVEL = LOG_LEVEL.INFO, module_name: str = "", config: LoggerConfig = None) -> None:
        """Logs a message to a file."""
        if isinstance(config, LoggerConfig) and config.enabled and config.enabled_file:
            if not config.log_path.exists():
                config.log_path.touch()

            if config.log_path.stat().st_size >= config.max_file_size:
                _LoggerCore._rotate_file(config)

            with open(config.log_path, 'a') as f:
                f.write(_LoggerCore._format_message(message, level, module_name, config.datetime_format_file, config.auto_newline_file))

    @staticmethod
    def _log_console(message: str, level: LOG_LEVEL = LOG_LEVEL.INFO, module_name: str = "", config: LoggerConfig = None) -> None:
        """Logs a message to the console."""
        if isinstance(config, LoggerConfig) and config.enabled and config.enabled_console:
            print(_LoggerCore._format_message(message, level, module_name, config.datetime_format_console, config.auto_newline_console), end="")

    @staticmethod
    def _format_message(message: str, level: LOG_LEVEL = LOG_LEVEL.INFO, module_name: str = "", datetime_format: str = None, auto_newline: bool = True) -> str:
        """Formats a log message."""
        timestamp = datetime.now().strftime(datetime_format)
        module_name = f"[{module_name}]" if module_name else ""
        new_line = "\n" if auto_newline else ""
        return f"[{timestamp}]{module_name} [{level.name}] {message}{new_line}"

    @classmethod
    def _rotate_file(cls, config: LoggerConfig) -> None:
        """Rotates the log file to manage file size."""
        if isinstance(config, LoggerConfig) and config.enabled and config.log_path.exists() and config.log_path.stat().st_size > 0:
            backup_files = sorted((f for f in config.log_directory.iterdir() if f.is_file() and f.name.startswith(config.log_name + "_")), key=lambda x: x.stat().st_ctime)
            while len(backup_files) >= config.backup_count:
                backup_files.pop(0).unlink()

            backup_file_name = f"{config.log_name}_{datetime.now().strftime(config.datetime_format_rotation)}.{config.log_extension}"
            backup_file_path = config.log_directory / backup_file_name
            shutil.copy2(config.log_path, backup_file_path)
            config.log_path.write_text('')
