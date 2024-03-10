# GuiFramework/utilities/logger.py

from ._logger_core import _LoggerCore, LOG_LEVEL


class Logger:
    @staticmethod
    def add_config(logger_name="default", config=None):
        _LoggerCore._add_config(logger_name, config)

    @staticmethod
    def change_config(logger_name="default", config=None):
        _LoggerCore._change_config(logger_name, config)

    @staticmethod
    def remove_config(logger_name="default"):
        _LoggerCore._remove_config(logger_name)

    @staticmethod
    def log(message, level=LOG_LEVEL.INFO, logger_name="default", module_name="", auto_newline=True):
        _LoggerCore._log(message, level, logger_name, module_name, auto_newline)

    @staticmethod
    def debug(message, logger_name="default", module_name="", auto_newline=True):
        _LoggerCore._log(message, LOG_LEVEL.DEBUG, logger_name, module_name, auto_newline)

    @staticmethod
    def info(message, logger_name="default", module_name="", auto_newline=True):
        _LoggerCore._log(message, LOG_LEVEL.INFO, logger_name, module_name, auto_newline)

    @staticmethod
    def warning(message, logger_name="default", module_name="", auto_newline=True):
        _LoggerCore._log(message, LOG_LEVEL.WARNING, logger_name, module_name, auto_newline)

    @staticmethod
    def error(message, logger_name="default", module_name="", auto_newline=True):
        _LoggerCore._log(message, LOG_LEVEL.ERROR, logger_name, module_name, auto_newline)

    @staticmethod
    def fatal(message, logger_name="default", module_name="", auto_newline=True):
        _LoggerCore._log(message, LOG_LEVEL.FATAL, logger_name, module_name, auto_newline)

    @staticmethod
    def critical(message, logger_name="default", module_name="", auto_newline=True):
        _LoggerCore._log(message, LOG_LEVEL.CRITICAL, logger_name, module_name, auto_newline)

    @staticmethod
    def rotate_file(logger_name="default"):
        config = _LoggerCore.logger_configs.get(logger_name)
        _LoggerCore._rotate_file(config)
