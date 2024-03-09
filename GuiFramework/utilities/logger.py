# GuiFramework/utilities/logger.py

import logging
import os
import traceback

from datetime import datetime
from logging.handlers import RotatingFileHandler


class LOG_LEVEL:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class TextboxHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.configure(state="normal")
        self.textbox.insert("end", msg + "\n")
        self.textbox.configure(state="disabled")
        self.textbox.yview("end")


class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, date_format, backup_count,
                 append_datetime_to_rolled_files, **kwargs):
        self.base_filename = filename
        self.original_filename = filename
        self.date_format = date_format
        self.backup_count = backup_count
        self.append_datetime_to_rolled_files = append_datetime_to_rolled_files
        super().__init__(filename, encoding="utf-8", **kwargs)

    def _append_date_to_filename(self, filename):
        base, ext = os.path.splitext(filename)
        current_time = datetime.now().strftime(self.date_format)
        return f"{base}_{current_time}{ext}"

    def doRollover(self):
        try:
            if self.stream:
                self.stream.close()
                self.stream = None

            if os.path.exists(self.original_filename) and \
                    os.path.getsize(self.original_filename) > 0:
                next_backup_number = self._get_next_backup_number()

                if self.append_datetime_to_rolled_files:
                    backup_filename = self._append_date_to_filename(
                        self.base_filename)
                else:
                    backup_filename = f"{self.base_filename}.backup_{next_backup_number:02d}"
                os.makedirs(os.path.dirname(backup_filename), exist_ok=True)
                os.rename(self.original_filename, backup_filename)
                self._manage_backups()

            self.baseFilename = self.original_filename
            self.stream = self._open()
        except Exception as e:
            print(f"Error occurred during log file rollover: {str(e)}")
            print(traceback.format_exc())

    def _get_next_backup_number(self):
        backups = [f for f in os.listdir(os.path.dirname(self.base_filename))
                   if f.startswith(os.path.basename(self.base_filename) + ".backup_")]
        backup_numbers = [int(f.split("_")[-1]) for f in backups if f.split("_")[-1].isdigit()]

        return max(backup_numbers) + 1 if backup_numbers else 1

    def _manage_backups(self):
        backups = os.listdir(os.path.dirname(self.base_filename))
        backups.sort(key=lambda f: os.path.getctime(
            os.path.join(os.path.dirname(self.base_filename), f)))

        while len(backups) > self.backup_count:
            oldest_backup = backups.pop(0)
            os.remove(os.path.join(os.path.dirname(self.base_filename), oldest_backup))

        if not self.append_datetime_to_rolled_files:
            for i, backup in enumerate(backups, start=1):
                new_name_parts = backup.rsplit("_", 1)[0] + f"_{i:02d}"

                old_path = os.path.join(os.path.dirname(self.base_filename), backup)
                new_path = os.path.join(os.path.dirname(self.base_filename), new_name_parts)

                if old_path != new_path:
                    os.rename(old_path, new_path)

    def should_rollover(self):
        if self.stream is None:
            return False
        if self.maxBytes > 0:
            return self.stream.tell() >= self.maxBytes
        return False


class CustomLogger:
    def __init__(self, log_name="application.log", log_path="logs", textbox=None, log_level=logging.DEBUG,
                 max_log_size=10*1024*1024, backup_count=5, rotate_on_start=False, append_datetime_to_rolled_files=False,
                 rotation_datetime_format="%Y-%m-%d_%H-%M-%S", datetime_format="%H:%M:%S"):

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        log_file_path = os.path.join(log_path, log_name)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        log_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt=datetime_format
        )

        self.file_handler = CustomRotatingFileHandler(
            log_file_path, rotation_datetime_format, backup_count,
            append_datetime_to_rolled_files=append_datetime_to_rolled_files,
            maxBytes=max_log_size
        )
        self.file_handler.setLevel(log_level)
        self.file_handler.setFormatter(log_formatter)
        self.logger.addHandler(self.file_handler)

        if rotate_on_start:
            self.file_handler.doRollover()

        if textbox:
            textbox_handler = TextboxHandler(textbox)
            textbox_handler.setLevel(log_level)
            textbox_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                datefmt=datetime_format
            )
            textbox_handler.setFormatter(textbox_formatter)
            self.logger.addHandler(textbox_handler)

    def log(self, level, msg, *args, **kwargs):
        try:
            if self.logger.isEnabledFor(level):
                if self.file_handler.should_rollover():
                    self.file_handler.doRollover()
                self.logger._log(level, msg, args, **kwargs)
        except Exception as e:
            print(f"Error occurred during logging: {str(e)}")
            print(traceback.format_exc())

    def debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log(logging.CRITICAL, msg, *args, **kwargs)
