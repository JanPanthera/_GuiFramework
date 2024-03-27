import os
import customtkinter as ctk

from GuiFramework.widgets.new_tree_view.file_tree_view.file_node import FileNode
from GuiFramework.widgets.new_tree_view.base.base_folder_node import BaseFolderNode


class FolderNode(BaseFolderNode):
    def __init__(self, parent_node, parent_widget, name, data=None):
        #icons = "📁"
        icons = ""
        super().__init__(parent_node, parent_widget, name, data, optional_icon_str=icons)
        self._add_children()

    def _add_children(self):
        # iterates through self.data (its path) and adds all direct child, no recursion
        for entry in os.scandir(self.data):
            if entry.is_dir():
                folder_node = FolderNode(self, self.child_nodes_container, name=entry.name, data=entry.path)
                self.add_child(folder_node)

        for entry in os.scandir(self.data):
            if not entry.is_dir():
                file_node = FileNode(self, self.child_nodes_container, name=entry.name, data=entry.path)
                self.add_child(file_node)
