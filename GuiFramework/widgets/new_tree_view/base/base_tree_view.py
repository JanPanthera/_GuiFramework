import customtkinter as ctk


class BaseTreeView(ctk.CTkScrollableFrame):
    def __init__(self, parent_widget, *args, **kwargs):
        super().__init__(parent_widget, *args, **kwargs)
        self.root_node = None

    def add_root_node(self, node):
        if self.root_node is not None:
            raise ValueError("Root node already exists")
        self.root_node = node
        self.root_node.show()

    def clear(self):
        if self.root_node:
            self.root_node.cleanup()
            self.root_node = None
