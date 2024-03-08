# GuiFramework/gui/gui_manager/widget_builder/ctk_entry_builder.py

from customtkinter import CTkEntry
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities import setup_default_logger


class CtkEntryBuilder(AbstractCtkBuilder):
    def __init__(self, config_manager=None, localize_func=None, logger=None):
        super().__init__(config_manager, localize_func, logger)
        self.logger = logger or setup_default_logger(log_name="CtkEntryBuilder", log_directory="logs/GuiFramework")

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
            self.logger.debug(f"CTkEntry created with properties: {widget_properties}")
            return widget
        except Exception as e:
            self.logger.error(f"Error creating CTkEntry: {e}")
            return None