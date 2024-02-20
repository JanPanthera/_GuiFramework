# gui_builder.py ~ GuiFramework/gui/gui_manager/gui_builder.py

import json

from .widget_builder import WidgetBuilder
from ...utilities import setup_default_logger


class GuiBuilder:
    def __init__(self, logger=None):
        self.logger = logger if logger else setup_default_logger('GuiBuilder')
        self.widget_builder = WidgetBuilder(self.logger)
        self.widget_builders = {}
        self.logger.info("Initialized GuiBuilder.")

    def register_widget_builder(self, widget_builder):
        self.widget_builders[widget_builder.widget_type] = widget_builder
        self.logger.debug(f"Registered widget builder for type: {widget_builder.widget_type}")

    def build(self, master, config_path):
        self.logger.info(f"Starting to build GUI from config: {config_path}")
        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            elements = self._process_element(config, master)
            self.logger.info("GUI build completed successfully.")
            return elements
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to read or parse config file {config_path}: {e}")
            raise

    def _process_element(self, element_config, master):
        elements = {}
        for name, config in element_config.items():
            try:
                widget_type = config.get("widget_type")
                self.logger.debug(f"Processing widget: {name} of type: {widget_type}")

                if widget_type:
                    builder_instance = self.widget_builders.get(widget_type)
                    if not builder_instance:
                        self.logger.error(f"Widget builder not found for widget type: {widget_type}")
                        continue

                    widget = self.widget_builder.create_widget(master, builder_instance, config.get("widget_properties", {}))
                    self._apply_widget_properties(builder_instance, widget, config)

                    child_elements = config.get("children", {})
                    if child_elements:
                        elements.update(self._process_element(child_elements, widget))

                    elements[name] = widget

                self.logger.debug(f"Completed processing widget: {name}")
            except Exception as e:
                self.logger.error(f"Error processing widget {name}: {e}")
        return elements

    def _apply_widget_properties(self, builder_instance, widget, config):
        if "packing_properties" in config and hasattr(builder_instance, "apply_packing"):
            builder_instance.apply_packing(widget, config["packing_properties"])

        if "grid_configuration" in config and hasattr(builder_instance, "apply_grid_configuration"):
            builder_instance.apply_grid_configuration(widget, config["grid_configuration"])