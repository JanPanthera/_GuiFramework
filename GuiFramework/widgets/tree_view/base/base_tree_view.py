import customtkinter as ctk

from .base_file_node import BaseFileNode
from .base_folder_node import BaseFolderNode


class BaseTreeView(ctk.CTkScrollableFrame):
    def __init__(self, parent_container, single_selection=False, *args, **kwargs):
        """Initialize the tree view with optional single selection mode."""
        super().__init__(parent_container, *args, **kwargs)
        self.root_node = None
        self.single_selection = single_selection
        self.nodes = []
        self.selected_nodes: dict = {"folder": [], "file": []}

    def create_tree(self):
        """Raise NotImplementedError to enforce method override in subclasses."""
        raise NotImplementedError("Inheriting classes must implement this method")

    def recreate_tree(self, expand_root_node=False):
        """Destroy and recreate the tree structure."""
        self.destroy_tree()
        self.create_tree(expand_root_node)

    def destroy_tree(self):
        """Clean up the tree, removing all nodes."""
        if self.root_node:
            self.root_node.cleanup()
            self.root_node = None

    def add_node(self, node):
        """Add a node to the tree."""
        self.nodes.append(node)

    def remove_node(self, node):
        """Remove a node from the tree."""
        self.nodes.remove(node)

    def select_all_nodes(self):
        """Select all nodes in the tree."""
        for node in self.nodes:
            node.select()

    def select_all_file_nodes(self):
        """Select all file nodes in the tree."""
        for node in self.nodes:
            if isinstance(node, BaseFileNode):
                node.select()

    def select_all_folder_nodes(self):
        """Select all folder nodes in the tree."""
        for node in self.nodes:
            if isinstance(node, BaseFolderNode):
                node.select()

    def deselect_all_nodes(self):
        """Deselect all nodes in the tree."""
        self.deselect_all_file_nodes()
        self.deselect_all_folder_nodes()

    def deselect_all_file_nodes(self):
        """Deselect all file nodes in the tree."""
        for node in self.selected_nodes["file"]:
            node.deselect()

    def deselect_all_folder_nodes(self):
        """Deselect all folder nodes in the tree."""
        for node in self.selected_nodes["folder"]:
            node.deselect()

    def select_node(self, node):
        """Select a single node, respecting the single selection mode if enabled."""
        if self.single_selection:
            self.deselect_all_nodes()
        node_type = "folder" if isinstance(node, BaseFolderNode) else "file"
        if node not in self.selected_nodes[node_type]:
            self.selected_nodes[node_type].append(node)

    def deselect_node(self, node):
        """Deselect a single node."""
        node_type = "folder" if isinstance(node, BaseFolderNode) else "file"
        if node in self.selected_nodes[node_type]:
            self.selected_nodes[node_type].remove(node)

    def expand_all(self):
        """Expand all nodes in the tree."""
        for node in self.nodes:
            if isinstance(node, BaseFolderNode):
                node.expand()

    def collapse_all(self):
        """Collapse all nodes in the tree."""
        for node in self.nodes:
            if isinstance(node, BaseFolderNode):
                node.collapse()

    def get_selected_nodes(self) -> dict:
        """Return a dictionary of selected nodes."""
        return self.selected_nodes

    def get_selected_files(self) -> list:
        """Return a list of selected file nodes."""
        return [[node.text_widget_str, node.data] for node in self.selected_nodes["file"]]

    def get_selected_folders(self) -> list:
        """Return a list of selected folder nodes."""
        return [[node.text_widget_str, node.data] for node in self.selected_nodes["folder"]]
