# GuiFramework/gui/gui_manager/widget_builder/file_tree_view_builder.py

from GuiFramework.widgets import FileTreeView
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities.logging import Logger


class FileTreeViewBuilder(AbstractCtkBuilder):
    def __init__(self, localize_func=None):
        super().__init__(localize_func)

    @property
    def widget_type(self):
        return "FileTreeView"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply FileTreeView specific property handlers to property_handlers dict if any

            # Create FileTreeView with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = FileTreeView(master, **widget_properties)
            self.logger.log_debug(f"FileTreeView created with properties: {widget_properties}", "FileTreeViewBuilder")
            return widget
        except Exception as e:
            self.logger.log_error(f"Error creating FileTreeView: {e}", "FileTreeViewBuilder")
            return None
