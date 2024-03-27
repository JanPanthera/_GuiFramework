import customtkinter as ctk

from .base_tree_view import BaseTreeView


class BaseNode:
    def __init__(self, parent_node, parent_widget, name, data=None):
        self.parent_node = parent_node
        self.parent_widget = parent_widget
        self.name = name
        self.data = data
        self.is_root = None if parent_node is None else False
        self.is_visible = False
        self.node_container = ctk.CTkFrame(parent_widget, fg_color="transparent")

    def show(self, padx=0, pady=0):
        if not self.is_visible:
            self.node_container.pack(padx=padx, pady=pady, anchor="nw")
            self.is_visible = True

    def hide(self):
        if self.is_visible:
            self.node_container.pack_forget()
            self.is_visible = False

    def cleanup(self):
        self.data = None
        self.node_container.destroy()
