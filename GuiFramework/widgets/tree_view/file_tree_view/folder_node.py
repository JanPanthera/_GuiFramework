import os

from GuiFramework.widgets.tree_view.file_tree_view.file_node import FileNode
from GuiFramework.widgets.tree_view.base.base_folder_node import BaseFolderNode


class FolderNode(BaseFolderNode):
    def __init__(self, tree_view_instance, parent_node, parent_container, node_text, data=None):
        icon = "📁"
        super().__init__(tree_view_instance, parent_node, parent_container, data, text_widget_str=node_text, icon_widget_str=icon)
        self._add_children()

    def _add_children(self):
        # iterates through self.data (its path) and adds all direct child, no recursion
        for entry in os.scandir(self.data):
            if entry.is_dir():
                folder_node = FolderNode(self.tree_view_instance, self, self.child_nodes_container, data=entry.path, node_text=entry.name)
                self.add_child(folder_node)

        for entry in os.scandir(self.data):
            if not entry.is_dir():
                file_node = FileNode(self.tree_view_instance, self, self.child_nodes_container, data=entry.path, node_text=entry.name)
                self.add_child(file_node)
