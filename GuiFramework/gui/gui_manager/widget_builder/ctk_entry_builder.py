# GuiFramework/gui/gui_manager/widget_builder/ctk_entry_builder.py

from customtkinter import CTkEntry
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities.logging import Logger


class CtkEntryBuilder(AbstractCtkBuilder):
    def __init__(self, localize_func=None):
        super().__init__(localize_func)

    @property
    def widget_type(self):
        return "CTkEntry"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CTkEntry specific property handlers to property_handlers dict if any

            # Create CTkEntry with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = CTkEntry(master, **widget_properties)
            self.logger.log_debug(f"CTkEntry created with properties: {widget_properties}", "CtkEntryBuilder")
            return widget
        except Exception as e:
            self.logger.log_error(f"Error creating CTkEntry: {e}", "CtkEntryBuilder")
            return None

