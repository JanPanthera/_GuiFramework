# GuiFramework/utilities/utils.py

import ctypes

from threading import Timer
from GuiFramework.utilities.logging import Logger


class Utils:

    @staticmethod
    def get_dpi_scaling_factor():
        """Get the DPI scaling factor for the current system."""
        logger = Logger.get_logger("GuiFramework")
        if not hasattr(ctypes, "windll"):
            logger.log_warning("get_dpi_scaling_factor is designed to run on Windows.", "Utils")
            return 1.0

        try:
            awareness = ctypes.c_int()
            error_code = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

            if error_code == 0:
                dpi = ctypes.windll.user32.GetDpiForSystem()
                return dpi / 96.0
        except (AttributeError, OSError) as e:
            logger.error(f"Failed to query DPI settings: {type(e).__name__}: {e}. Using default scaling factor.", "Utils")

        return 1.0


class Debouncer:
    """Class for debouncing function calls."""

    def __init__(self, delay=0.1):
        """Initialize Debouncer with a delay."""
        self.delay = delay
        self.callback = None
        self.timer = None

    def __call__(self, callback):
        """Call the debounced function."""
        self.callback = callback
        return self._debounced

    def _debounced(self, *args, **kwargs):
        """Debounce the function call."""
        if self.timer is not None:
            self.timer.cancel()
        self.timer = Timer(self.delay, self._debounced_callback, args=args, kwargs=kwargs)
        self.timer.start()

    def _debounced_callback(self, *args, **kwargs):
        """The debounced function call."""
        if self.callback is not None:
            self.callback(*args, **kwargs)
        self.timer = None

    def cancel(self):
        """Cancel the debounce delay."""
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
