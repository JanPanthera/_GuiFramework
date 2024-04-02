import os

from GuiFramework.widgets.tree_view.base.base_file_node import BaseFileNode


class FileIconProvider:
    # Mapping of file extensions to icons
    FILE_ICONS = {
        ".zip": "📦",
        ".7z": "📦",
        ".tar": "📦",
        ".gz": "📦",
        ".bz2": "📦",
        ".xz": "📦",
        ".py": "🐍",
        ".iso": "💿",
        # Add more mappings as needed
    }

    @staticmethod
    def get_file_icon(file_path: str) -> str:
        """Return the icon for a given file path using a dictionary for mapping."""
        if os.path.islink(file_path):
            return "🔗"
        elif os.path.isdir(file_path):
            return "📁"
        elif os.path.isfile(file_path):
            # Check file extension and return the corresponding icon
            _, ext = os.path.splitext(file_path)
            return FileIconProvider.FILE_ICONS.get(ext, "📄")  # Default to generic file icon
        else:
            return "📝"


class FileNode(BaseFileNode):
    def __init__(self, tree_view_instance, parent_node, parent_container, node_text, data=None):
        super().__init__(tree_view_instance, parent_node, parent_container, data, text_widget_str=node_text, icon_widget_str=FileIconProvider.get_file_icon(data))
