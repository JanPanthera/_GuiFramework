import customtkinter as ctk

from typing import Any

from .base_node import BaseNode
from .base_file_node import BaseFileNode


class BaseFolderNode(BaseNode):
    DEFAULT_STATE_ICONS = ("▼", "▶")

    def __init__(self, tree_view_instance, parent_node, parent_container, data: Any = None, **kwargs):
        folder_selectable = tree_view_instance.folder_selectable
        super().__init__(tree_view_instance, parent_node, parent_container, data, selectable=folder_selectable, **kwargs)
        self.child_nodes_container = None

        self.state_icon_widget = None
        self.state_icon_str = kwargs.get("state_icon_str", self.DEFAULT_STATE_ICONS)
        self.state_icon_padx = kwargs.get("state_icon_padx", self.DEFAULT_PADX)
        self.state_icon_pady = kwargs.get("state_icon_pady", self.DEFAULT_PADY)

        self.is_expanded = False
        self.child_nodes = []

        self._setup_folder_gui()

    def _setup_folder_gui(self):
        self.state_icon_widget = ctk.CTkButton(
            self.node_frame, text=self.state_icon_str[1],
            fg_color="transparent", corner_radius=0,
            width=self.icon_size[0], height=self.icon_size[1],
            font=self.icon_font,
            command=self.toggle_expansion
        )
        self.state_icon_widget.pack(side="left", anchor="nw", fill="both", before=self.icon_widget or self.text_widget)
        self.node_container.pack(side="top", anchor="nw")

        self.child_nodes_container = ctk.CTkFrame(
            self.node_container,
            fg_color="transparent", corner_radius=0,
            height=0
        )

    def add_child(self, child_node):
        child_node.node_container.pack(side="top", anchor="nw", padx=(self.icon_size[0], 0) if isinstance(child_node, BaseFileNode) else None)
        self.child_nodes.append(child_node)

    def remove_child(self, child_node):
        if child_node in self.child_nodes:
            self.child_nodes.remove(child_node)
            self.child_nodes_container.configure(height=0)

    def toggle_expansion(self):
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        self.state_icon_widget.configure(text=self.state_icon_str[0])
        self.child_nodes_container.pack(side="top", anchor="nw", padx=(self.icon_size[0], 0))
        self.is_expanded = True

    def collapse(self):
        self.state_icon_widget.configure(text=self.state_icon_str[1])
        for child_node in self.child_nodes:
            if isinstance(child_node, BaseFolderNode):
                child_node.collapse()
            child_node.deselect()
        self.child_nodes_container.pack_forget()
        self.is_expanded = False

    def cleanup(self):
        for child_node in self.child_nodes:
            child_node.cleanup()
        self.child_nodes.clear()
        self.child_nodes_container.destroy()
        super().cleanup()
