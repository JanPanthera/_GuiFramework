import customtkinter as ctk

from typing import Any

from .base_node import BaseNode


class BaseFileNode(BaseNode):
    DEFAULT_FONT_FAMILY = "Segoe UI"
    DEFAULT_ICON_FONT_FAMILY = "Segoe UI Symbol"
    DEFAULT_PADX = (0, 4)
    DEFAULT_PADY = (0, 0)
    ICON_SIZE = (20, 20)

    def __init__(
        self, parent_node, parent_widget,
        name: str, data: Any = None,
        **kwargs
    ):
        super().__init__(parent_node, parent_widget, name, data)

        self.file_node_container = None
        self.optional_icon_widget = None
        self.text_widget = None

        self._setup_parameters(kwargs)
        self._init_gui()

    def _setup_parameters(self, kwargs):
        default_params = {
            'icon_size': self.ICON_SIZE,
            'icon_font': ctk.CTkFont(family=self.DEFAULT_ICON_FONT_FAMILY),
            'text_font': ctk.CTkFont(family=self.DEFAULT_FONT_FAMILY),
            'text_padx': (0, 0),
            'text_pady': self.DEFAULT_PADY,
            'optional_icon_str': None,
            'optional_icon_padx': self.DEFAULT_PADX,
            'optional_icon_pady': self.DEFAULT_PADY
        }
        for key, default in default_params.items():
            setattr(self, key, kwargs.get(key, default))

    def _init_gui(self):
        self.file_node_container = ctk.CTkFrame(
            self.node_container, fg_color="blue", corner_radius=0
        )
        self.file_node_container.pack(side="top")

        if self.optional_icon_str:
            self.optional_icon_widget = ctk.CTkLabel(
                self.file_node_container, text=self.optional_icon_str,
                fg_color="transparent", corner_radius=0,
                width=self.icon_size[0], height=self.icon_size[1],
                font=self.icon_font
            )
            self.optional_icon_widget.grid(row=0, column=0, padx=self.optional_icon_padx, pady=self.optional_icon_pady, sticky="w")

        self.text_widget = ctk.CTkLabel(
            self.file_node_container, text=self.name,
            fg_color="transparent", corner_radius=0,
            width=self.icon_size[0], height=self.icon_size[1],
            font=self.text_font
        )
        self.text_widget.grid(row=0, column=1, padx=self.text_padx, pady=self.text_pady, sticky="w")

    def cleanup(self):
        super().cleanup()
