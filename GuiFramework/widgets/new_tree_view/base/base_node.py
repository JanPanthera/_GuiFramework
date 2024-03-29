import customtkinter as ctk
from typing import Optional, Any, Tuple


class BaseNode:
    DEFAULT_ICON_FONT_FAMILY = "Consolas"
    DEFAULT_FONT_FAMILY = "Segoe UI"
    DEFAULT_PADX = (0, 2)
    DEFAULT_PADY = (2, 2)
    DEFAULT_SELECTION_COLOR = "#4d4d4d"
    ICON_SIZE = (20, 20)

    def __init__(self, tree_view_instance, parent_node: Optional["BaseNode"], parent_container: ctk.CTkFrame, data: Optional[Any] = None, **kwargs):
        """Initialize the node with optional data and configuration."""
        self.tree_view_instance = tree_view_instance
        self.parent_node = parent_node
        self.parent_container = parent_container
        self.data = data

        self.node_container: ctk.CTkFrame = None
        self.node_frame: ctk.CTkFrame = None
        self.text_widget: ctk.CTkLabel = None
        self.icon_widget: ctk.CTkLabel = None

        self.icon_font = ctk.CTkFont(family=kwargs.pop("icon_font", self.DEFAULT_ICON_FONT_FAMILY))
        self.text_font = ctk.CTkFont(family=kwargs.pop("text_font", self.DEFAULT_FONT_FAMILY))
        self.icon_size = kwargs.pop("icon_size", self.ICON_SIZE)

        self.selection_color = kwargs.pop("selection_color", self.DEFAULT_SELECTION_COLOR)

        self._validate_icon_size()

        self.text_widget_str: str = kwargs.pop("text_widget_str", "NoName")
        self.text_widget_padx: Tuple[int, int] = kwargs.pop("text_widget_padx", self.DEFAULT_PADX)
        self.text_widget_pady: Tuple[int, int] = kwargs.pop("text_widget_pady", self.DEFAULT_PADY)

        self.icon_widget_str: str = kwargs.pop("icon_widget_str", "")
        self.icon_widget_padx: Tuple[int, int] = kwargs.pop("icon_widget_padx", self.DEFAULT_PADX)
        self.icon_widget_pady: Tuple[int, int] = kwargs.pop("icon_widget_pady", self.DEFAULT_PADY)

        self.is_visible: bool = False
        self.is_selected: bool = False
        self.is_root: bool = kwargs.pop("is_root", False)

        self._init_gui()

    def _validate_icon_size(self):
        """Ensure the icon size is a valid tuple."""
        if isinstance(self.icon_size, int):
            self.icon_size = (self.icon_size, self.icon_size)
        elif isinstance(self.icon_size, tuple) and len(self.icon_size) != 2:
            self.icon_size = (self.icon_size[0], self.icon_size[0])
        else:
            self.icon_size = self.ICON_SIZE

    def _init_gui(self):
        """Initialize the graphical user interface of the node."""
        self.node_container = ctk.CTkFrame(self.parent_container, fg_color="transparent", corner_radius=0)

        self.node_frame = ctk.CTkFrame(self.node_container, fg_color="transparent", corner_radius=0)
        self.node_frame.pack(side="top", anchor="nw")

        self.node_representation_frame = ctk.CTkFrame(self.node_frame, fg_color="transparent", corner_radius=0)
        self.node_representation_frame.pack(side="left", anchor="nw")

        if self.icon_widget_str:
            self.icon_widget = ctk.CTkLabel(
                self.node_representation_frame, text=self.icon_widget_str,
                fg_color="transparent", corner_radius=0,
                width=self.icon_size[0], height=self.icon_size[1],
                font=self.icon_font
            )
            self.icon_widget.bind("<Button-1>", self.toggle_selection)
            self.icon_widget.pack(side="left", anchor="nw", fill="both", padx=self.icon_widget_padx, pady=self.icon_widget_pady)

        self.text_widget = ctk.CTkLabel(
            self.node_representation_frame, text=self.text_widget_str,
            fg_color="transparent", corner_radius=0,
            width=self.icon_size[0], height=self.icon_size[1],
            font=self.text_font
        )
        self.text_widget.bind("<Button-1>", self.toggle_selection)
        self.text_widget.pack(side="left", anchor="nw", fill="both", padx=self.text_widget_padx, pady=self.text_widget_pady)

    def show(self):
        """Make the node visible."""
        if not self.is_visible:
            self.node_frame.pack(side="top", anchor="nw")
            self.is_visible = True

    def hide(self):
        """Hide the node."""
        if self.is_visible:
            self.node_frame.pack_forget()
            self.is_visible = False

    def toggle_selection(self, event=None):
        """Toggle the selection state of the node."""
        self.deselect() if self.is_selected else self.select()

    def select(self):
        """Select the node and apply the selection color."""
        if self.tree_view_instance.single_selection:
            for node in self.tree_view_instance.get_selected_nodes():
                node.deselect()
        if self.icon_widget:
            self.icon_widget.configure(fg_color=self.selection_color)
        self.text_widget.configure(fg_color=self.selection_color)
        self.node_representation_frame.configure(fg_color=self.selection_color)
        self.is_selected = True
        self.on_select()

    def on_select(self):
        """Handle additional actions upon selection."""
        raise NotImplementedError("on_select method must be implemented in subclass")

    def deselect(self):
        """Deselect the node and revert the selection color."""
        if self.icon_widget:
            self.icon_widget.configure(fg_color="transparent")
        self.text_widget.configure(fg_color="transparent")
        self.node_representation_frame.configure(fg_color="transparent")
        self.is_selected = False
        self.on_deselect()

    def on_deselect(self):
        """Handle additional actions upon deselection."""
        raise NotImplementedError("on_deselect method must be implemented in subclass")

    def cleanup(self):
        """Clean up resources and destroy the node container."""
        self.data = None
        self.node_container.destroy()
