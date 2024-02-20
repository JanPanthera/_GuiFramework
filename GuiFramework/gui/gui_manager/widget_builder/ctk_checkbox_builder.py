# ctk_checkbox_builder.py ~ GuiFramework/gui/gui_manager/widget_builder/ctk_checkbox_builder.py

from customtkinter import CTkCheckBox
from .abstract_ctk_builder import AbstractCtkBuilder
from ....utilities import setup_default_logger


class CtkCheckBoxBuilder(AbstractCtkBuilder):
    def __init__(self, config_manager=None, localize_func=None, logger=None):
        super().__init__(config_manager, localize_func, logger)
        self.logger = logger or setup_default_logger('CtkCheckBoxBuilder')

    @property
    def widget_type(self):
        return 'CTkCheckBox'

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CTkCheckBox specific property handlers to property_handlers dict if any

            # Create CTkCheckBox with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = CTkCheckBox(master, **widget_properties)
            self.logger.debug(f"CTkCheckBox created with properties: {widget_properties}")
            return widget
        except Exception as e:
            self.logger.error(f"Error creating CTkCheckBox: {e}")
            return None