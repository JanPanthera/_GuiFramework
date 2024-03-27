import customtkinter as ctk

from GuiFramework.widgets.new_tree_view.base.base_file_node import BaseFileNode


class FileNode(BaseFileNode):
    def __init__(self, parent_node, parent_widget, name, data=None):
        #icon = "📄"
        icon = ""
        super().__init__(parent_node, parent_widget, name, data, optional_icon_str=icon)
