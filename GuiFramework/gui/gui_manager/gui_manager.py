# GuiFramework/gui/gui_manager/gui_manager.py

from GuiFramework.utilities.logging import Logger
from GuiFramework.gui.gui_manager.gui_builder import GuiBuilder


class GuiManager:
    def __init__(self):
        self.logger = Logger.get_logger("GuiFramework")
        self.gui_builder = GuiBuilder()
        self.observers = []
        self.components = {}
        self.widgets = {}
        self.logger.log_info("GuiManager initialized.", "GuiManager")

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def register_widget_builder(self, widget_builder):
        self.gui_builder.register_widget_builder(widget_builder)

    def register_gui_file(self, component_name, config, master, instance):
        self.components[component_name] = {
            "config": config,
            "master": master,
            "instance": instance
        }

    def build(self):
        self.logger.log_info("Starting GUI build process.", "GuiManager")
        try:
            for component_name, info in self.components.items():
                self.logger.log_debug(f"Building component: {component_name}", "GuiManager")
                self.widgets[component_name] = self.gui_builder.build(info["master"], info["config"], info["instance"])
            self._notify()
            self.logger.log_info("GUI build completed successfully.", "GuiManager")
        except Exception as e:
            self.logger.log_error(f"Error during GUI build process: {e}", "GuiManager")
            raise

    def _notify(self):
        for observer in self.observers:
            observer.on_gui_build()
