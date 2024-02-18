# gui_manager.py

from .gui_builder import GuiBuilder


class GuiManager:

    def __init__(self, config_manager=None, localization_function=None, logger=None):
        self.gui_builder = GuiBuilder(config_manager, localization_function, logger)
        self.logger = logger
        self.observers = []
        self.components = {}
        self.widgets = {}

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def register(self, component_name, config, master, instance):
        self.components[component_name] = {
            "config": config,
            "master": master,
            "instance": instance
        }

    def build(self):
        for component_name, info in self.components.items():
            self.widgets[component_name] = self.gui_builder.build(info["master"], info["config"], info["instance"])
        self._notify()

    def register_widget_creator(self, widget_type, widget_creator):
        self.gui_builder.register_widget_creator(widget_type, widget_creator)

    def _notify(self):
        for observer in self.observers:
            observer.set_widget_references()