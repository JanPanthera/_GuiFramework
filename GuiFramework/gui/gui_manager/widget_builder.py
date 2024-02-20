# widget_builder.py ~ GuiFramework/gui/gui_manager/widget_builder.py

from ...utilities import setup_default_logger


class WidgetBuilder:
    def __init__(self, logger=None):
        self.logger = logger if logger else setup_default_logger('WidgetBuilder')
        self.logger.info("WidgetBuilder initialized.")

    def create_widget(self, master, builder_instance, widget_properties):
        self.logger.debug(f"Creating widget with builder: {type(builder_instance).__name__}")
        try:
            property_handlers = builder_instance.property_handlers

            for property_name, property_value in widget_properties.items():
                property_handler = property_handlers.get(property_name)
                if property_handler:
                    widget_properties[property_name] = property_handler(property_value)

            widget = builder_instance.create_widget(master, widget_properties)
            self.logger.debug("Widget created successfully.")
            return widget
        except Exception as e:
            self.logger.error(f"Error creating widget: {e}")
            raise
