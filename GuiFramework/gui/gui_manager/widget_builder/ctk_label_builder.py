# GuiFramework/gui/gui_manager/widget_builder/ctk_label_builder.py

from customtkinter import CTkLabel
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities.logging import Logger


class CtkLabelBuilder(AbstractCtkBuilder):
    def __init__(self, localize_func=None):
        super().__init__(localize_func)

    @property
    def widget_type(self):
        return "CTkLabel"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CTkLabel specific property handlers to property_handlers dict if any

            # Create CTkLabel with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = CTkLabel(master, **widget_properties)
            self.logger.log_debug(f"CTkLabel created with properties: {widget_properties}", "CtkLabelBuilder")
            return widget
        except Exception as e:
            self.logger.log_error(f"Error creating CTkLabel: {e}", "CtkLabelBuilder")
