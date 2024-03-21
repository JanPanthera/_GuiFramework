# GuiFramework/widgets/tree_view/file_tree_view.py

import os
from functools import lru_cache

from GuiFramework.widgets.tree_view import BaseTreeView, BaseFolderNode, BaseFileNode


@lru_cache(maxsize=None)
def get_file_icon(file_path):
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
    def __init__(self, parent, path):
        super().__init__(parent, os.path.basename(path), path, get_file_icon(path))


class FolderNode(BaseFolderNode):
    def __init__(self, parent, path):
        self.expanded_icon = "📂"
        self.collapsed_icon = "📁"
        super().__init__(parent, os.path.basename(path), path, self.expanded_icon, self.collapsed_icon)

    def populate_child_nodes(self, parent):
        for entry in os.scandir(self.data):
            if entry.is_dir():
                self.child_nodes.append(FolderNode(parent, entry.path))
            else:
                self.child_nodes.append(FileNode(parent, entry.path))


class FileTreeView(BaseTreeView):
    def __init__(self, parent, root=None, expand_root_node=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root = root
        if self.root:
            self.create_tree(root, expand_root_node)

    def create_tree(self, root=None, expand_root_node=False):
        self.root = root or self.root
        if not self.root:
            raise ValueError("Root path must be set or provided before creating the tree.")

        if self.root_node:
            raise ValueError("Tree already exists. Use recreate_tree() to recreate the tree.")

        self.root_node = FolderNode(self, self.root)
        self.root_node.show()
        if expand_root_node:
            self.root_node.expand()

    def recreate_tree(self, root=None, expand_root_node=False):
        self.destroy_tree()
        self.create_tree(root, expand_root_node)
