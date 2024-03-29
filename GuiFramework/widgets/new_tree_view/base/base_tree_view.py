import customtkinter as ctk


class BaseTreeView(ctk.CTkScrollableFrame):
    def __init__(self, parent_container, *args, **kwargs):
        super().__init__(parent_container, *args, **kwargs)
        self.root_node = None
        self.single_selection = kwargs.get("single_selection", True)
        self.selected_nodes: dict = {"folder": [], "file": []}

    def get_selected_nodes(self) -> list:
        return self.selected_nodes["folder"] + self.selected_nodes["file"]

    def get_selected_folders(self) -> list:
        return self.selected_nodes["folder"]

    def get_selected_files(self) -> list:
        return self.selected_nodes["file"]

    def add_root_node(self, node):
        if self.root_node is not None:
            raise ValueError("Root node already exists")
        self.root_node = node
        self.root_node.show()

    def clear(self):
        if self.root_node:
            self.root_node.cleanup()
            self.root_node = None
