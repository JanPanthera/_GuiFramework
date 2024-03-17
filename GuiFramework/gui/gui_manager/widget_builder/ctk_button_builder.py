# GuiFramework/gui/gui_manager/widget_builder/ctk_button_builder.py

from customtkinter import CTkButton
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities.logging import Logger


class CtkButtonBuilder(AbstractCtkBuilder):
    def __init__(self, config_manager=None, localize_func=None):
        super().__init__(config_manager, localize_func)

    @property
    def widget_type(self):
        return "CTkButton"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CTkButton specific property handlers to property_handlers dict if any

            # Create CTkButton with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = CTkButton(master, **widget_properties)
            self.logger.log_debug(f"CTkButton created with properties: {widget_properties}", "CtkButtonBuilder")
            return widget
        except Exception as e:
            self.logger.log_error(f"Error creating CTkButton: {e}", "CtkButtonBuilder")
            return None

