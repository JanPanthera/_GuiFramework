# gui_manager.py

from .gui_builder import GuiBuilder
from ...utilities import setup_default_logger


class GuiManager:
    def __init__(self, logger=None):
        self.gui_builder = GuiBuilder(logger)
        self.logger = logger if logger else setup_default_logger('GuiManager')
        self.observers = []
        self.components = {}
        self.widgets = {}
        self.logger.info("GuiManager initialized.")

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def register_widget_builder(self, widget_builder):
        self.gui_builder.register_widget_builder(widget_builder)

    def register_gui_file(self, component_name, config, master):
        self.components[component_name] = {
            "config": config,
            "master": master,
        }

    def build(self):
        self.logger.info("Starting GUI build process.")
        try:
            for component_name, info in self.components.items():
                self.logger.debug(f"Building component: {component_name}")
                self.widgets[component_name] = self.gui_builder.build(info["master"], info["config"])
            self._notify()
            self.logger.info("GUI build completed successfully.")
        except Exception as e:
            self.logger.error(f"Error during GUI build process: {e}")
            raise

    def _notify(self):
        for observer in self.observers:
            observer.set_widget_references()
