# GuiFramework/gui/gui_manager/widget_builder/ctk_option_menu_builder.py

from customtkinter import CTkOptionMenu
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities.logging import Logger


class CtkOptionMenuBuilder(AbstractCtkBuilder):
    def __init__(self, localize_func=None):
        super().__init__(localize_func)

    @property
    def widget_type(self):
        return "CTkOptionMenu"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply CTkOptionMenu specific property handlers to property_handlers dict if any

            # Create CTkOptionMenu with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = CTkOptionMenu(master, **widget_properties)
            self.logger.log_debug(f"CTkOptionMenu created with properties: {widget_properties}", "CtkOptionMenuBuilder")
            return widget
        except Exception as e:
            self.logger.log_error(f"Error creating CTkOptionMenu: {e}", "CtkOptionMenuBuilder")
