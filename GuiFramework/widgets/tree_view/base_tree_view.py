# GuiFramework/widgets/tree_view/base_tree_view.py

import customtkinter as ctk

from typing import Any

from abc import abstractmethod
from GuiFramework.widgets.custom_tooltip import CustomTooltip as FWK_CustomTooltip


class BaseNode:
    """Initialize a new instance of the BaseNode class."""

    def __init__(self, parent_widget: Any, name: str = "name", data: Any = None, icon_text: str = None) -> None:
        """Raise ValueError if parent_widget is None, else initialize node."""
        if parent_widget is None:
            raise ValueError("Parent must be provided.")

        # Private properties
        self._parent_widget: Any = parent_widget
        self._node_container: Any = None
        self._icon_widget: ctk.CTkLabel = None
        self._text_widget: ctk.CTkButton = None
        self._is_visible: bool = False

        # Publicly available properties
        self.name: str = name
        self.data: Any = data

        self._init_gui(icon_text)

    def _init_gui(self, icon_text: str = None) -> None:
        """Initialize the graphical components of the node."""
        self._node_container = ctk.CTkFrame(self._parent_widget, fg_color="transparent")

        if icon_text:
            self._icon_widget = ctk.CTkLabel(
                self._node_container, text=icon_text, fg_color="transparent", anchor="nw"
            )
            self._icon_widget.pack(side="left", padx=(0, 5), pady=0, ipadx=0, ipady=0)

        self._text_widget = ctk.CTkButton(
            self._node_container, text=self.name, fg_color="transparent",
            anchor="nw", hover=False, corner_radius=0
        )
        self._text_widget.pack(side="left", padx=0, pady=0, ipadx=0, ipady=0)
        FWK_CustomTooltip(self._text_widget, self.name, delay=1000)

    @property
    def is_visible(self) -> bool:
        """Return the visibility state of the node."""
        return self._is_visible

    def show(self) -> None:
        """Show the node."""
        if not self.is_visible:
            self._node_container.pack(padx=(5, 0), pady=(5, 0), anchor="nw")
            self._is_visible = True

    def hide(self) -> None:
        """Hide the node."""
        if self.is_visible:
            self._node_container.pack_forget()
            self._is_visible = False

    def update_icon(self, new_icon_text: str) -> None:
        """Update the icon text of the node."""
        if self._icon_widget is not None:
            self._icon_widget.configure(text=new_icon_text)

    def rename(self, new_name: str) -> None:
        """Rename the node."""
        self._text_widget.configure(text=new_name)
        self.name = new_name

    def cleanup(self) -> None:
        """Clean up resources used by the node."""
        self.data = None


class BaseFileNode(BaseNode):
    """Initialize a new instance of the BaseFileNode class."""

    def __init__(self, tree_view_instance: Any, parent_widget: Any, name: str, data: Any, icon_text: str = None) -> None:
        """Raise ValueError if tree_view_instance or parent_widget is None, else initialize file node."""
        if tree_view_instance is None:
            raise ValueError("Tree View Instance must be provided.")
        if parent_widget is None:
            raise ValueError("Parent Widget must be provided.")

        self._tree_view_instance = tree_view_instance
        self._normal_color = "transparent"
        self._highlight_color = "#4d4d4d"
        self._is_selected = False

        super().__init__(parent_widget=parent_widget, name=name, data=data, icon_text=icon_text)
        self._text_widget.configure(command=self.on_select)

    @property
    def is_selected(self) -> bool:
        """Return the selection state of the node."""
        return self._is_selected

    def on_select(self) -> None:
        """Handle the node selection event, toggling the node's selection state."""
        if self.is_selected:
            self.deselect()
        else:
            if not self._tree_view_instance.multi_select:
                self._tree_view_instance.deselect_all()
            self.select()

    def select(self) -> None:
        """Mark the node as selected and update its appearance."""
        if not self.is_selected and self.is_visible:
            self._is_selected = True
            self._text_widget.configure(fg_color=self._highlight_color)

    def deselect(self) -> None:
        """Mark the node as deselected and restore its default appearance."""
        if self.is_selected and self.is_visible:
            self._is_selected = False
            self._text_widget.configure(fg_color=self._normal_color)

    def cleanup(self) -> None:
        """Perform cleanup tasks for the node, ensuring resources are properly released."""
        super().cleanup()


