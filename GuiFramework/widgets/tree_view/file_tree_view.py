# GuiFramework/widgets/tree_view/file_tree_view.py

import os

from typing import Any
from functools import lru_cache

from GuiFramework.widgets.tree_view import BaseTreeView, BaseFolderNode, BaseFileNode


@lru_cache(maxsize=None)
def get_file_icon(file_path: str) -> str:
    """Return the icon for a given file path."""
    if file_path.endswith((".zip", ".7z", ".tar", ".gz", ".bz2", ".xz")):
        return "📦"
    elif file_path.endswith(".iso"):
        return "💿"
    elif os.path.islink(file_path):
        return "🔗"
    elif os.path.isdir(file_path):
        return "📁"
    elif os.path.isfile(file_path):
        return "📄"
    else:
        return "📝"


class FileNode(BaseFileNode):
    def __init__(self, tree_view_instance: Any, parent_widget: Any, path: str):
        """Initialize a file node with the given path."""
        super().__init__(tree_view_instance=tree_view_instance, parent_widget=parent_widget, name=os.path.basename(path), data=path, icon_text=get_file_icon(path),)


class FolderNode(BaseFolderNode):
    def __init__(self, tree_view_instance: Any, parent_widget: Any, path: str, **kwargs):
        """Initialize a folder node with the given path."""
        self.tree_view_instance = tree_view_instance
        self.expanded_icon = "📂"
        self.collapsed_icon = "📁"
        super().__init__(tree_view_instance=tree_view_instance, parent_widget=parent_widget, name=os.path.basename(path), data=path, expanded_icon=self.expanded_icon, collapsed_icon=self.collapsed_icon, **kwargs)

    def populate_child_nodes(self, parent_widget: Any) -> None:
        """Populate child nodes for a folder node."""
        for entry in os.scandir(self.data):
            if entry.is_dir():
                self.add_child_node(FolderNode(tree_view_instance=self.tree_view_instance, parent_widget=parent_widget, path=entry.path))
            else:
                self.add_child_node(FileNode(tree_view_instance=self.tree_view_instance, parent_widget=parent_widget, path=entry.path))


class FileTreeView(BaseTreeView):
    def __init__(self, parent_widget: Any, root: str = None, multi_select: bool = False, expand_root_node: bool = False, *args, **kwargs) -> None:
        """Initialize the file tree view with the given root."""
        super().__init__(parent_widget=parent_widget, multi_select=multi_select, *args, **kwargs)
        self.root = root
        if self.root:
            self.create_tree(root, expand_root_node)

    def create_tree(self, root: str = None, expand_root_node: bool = False) -> None:
        """Create the tree with the given root."""
        self.root = root or self.root
        if not self.root:
            raise ValueError("Root path must be set or provided before creating the tree.")

        if self.root_node:
            raise ValueError("Tree already exists. Use recreate_tree() to recreate the tree.")

        self.root_node = FolderNode(tree_view_instance=self, parent_widget=self, path=self.root)
        self.root_node.show()
        if expand_root_node:
            self.root_node.expand()

    def recreate_tree(self, root: str = None, expand_root_node: bool = False) -> None:
        """Recreate the tree with the given root."""
        self.destroy_tree()
        self.create_tree(root, expand_root_node)
