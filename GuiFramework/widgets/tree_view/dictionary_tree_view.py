# GuiFramework/widgets/tree_view/dictionary_tree_view.py

from GuiFramework.widgets.tree_view import BaseTreeView, BaseFolderNode, BaseFileNode


class FileNode(BaseFileNode):
    def __init__(self, parent, name, data):
        # appropriate icon for a data of a dictionary key
        icon = "📝"
        super().__init__(parent, name, data, icon)


class FolderNode(BaseFolderNode):
    def __init__(self, parent, name, data):
        super().__init__(parent, name, data)

    def populate_child_nodes(self, container):
        for key, value in self.data.items():
            if isinstance(value, dict):
                folder_node = FolderNode(container, key, value)
                self.child_nodes.append(folder_node)
            else:
                file_node = FileNode(container, key, value)
                self.child_nodes.append(file_node)


class DictionaryTreeView(BaseTreeView):
    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        first_key = list(data.keys())[0]
        first_key_data = data[first_key]
        self.root_node = FolderNode(self, first_key, first_key_data)
        self.root_node.show()