class BaseFolderNode(BaseNode):
    """Represent a folder node with expandable/collapsible functionality."""

    def __init__(self, tree_view_instance: Any, parent_widget: Any, name: str, data: Any, expanded_icon="▼", collapsed_icon="▶") -> None:
        """Raise ValueError if parent_widget or tree_view_instance is None, else initialize folder node."""
        if parent_widget is None:
            raise ValueError("Parent must be provided.")
        if tree_view_instance is None:
            raise ValueError("Tree View Instance must be provided.")

        self._tree_view_instance = tree_view_instance
        self._folder_node_container = None
        self._child_nodes_container = None
        self._child_nodes = []
        self._is_expanded = False

        self._collapsed_icon = collapsed_icon
        self._expanded_icon = expanded_icon

        self._folder_node_container = ctk.CTkFrame(parent_widget, fg_color="transparent")
        self._folder_node_container.pack(padx=0, pady=0, ipadx=0, ipady=0, anchor="nw")

        self._child_nodes_container = ctk.CTkFrame(self._folder_node_container, fg_color="transparent")

        super().__init__(parent_widget=self._folder_node_container, name=name, data=data, icon_text=collapsed_icon)
        self._text_widget.configure(command=self.toggle_child_nodes)

        self.populate_child_nodes(self._child_nodes_container)

    @property
    def is_expanded(self) -> bool:
        """Return the expansion state of the folder node."""
        return self._is_expanded

    @abstractmethod
    def populate_child_nodes(self, container: ctk.CTkFrame) -> None:
        """Populate the folder node with child nodes."""
        pass

    def add_child_node(self, child_node: BaseNode) -> None:
        """Add a child node to the folder node."""
        self._child_nodes.append(child_node)

    def remove_child_node(self, child_node: BaseNode) -> None:
        """Remove a child node from the folder node."""
        self._child_nodes.remove(child_node)

    def toggle_child_nodes(self) -> None:
        """Toggle the visibility of the child nodes."""
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self) -> None:
        """Show the child nodes."""
        if not self.is_expanded:
            for child_node in self._child_nodes:
                child_node.show()
            self._child_nodes_container.pack(padx=(15, 0), pady=0, anchor="nw")
            self.update_icon(self._expanded_icon)
            self._is_expanded = True

    def collapse(self) -> None:
        """Hide the child nodes."""
        if self.is_expanded:
            for child_node in self._child_nodes:
                if isinstance(child_node, BaseFileNode):
                    child_node.deselect()
                child_node.hide()
                if isinstance(child_node, BaseFolderNode):
                    child_node.collapse()
            self._child_nodes_container.pack_forget()
            self.update_icon(self._collapsed_icon)
            self._is_expanded = False

    def cleanup(self) -> None:
        """Clean up the folder node."""
        for child_node in self._child_nodes:
            child_node.cleanup()
        self._child_nodes = []
        super().cleanup()


class BaseTreeView(ctk.CTkScrollableFrame):
    def __init__(self, parent_widget: Any, multi_select: bool = False, *args, **kwargs) -> None:
        """Initialize the BaseTreeView with optional multi-selection."""
        super().__init__(parent_widget, *args, **kwargs)
        self.multi_select = multi_select
        self.root_node = None

    @abstractmethod
    def create_tree(self, *args, **kwargs) -> None:
        """Create the tree structure."""
        raise NotImplementedError

    @abstractmethod
    def recreate_tree(self, *args, **kwargs) -> None:
        """Recreate the tree structure."""
        raise NotImplementedError

    def destroy_tree(self) -> None:
        """Destroy the tree and clean up resources."""
        if self.root_node:
            self.root_node.cleanup()
            self.root_node.folder_node_container.destroy()
            self.root_node = None
        else:
            raise ValueError("Root Node must be set before destroying the tree.")

    def expand_all(self) -> None:
        """Expand all folder nodes in the tree."""
        if self.root_node:
            self._expand_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before expanding all nodes.")

    def collapse_all(self) -> None:
        """Collapse all folder nodes in the tree."""
        if self.root_node:
            self._collapse_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before collapsing all nodes.")

    def select_all(self) -> None:
        """Select all file nodes in the tree."""
        if self.root_node:
            self._select_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before selecting all nodes.")

    def deselect_all(self) -> None:
        """Deselect all file nodes in the tree."""
        if self.root_node:
            self._deselect_all(self.root_node)
        else:
            raise ValueError("Root Node must be set before deselecting all nodes.")

    def get_selected_files(self) -> dict:
        """Return a dictionary of selected files."""
        if self.root_node:
            selected_files = {}
            self._get_selected_files(self.root_node, selected_files)
            return selected_files
        else:
            raise ValueError("Root Node must be set before getting selected files.")

    def _expand_all(self, node: BaseNode) -> None:
        """Recursively expand all folder nodes starting from the given node."""
        if isinstance(node, BaseFolderNode):
            node.expand()
            for child_node in node.child_nodes:
                self._expand_all(child_node)

    def _collapse_all(self, node: BaseNode) -> None:
        """Recursively collapse all folder nodes starting from the given node."""
        if isinstance(node, BaseFolderNode):
            node.collapse()
            for child_node in node.child_nodes:
                self._collapse_all(child_node)

    def _select_all(self, node: BaseNode) -> None:
        """Recursively select all file nodes starting from the given node."""
        for child_node in node.child_nodes:
            if isinstance(child_node, BaseFolderNode):
                self._select_all(child_node)
            elif isinstance(child_node, BaseFileNode):
                child_node.select()

    def _deselect_all(self, node: BaseNode) -> None:
        """Recursively deselect all file nodes starting from the given node."""
        for child_node in node.child_nodes:
            if isinstance(child_node, BaseFolderNode):
                self._deselect_all(child_node)
            elif isinstance(child_node, BaseFileNode):
                child_node.deselect()

    def _get_selected_files(self, node: BaseNode, selected_files: dict) -> None:
        """Recursively gather selected files starting from the given node."""
        for child_node in node.child_nodes:
            if isinstance(child_node, BaseFolderNode):
                self._get_selected_files(child_node, selected_files)
            elif isinstance(child_node, BaseFileNode) and child_node.selected:
                selected_files[child_node.name] = child_node.data
