# GuiFramework/gui/gui_manager/widget_builder/ctk_custom_textbox_builder.py

from GuiFramework.widgets import custom_textbox as ct
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities.logging import Logger


class CustomTextboxBuilder(AbstractCtkBuilder):
    def __init__(self, config_manager=None, localize_func=None):
        super().__init__(config_manager, localize_func)

    @property
    def widget_type(self):
        return "CustomTextbox"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CustomTextbox specific property handlers to property_handlers dict if any

            # Create CustomTextbox with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = ct.CustomTextbox(master, **widget_properties)
            self.logger.log_debug(f"CustomTextbox created with properties: {widget_properties}", "CustomTextboxBuilder")
            return widget
        except Exception as e:
            self.logger.log_error(f"Error creating CustomTextbox: {e}", "CustomTextboxBuilder")
