from .file_node import FileNode
from .folder_node import FolderNode

from GuiFramework.widgets.new_tree_view.base.base_tree_view import BaseTreeView

import os


class FileTreeView(BaseTreeView):
    def __init__(self, parent_widget, root_path, *args, **kwargs):
        super().__init__(parent_widget, *args, **kwargs)
        self.root_path = root_path
        self.populate_tree()

    def populate_tree(self):
        if not os.path.isdir(self.root_path):
            raise ValueError("The specified root path must be a directory.")

        # Initialize the root folder node with the root path
        root_node = FolderNode(None, self, name=os.path.basename(self.root_path) or self.root_path, data=self.root_path)
        self.add_root_node(root_node)
        self._populate_folder(root_node)

    def _populate_folder(self, folder_node):
        for entry in os.scandir(folder_node.data):
            if entry.is_dir():
                # iterate through the path and create a folder node for each directory
                # the folder itself is responsible for populating its children
                pass

    def refresh(self):
        """Refresh the entire tree view based on the current root path."""
        self.clear()  # Clear the existing tree structure
        self.populate_tree()  # Repopulate the tree
