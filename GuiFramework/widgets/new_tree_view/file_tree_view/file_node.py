import customtkinter as ctk

from GuiFramework.widgets.new_tree_view.base.base_file_node import BaseFileNode


class FileNode(BaseFileNode):
    def __init__(self, tree_view_instance, parent_node, parent_container, node_text, data=None):
        icon = "📄"
        super().__init__(tree_view_instance, parent_node, parent_container, data, text_widget_str=node_text, icon_widget_str=icon)
