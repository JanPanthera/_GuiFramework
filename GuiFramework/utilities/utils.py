# utilities/utils.py

import time
import ctypes
import logging

DEBOUNCE_DELAY = 100


def setup_default_logger(logger_name='default_logger'):
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
    return logger


def get_dpi_scaling_factor(logger=None):
    """
    Function to get the DPI scaling factor for the current system.
    Designed to run on Windows. If not on Windows, returns 1.0.
    """
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


def get_dpi_scaling_factor():
    return ctypes.windll.user32.GetDpiForSystem() / 96


def handle_error(logger, message):
    if logger is not None:
        logger.error(message)
    else:
        print(message)


def handle_warning(logger, message):
    if logger is not None:
        logger.warning(message)
    else:
        print(message)


class Debouncer:
    def __init__(self, delay=0.1):
        self.delay = delay  # The minimum delay between calls
        self.callback = None
        self.next_call_time = 0  # The earliest time the next call is allowed

    def __call__(self, callback):
        self.callback = callback
        return self._debounced

    def _debounced(self, *args, **kwargs):
        current_time = time.time()
        if current_time >= self.next_call_time:
            self.next_call_time = current_time + self.delay
            self.callback(*args, **kwargs)

    def cancel(self):
        self.next_call_time = 0  # Reset the timer, effectively cancelling the debounce delay
