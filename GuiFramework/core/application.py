# GuiFramework/core/application.py

from .window import Window

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.mixins import EventMixin
from GuiFramework.utilities import FileOps
from GuiFramework.utilities.logging import Logger, LOG_LEVEL


class Application(EventMixin):

    def __init__(self):
        EventMixin.__init__(self)
        self._log_error = lambda message: Logger.error(message, logger_name=FRAMEWORK_NAME, module_name=Application.__name__)

        self.window = Window()
        self._app_init()

    def init(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def event(self, event_type, *args):
        pass

    def cleanup(self):
        pass

    # Main application loop
    def _app_run(self):
        while not self.window.should_close():
            try:
                self._app_update()
                self._app_render()

                self.window.poll_events()
                self.window.swap_buffers()
            except Exception as e:
                self._log_error(f"An error occurred in the run loop: {e}")
                break
        self._app_cleanup()

    # Application lifecycle methods
    def _app_init(self):
        try:
            self.init()
            self._app_run()
        except Exception as e:
            self._log_error(f"An error occurred during application initialization: {e}")

    def _app_update(self):
        try:
            self.update()
            self.window.update()
        except Exception as e:
            self._log_error(f"An error occurred during application update: {e}")

    def _app_render(self):
        try:
            self.render()
            self.window.render()
        except Exception as e:
            self._log_error(f"An error occurred during application rendering: {e}")

    def _app_cleanup(self):
        try:
            self.cleanup()
            self.window.cleanup()
        except Exception as e:
            self._log_error(f"An error occurred during application cleanup: {e}")
