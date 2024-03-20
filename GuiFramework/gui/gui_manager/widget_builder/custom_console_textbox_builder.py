# GuiFramework/gui/gui_manager/widget_builder/custom_console_textbox_builder.py

from GuiFramework.widgets import custom_console_textbox as cct
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities.logging import Logger


class CustomConsoleTextboxBuilder(AbstractCtkBuilder):
    def __init__(self, localize_func=None):
        super().__init__(localize_func)

    @property
    def widget_type(self):
        return "CustomConsoleTextbox"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CustomConsoleTextbox specific property handlers to property_handlers dict if any

            # Create CustomConsoleTextbox with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = cct.CustomConsoleTextbox(master, **widget_properties)
            self.logger.log_debug(f"CustomConsoleTextbox created with properties: {widget_properties}", "CustomConsoleTextboxBuilder")
            return widget
        except Exception as e:
            self.logger.log_error(f"Error creating CustomConsoleTextbox: {e}", "CustomConsoleTextboxBuilder")
