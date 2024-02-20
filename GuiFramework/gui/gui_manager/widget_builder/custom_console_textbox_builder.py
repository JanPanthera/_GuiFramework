# custom_console_textbox_builder.py ~ GuiFramework/gui/gui_manager/widget_builder/custom_console_textbox_builder.py

from GuiFramework.widgets import custom_console_textbox as cct
from .abstract_ctk_builder import AbstractCtkBuilder
from ....utilities import setup_default_logger


class CustomConsoleTextboxBuilder(AbstractCtkBuilder):
    def __init__(self, config_manager=None, localize_func=None, logger=None):
        super().__init__(config_manager, localize_func, logger)
        self.logger = logger or setup_default_logger('CustomConsoleTextboxBuilder')

    @property
    def widget_type(self):
        return 'CustomConsoleTextbox'

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CustomConsoleTextbox specific property handlers to property_handlers dict if any

            # Create CustomConsoleTextbox with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = cct.CustomConsoleTextbox(master, **widget_properties)
            self.logger.debug(f"CustomConsoleTextbox created with properties: {widget_properties}")
            return widget
        except Exception as e:
            self.logger.error(f"Error creating CustomConsoleTextbox: {e}")
            return None