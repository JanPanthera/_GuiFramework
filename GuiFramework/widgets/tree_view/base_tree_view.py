# GuiFramework/widgets/tree_view/base_tree_view.py

import customtkinter as ctk

from abc import abstractmethod
from GuiFramework.utilities import EventManager


class BaseNode:
    """Base class for nodes."""

    def __init__(self, parent, name, data=None, icon_text=None):
        self.name = name
        self.data = data
        self.icon_text = icon_text
        self.visible = False

        self.node_container = ctk.CTkFrame(parent, fg_color="transparent")

        if icon_text:
            self.icon_label = ctk.CTkLabel(self.node_container, text=icon_text, fg_color="transparent", anchor="nw")
            self.icon_label.pack(side="left", padx=(0, 5), pady=0, ipadx=0, ipady=0)
        else:
            self.icon_label = None

        self.controller = ctk.CTkButton(self.node_container, text=name, fg_color="transparent", anchor="nw", hover=False, corner_radius=0)
        self.controller.pack(side="left", padx=0, pady=0, ipadx=0, ipady=0)

    def show(self):
        """Makes the node"s container visible."""
        if not self.visible:
            self.node_container.pack(padx=(20, 0), pady=(5, 0), anchor="nw")
            self.visible = True

    def hide(self):
        """Hides the node"s container."""
        if self.visible:
            self.node_container.pack_forget()
            self.visible = False

    def update_icon(self, new_icon_text):
        """Updates the icon of the node."""
        if self.icon_label is not None:
            self.icon_label.configure(text=new_icon_text)

    def rename(self, new_name):
        """Renames the node."""
        self.controller.configure(text=new_name)
        self.name = new_name

    def cleanup(self):
        """Cleans up the node."""
        self.data = None


class BaseFileNode(BaseNode):
    """Base class for file nodes."""

    def __init__(self, parent, name, data=None, icon=None):
        super().__init__(parent, name, data, icon)
        self.selected = False
        self.controller.configure(command=self.on_select)

    def on_select(self):
        """Toggles the selection of the file node."""
        if self.selected:
            self.deselect()
        else:
            EventManager.notify("deselect_all_files", single_select=True)
            self.select()

    def select(self):
        """Selects the file node."""
        if not self.selected and self.visible:
            self.selected = True
            self.controller.configure(fg_color="#4d4d4d")
            EventManager.notify("file_selected", self)

    def deselect(self):
        """Deselects the file node."""
        if self.selected and self.visible:
            self.selected = False
            self.controller.configure(fg_color="transparent")
            EventManager.notify("file_deselected", self)

    def cleanup(self):
        """Cleans up the file node."""
        super().cleanup()


class BaseFolderNode(BaseNode):
    """Base class for folder nodes."""

    def __init__(self, parent, name, data=None, expanded_icon=None, collapsed_icon=None):
        self.expanded_icon = expanded_icon or "▼"
        self.collapsed_icon = collapsed_icon or "▶"

        self.folder_node_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.folder_node_container.pack(padx=0, pady=0, ipadx=0, ipady=0, anchor="nw")

        self.child_nodes_container = ctk.CTkFrame(self.folder_node_container, fg_color="transparent")

        super().__init__(self.folder_node_container, name, data, self.collapsed_icon)
        self.controller.configure(command=self.toggle_child_nodes)

        self.child_nodes = []
        self.expanded = False
        self.populate_child_nodes(self.child_nodes_container)

    @abstractmethod
    def populate_child_nodes(self, container):
        raise NotImplementedError

    def add_child_node(self, child_node):
        """Adds a child node to the folder node."""
        self.child_nodes.append(child_node)
        EventManager.notify("child_node_added", child_node)

    def remove_child_node(self, child_node):
        """Removes a child node from the folder node."""
        self.child_nodes.remove(child_node)
        EventManager.notify("child_node_removed", child_node)

    def toggle_child_nodes(self):
        """Toggles the visibility of the child nodes."""
        if self.expanded:
            self.collapse()
            EventManager.notify("folder_collapsed", self)
        else:
            self.expand()
            EventManager.notify("folder_expanded", self)

    def expand(self):
        """Shows the child nodes."""
        if not self.expanded:
            for child_node in self.child_nodes:
                child_node.show()
            self.child_nodes_container.pack(padx=(15, 0), pady=0, anchor="nw")
            self.update_icon(self.expanded_icon)
            self.expanded = True

    def collapse(self):
        """Hides the child nodes."""
        if self.expanded:
            for child_node in self.child_nodes:
                if isinstance(child_node, BaseFileNode):
                    child_node.deselect()
                child_node.hide()
                if isinstance(child_node, BaseFolderNode):
                    child_node.collapse()
            self.child_nodes_container.pack_forget()
            self.update_icon(self.collapsed_icon)
            self.expanded = False

    def cleanup(self):
        """Cleans up the file node."""
        for child_node in self.child_nodes:
            child_node.cleanup()
        self.child_nodes = []
        super().cleanup()


class BaseTreeView(ctk.CTkScrollableFrame):
    def __init__(self, parent, multi_select=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        EventManager.subscribe("deselect_all_files", self.deselect_all)
        self.multi_select = multi_select
        self.root_node = None

    # Public methods
    @abstractmethod
    def create_tree(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def recreate_tree(self, *args, **kwargs):
        raise NotImplementedError

    def destroy_tree(self):
        if self.root_node:
            self.root_node.cleanup()
            self.root_node.folder_node_container.destroy()
            self.root_node = None
        else:
            raise ValueError("Root Node must be set before destroying the tree.")

    def expand_all(self):
        if self.root_node:
            self._expand_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before expanding all nodes.")

    def collapse_all(self):
        if self.root_node:
            self._collapse_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before collapsing all nodes.")

    def select_all(self):
        if self.root_node:
            self._select_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before selecting all nodes.")

    def deselect_all(self, **kwargs):
        if kwargs.get("single_select", False) and self.multi_select:
            return
        if self.root_node:
            self._deselect_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before deselecting all nodes.")

    def get_selected_files(self):
        if self.root_node:
            selected_files = {}
            self._get_selected_files(self.root_node, selected_files)
            return selected_files
        else:
            raise ValueError("Root Node must be set before getting selected files.")

    # Private methods
    def _expand_all(self, node):
        if isinstance(node, BaseFolderNode):
            node.expand()
            for child_node in node.child_nodes:
                self._expand_all(child_node)

    def _collapse_all(self, node):
        if isinstance(node, BaseFolderNode):
            node.collapse()
            for child_node in node.child_nodes:
                self._collapse_all(child_node)

    def _select_all(self, node):
        for child_node in node.child_nodes:
            if isinstance(child_node, BaseFolderNode):
                self._select_all(child_node)
            elif isinstance(child_node, BaseFileNode):
                child_node.select()

    def _deselect_all(self, node):
        for child_node in node.child_nodes:
            if isinstance(child_node, BaseFolderNode):
                self._deselect_all(child_node)
            elif isinstance(child_node, BaseFileNode):
                child_node.deselect()

    def _get_selected_files(self, node, selected_files):
        for child_node in node.child_nodes:
            if isinstance(child_node, BaseFolderNode):
                self._get_selected_files(child_node, selected_files)
            elif isinstance(child_node, BaseFileNode) and child_node.selected:
                selected_files[child_node.name] = child_node.data
