# GuiFramework/gui/gui_manager/gui_builder.py

import json

from GuiFramework.utilities.logging import Logger


class GuiBuilder:
    def __init__(self):
        self.widget_builders = {}
        self.logger = Logger.get_logger("GuiFramework")

    def register_widget_builder(self, widget_builder):
        self.widget_builders[widget_builder.widget_type] = widget_builder

    def build(self, master, config_path, instance):
        try:
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            elements = self._process_elements(master, config, instance)
            return elements
        except (IOError, json.JSONDecodeError) as e:
            self.logger.log_error(f"Failed to read or parse config file {config_path}: {e}", "GuiBuilder")
            raise

    def _process_elements(self, parent, element_config, instance):
        elements = {}
        for name, config in element_config.items():
            widget_type = config.get("widget_type")
            if widget_type:
                builder_instance = self.widget_builders.get(widget_type)
                if builder_instance:
                    widget = self._create_widget(builder_instance, parent, config, instance)
                    self._apply_packing(builder_instance, widget, config)
                    self._apply_grid_configuration(builder_instance, widget, config)
                    child_elements = config.get("children", {})
                    if child_elements:
                        elements.update(self._process_elements(widget, child_elements, instance))
                    elements[name] = widget
        return elements

    def _create_widget(self, builder_instance, parent, config, instance):
        widget_properties = config.get("widget_properties", {})
        if hasattr(builder_instance, "create_widget"):
            return builder_instance.create_widget(parent, widget_properties, instance)

    def _apply_packing(self, builder_instance, widget, config):
        packing_properties = config.get("packing_properties", {})
        if hasattr(builder_instance, "apply_packing") and packing_properties:
            builder_instance.apply_packing(widget, packing_properties)

    def _apply_grid_configuration(self, builder_instance, widget, config):
        grid_configuration = config.get("grid_configuration", {})
        if hasattr(builder_instance, "apply_grid_configuration") and grid_configuration:
            builder_instance.apply_grid_configuration(widget, grid_configuration)