import customtkinter as ctk

from typing import Any, Optional, Union, Tuple

from .base_node import BaseNode
from .base_file_node import BaseFileNode

from GuiFramework.utilities.utils import Utils


class BaseFolderNode(BaseNode):
    DEFAULT_FONT_FAMILY = "Segoe UI"
    DEFAULT_ICON_FONT_FAMILY = "Segoe UI Symbol"
    DEFAULT_PADX = (0, 4)
    DEFAULT_PADY = (0, 0)
    DEFAULT_STATE_ICONS = ("▼", "▶")
    ICON_SIZE = (20, 20)

    def __init__(
        self, parent_node, parent_widget,
        name: str, data: Any = None,
        **kwargs
    ):
        super().__init__(parent_node, parent_widget, name, data)
        self.child_nodes_container = None
        self.folder_node_container = None

        self.state_icons_widget = None
        self.optional_icon_widget = None
        self.text_widget = None

        self.is_expanded = False
        self.child_nodes = []

        self._setup_parameters(kwargs)
        self._init_gui()

    def _setup_parameters(self, kwargs):
        params = {
            'icon_size': self.ICON_SIZE,
            'icon_font': ctk.CTkFont(family=self.DEFAULT_ICON_FONT_FAMILY),
            'text_font': ctk.CTkFont(family=self.DEFAULT_FONT_FAMILY),
            'text_padx': (0, 0),
            'text_pady': self.DEFAULT_PADY,
            'state_icons_str': self.DEFAULT_STATE_ICONS,
            'state_icons_padx': self.DEFAULT_PADX,
            'state_icons_pady': self.DEFAULT_PADY,
            'optional_icon_str': None,
            'optional_icon_padx': self.DEFAULT_PADX,
            'optional_icon_pady': self.DEFAULT_PADY
        }
        for key, default in params.items():
            setattr(self, key, kwargs.get(key, default))

    def _init_gui(self):
        self._create_state_icon_button()
        self._create_folder_node_container()
        self._create_optional_icon_label()
        self._create_text_label()
        self._create_child_nodes_container()

    def _create_state_icon_button(self):
        self.state_icons_widget = ctk.CTkButton(
            self.node_container, text=self.state_icons_str[1],
            fg_color="transparent", corner_radius=0,
            width=self.icon_size[0], height=self.icon_size[1],
            font=self.icon_font,
            command=self.toggle_expansion
        )
        self.state_icons_widget.grid(row=0, column=0, padx=self.state_icons_padx, pady=self.state_icons_pady, sticky="w")

    def _create_folder_node_container(self):
        self.folder_node_container = ctk.CTkFrame(
            self.node_container, fg_color="blue", corner_radius=0
        )
        self.folder_node_container.grid(row=0, column=1, sticky="w")
        self.folder_node_container.columnconfigure(0, weight=0)
        self.folder_node_container.columnconfigure(1, weight=1)

    def _create_optional_icon_label(self):
        if self.optional_icon_str:
            icon_to_display = self.optional_icon_str[0] if isinstance(self.optional_icon_str, tuple) else self.optional_icon_str
            self.optional_icon_widget = ctk.CTkLabel(
                self.folder_node_container, text=icon_to_display,
                fg_color="transparent", corner_radius=0,
                width=self.icon_size[0], height=self.icon_size[1],
                font=self.icon_font
            )
            self.optional_icon_widget.grid(row=0, column=0, padx=self.optional_icon_padx, pady=self.optional_icon_pady, sticky="w")

    def _create_text_label(self):
        self.text_widget = ctk.CTkLabel(
            self.folder_node_container, text=self.name,
            fg_color="transparent", corner_radius=0,
            width=self.icon_size[0], height=self.icon_size[1],
            font=self.text_font
        )
        self.text_widget.grid(row=0, column=1, padx=self.text_padx, pady=self.text_pady, sticky="w")

    def _create_child_nodes_container(self):
        self.child_nodes_container = ctk.CTkFrame(
            self.node_container, fg_color="green",
            corner_radius=0
        )

    def add_child(self, child_node, show=False):
        self.child_nodes.append(child_node)
        child_node.node_container.update()
        padx = (self.state_icons_widget.winfo_width() / Utils.get_dpi_scaling_factor() + self.state_icons_padx[1], 0) if isinstance(child_node, BaseFileNode) else 0
        child_node.node_container.pack(side="top", anchor="w", padx=padx)

    def remove_child(self, child_node):
        if child_node in self.child_nodes:
            self.child_nodes.remove(child_node)
            child_node.cleanup()

    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        self.state_icons_widget.configure(text=self.state_icons_str[0] if self.is_expanded else self.state_icons_str[1])

        if isinstance(self.optional_icon_str, tuple) and self.optional_icon_widget:
            self.optional_icon_widget.configure(text=self.optional_icon_str[1] if self.is_expanded else self.optional_icon_str[0])

        self.expand() if self.is_expanded else self.collapse()

    def expand(self):
        self.child_nodes_container.grid(row=1, column=1, sticky="w")

    def collapse(self):
        self.child_nodes_container.grid_forget()

    def cleanup(self):
        for child_node in self.child_nodes:
            child_node.cleanup()
        self.child_nodes.clear()
        self.child_nodes_container.destroy()
        super().cleanup()
