import os

from GuiFramework.widgets.tree_view import BaseTreeView, BaseFolderNode, BaseFileNode


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
    def __init__(self, tree_view_instance, parent, path):
        super().__init__(tree_view_instance, parent, os.path.basename(path), path, get_file_icon(path))


class FolderNode(BaseFolderNode):
    def __init__(self, tree_view_instance, parent, path):
        self.tree_view_instance = parent
        self.expanded_icon = "📂"
        self.collapsed_icon = "📁"
        super().__init__(tree_view_instance, parent, os.path.basename(path), path, self.expanded_icon, self.collapsed_icon)

    def populate_child_nodes(self, parent):
        for file in os.listdir(self.data):
            file_path = os.path.join(self.data, file)
            if os.path.isdir(file_path):
                self.child_nodes.append(FolderNode(self.tree_view_instance, parent, file_path))
            else:
                self.child_nodes.append(FileNode(self.tree_view_instance, parent, file_path))


class FileTreeView(BaseTreeView):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root_node = FolderNode(self, self, root)
        self.root_node.show()
