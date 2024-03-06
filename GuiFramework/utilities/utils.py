# GuiFramework/utilities/utils.py

import time
import ctypes
import logging

from GuiFramework.utilities.logger import CustomLogger, LOG_LEVEL


DEBOUNCE_DELAY = 100


def setup_default_logger(log_name='default_logger'):
    """Setup the default logger."""
    return CustomLogger(
        log_name=log_name if log_name.endswith('.log') else f"{log_name}.log",
        log_path="logs",
        textbox=None,
        log_level=LOG_LEVEL.DEBUG,
        max_log_size=10 << 20,
        backup_count=1,
        rotate_on_start=True,
        append_datetime_to_rolled_files=True
    )


def get_dpi_scaling_factor(logger=None):
    """Get the DPI scaling factor for the current system."""
    logger = logger or setup_default_logger()
    scaling_factor = 1.0

    if not hasattr(ctypes, 'windll'):
        logger.warning("get_dpi_scaling_factor is designed to run on Windows.")
        return scaling_factor

    try:
        awareness = ctypes.c_int()
        error_code = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

        if error_code == 0:
            dpi = ctypes.windll.user32.GetDpiForSystem()
            scaling_factor = dpi / 96.0
    except (AttributeError, OSError) as e:
        logger.error(f"Failed to query DPI settings: {type(e).__name__}: {e}. Using default scaling factor.")

    return scaling_factor


def handle_error(logger, message):
    """Handle error messages."""
    if logger is not None:
        logger.error(message)
    else:
        print(message)


def handle_warning(logger, message):
    """Handle warning messages."""
    if logger is not None:
        logger.warning(message)
    else:
        print(message)


class Debouncer:
    """Class for debouncing function calls."""

    def __init__(self, delay=0.1):
        """Initialize Debouncer with a delay."""
        self.delay = delay
        self.callback = None
        self.next_call_time = 0

    def __call__(self, callback):
        """Call the debounced function."""
        self.callback = callback
        return self._debounced

    def _debounced(self, *args, **kwargs):
        """Debounce the function call."""
        current_time = time.time()
        if current_time >= self.next_call_time:
            self.next_call_time = current_time + self.delay
            self.callback(*args, **kwargs)

    def cancel(self):
        """Cancel the debounce delay."""
        self.next_call_time = 0
