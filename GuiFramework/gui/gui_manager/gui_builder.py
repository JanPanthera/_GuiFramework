# gui_builder.py ~ GuiFramework/gui/gui_manager/gui_builder.py

import json

from ...utilities import setup_default_logger


class GuiBuilder:
    def __init__(self, logger=None):
        self.logger = logger or setup_default_logger('GuiBuilder')
        self.widget_builders = {}
        self.logger.info("Initialized GuiBuilder.")

    def register_widget_builder(self, widget_builder):
        self.widget_builders[widget_builder.widget_type] = widget_builder
        self.logger.debug(f"Registered widget builder for type: {widget_builder.widget_type}")

    def build(self, master, config_path, instance):
        self.logger.info(f"Starting to build GUI from config: {config_path}")
        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            elements = self._process_element(master, config, instance)
            self.logger.info("GUI build completed successfully.")
            return elements
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to read or parse config file {config_path}: {e}")
            raise

    def _process_element(self, parent, element_config, instance):
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

                    widget_properties = config.get("widget_properties", {})
                    if hasattr(builder_instance, "create_widget"):
                        widget = builder_instance.create_widget(parent, widget_properties, instance)

                    packing_properties = config.get("packing_properties", {})
                    if hasattr(builder_instance, "apply_packing") and packing_properties:
                        builder_instance.apply_packing(widget, packing_properties)

                    grid_configuration = config.get("grid_configuration", {})
                    if hasattr(builder_instance, "apply_grid_configuration") and grid_configuration:
                        builder_instance.apply_grid_configuration(widget, grid_configuration)

                    child_elements = config.get("children", {})
                    if child_elements:
                        elements.update(self._process_element(widget, child_elements, instance))

                    elements[name] = widget

                self.logger.debug(f"Completed processing widget: {name}")
            except Exception as e:
                self.logger.error(f"Error processing widget {name}: {e}")
        return elements
