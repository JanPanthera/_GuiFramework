# GuiFramework/utilities/logger/_logger_core.py

from enum import Enum
from datetime import datetime
from dataclasses import dataclass

from GuiFramework.utilities.file_ops import FileOps, FileSizes


class LOG_LEVEL(Enum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


@dataclass
class LoggerConfig:
    log_name: str = "log_file"
    log_extension: str = "log"
    log_directory: str = "logs"
    log_level: LOG_LEVEL = LOG_LEVEL.NOTSET
    enabled: bool = True
    output_datetime_format: str = "%Y-%m-%d %H:%M:%S.%f"
    rotation_datetime_format: str = "%Y-%m-%d_%H-%M-%S"
    rotate_on_startup: bool = True
    backup_count: int = 1
    max_file_size: int = FileSizes.MB_10.value

    @property
    def log_path(self) -> str:
        return FileOps.join_paths(self.log_directory, f"{self.log_name}.{self.log_extension}")


class _LoggerCore:
    logger_configs = {}

    @classmethod
    def _add_config(cls, logger_name="default", config=None):
        if isinstance(config, LoggerConfig) and logger_name not in cls.logger_configs:
            cls.logger_configs[logger_name] = config
            cls._rotate_file(config) if config.rotate_on_startup else None

    @classmethod
    def _change_config(cls, logger_name="default", config=None):
        if isinstance(config, LoggerConfig) and logger_name in cls.logger_configs:
            cls.logger_configs[logger_name] = config

    @classmethod
    def _remove_config(cls, logger_name="default"):
        if logger_name in cls.logger_configs:
            del cls.logger_configs[logger_name]

    @classmethod
    def _log(cls, message, level=LOG_LEVEL.INFO, logger_name="default", module_name="", auto_newline=True):
        config = cls.logger_configs.get(logger_name, None)
        if not config or not config.enabled or level.value < config.log_level.value:
            return

        if FileOps.get_file_size(config.log_path) > config.max_file_size:
            cls._rotate_file(config)

        formatted_message = cls._format_message(message, config, module_name, level, auto_newline)
        try:
            FileOps.append_file(file_path=config.log_path, content=formatted_message)
        except Exception as e:
            raise e

    @staticmethod
    def _format_message(message, config, module_name="", level=LOG_LEVEL.INFO, auto_newline=True):
        if not config:
            return ""

        timestamp = datetime.now().strftime(config.output_datetime_format)
        new_line = "\n" if auto_newline else ""
        module_name = f"[{module_name}]" if module_name else ""
        return f"[{timestamp}]{module_name} [{level.name}] {message}{new_line}"

    @classmethod
    def _rotate_file(cls, config):
        if not config or not config.enabled or not FileOps.file_exists(config.log_path):
            return

        log_directory = config.log_directory
        if not FileOps.directory_exists(log_directory):
            FileOps.create_directory(log_directory)

        backup_files = FileOps.get_files_in_directory(log_directory, pattern=f"{config.log_name}_*")
        if len(backup_files) >= config.backup_count:
            FileOps.delete_file(min(backup_files, key=FileOps.get_file_creation_time))

        backup_file_name = f"{config.log_name}_{datetime.now().strftime(config.rotation_datetime_format)}.{config.log_extension}"
        backup_file_path = FileOps.join_paths(log_directory, backup_file_name)
        FileOps.copy_file(config.log_path, backup_file_path)
        FileOps.clear_file(config.log_path)
