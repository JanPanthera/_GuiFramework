# GuiFramework/tests/logging/test_logger.py

from GuiFramework.utilities.file_ops import FileOps
from GuiFramework.utilities.logging import Logger, LoggerConfig, LOG_LEVEL


class TestLoggerClass:
    def __init__(self):

        log_dir = FileOps.resolve_development_path(__file__, "logs", ".root")

        self.logger = Logger(
            LoggerConfig(
                logger_name="test_logger",
                log_name="test_log",
                log_directory=log_dir,
                log_level=LOG_LEVEL.DEBUG,
                module_name="TestLoggerClass"
            ),
            rotate_on_init=True
        )

    def test_method(self):
        self.logger.log_debug("This is a debug message", "test_method")
        self.logger.log_info("This is an info message", "test_method")
        self.logger.log_warning("This is a warning message", "test_method")
        self.logger.log_error("This is an error message")
        self.logger.log_critical("This is a critical message")

        another_logger = Logger.add_logger(
            LoggerConfig(
                logger_name="another_logger",
                log_name="another_log",
                log_directory=FileOps.resolve_development_path(__file__, "logs", ".root"),
                log_level=LOG_LEVEL.DEBUG,
                module_name="AnotherTestLoggerClass"
            )
        )
        another_logger.rotate_log()
        another_logger.log_debug("This is a debug message", "test_method")
        another_logger.log_info("This is an info message", "test_method")
        another_logger.log_warning("This is a warning message", "test_method")
        another_logger.log_error("This is an error message", "test_method")
        another_logger.log_critical("This is a critical message", "test_method")

    def test_method2(self):
        local_logger = Logger.get_logger("another_logger")
        local_logger.log_debug("This is a debug message", "test_method2")
        local_logger.log_info("This is an info message", "test_method2")
        local_logger.log_warning("This is a warning message", "test_method2")
        local_logger.log_error("This is an error message", "test_method2")
        local_logger.log_critical("This is a critical message", "test_method2")
        
        Logger.slog_error("another_logger", "This is a static error message", "test_method2")
        Logger.slog_critical("another_logger", "This is a static critical message", "test_method2")
        
        Logger.slog_info("another_logger", "This is a static info message", "test_method2")
        Logger.slog_warning("another_logger", "This is a static warning message", "test_method2")


def main():
    test_logger = TestLoggerClass()
    test_logger.test_method()
    test_logger.test_method2()


if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
