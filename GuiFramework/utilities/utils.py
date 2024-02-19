# utils.py / GuiFramework

import ctypes
import time

DEBOUNCE_DELAY = 100


def setup_default_logger():
    import logging
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def get_high_dpi_scale():
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
