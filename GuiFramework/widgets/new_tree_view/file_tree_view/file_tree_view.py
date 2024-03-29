from .file_node import FileNode
from .folder_node import FolderNode

from GuiFramework.widgets.new_tree_view.base.base_tree_view import BaseTreeView

import os


class FileTreeView(BaseTreeView):
    def __init__(self, parent_container, root_path, *args, **kwargs):
        super().__init__(parent_container, *args, **kwargs)
        self.root_path = root_path
        self.populate_tree()

    def populate_tree(self):
        if not os.path.isdir(self.root_path):
            raise ValueError("The specified root path must be a directory.")

        # Initialize the root folder node with the root path
        root_node = FolderNode(self, parent_node=None, parent_container=self, data=self.root_path, node_text=os.path.basename(self.root_path), is_root=True)
        self.add_root_node(root_node)

    def refresh(self):
        """Refresh the entire tree view based on the current root path."""
        self.clear()  # Clear the existing tree structure
        self.populate_tree()  # Repopulate the tree
