# gui_builder.py

import json
from .widget_builder import WidgetBuilder
from .frame_builder import FrameBuilder


class GuiBuilder:
    def __init__(self, config_manager=None, localization_function=None, logger=None):
        self.logger = logger
        self.widget_builder = WidgetBuilder(config_manager, localization_function, logger)
        self.frame_builder = FrameBuilder(self.widget_builder, self.apply_packing, logger)

    def register_widget_creator(self, widget_type, widget_creator):
        self.widget_builder.register_widget_creator(widget_type, widget_creator)

    def build(self, master, config_path, instance):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return self._process_element(config, master, instance)

    def _process_element(self, element_config, parent, instance):
        elements = {}
        for name, config in element_config.items():
            widget_type = config.pop("widget_type", None)
            if widget_type:
                widget_properties = config.get("widget_properties", {})

                if widget_type == "CTkFrame":
                    frame = self.frame_builder.create_frame(name, config, parent, instance)
                    elements[name] = frame
                    elements.update(self._process_element(config.get("children", {}), frame, instance))

                else:
                    widget = self.widget_builder.create_widget(widget_type, widget_properties, parent, instance)
                    self.apply_packing(widget, config.get("packing_properties", {}))
                    elements[name] = widget

        return elements

    @staticmethod
    def apply_packing(element, packing_config):
        for key in ['padx', 'pady', 'ipadx', 'ipady']:
            if key in packing_config:
                packing_config[key] = tuple(packing_config[key])
        packing_type = packing_config.pop("packing_type", "pack")
        getattr(element, packing_type)(**packing_config)
