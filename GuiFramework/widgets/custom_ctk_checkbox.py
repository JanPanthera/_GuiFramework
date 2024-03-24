# _GuiFramework/widgets/custom_ctk_checkbox.py

from typing import Optional, Callable

from customtkinter import CTkCheckBox
from .custom_tooltip import CustomTooltip as FWK_CustomTooltip


class CustomCTKCheckbox(CTkCheckBox):
    def __init__(self, checkbox_text: str, checkbox_properties: dict, tooltip_text: Optional[str] = None, tooltip_properties: Optional[dict] = None, pack_type: str = "grid", pack_properties: Optional[dict] = None, loc_func: Optional[Callable] = lambda x: x):
        self.tooltip = None
        self.loc_func = loc_func

        self._checkbox_text = checkbox_text  # The original text of the checkbox
        self._tooltip_text = tooltip_text  # The original text of the tooltip

        super().__init__(text=self.loc_func(self._checkbox_text), **(checkbox_properties or {}))

        if tooltip_text:
            self.tooltip = FWK_CustomTooltip(self, text=self.loc_func(self._tooltip_text), **(tooltip_properties or {}))

        pack_func = self.grid if pack_type == "grid" else self.pack
        pack_func(**(pack_properties or {}))

    def update_localization(self):
        if self.loc_func:
            self.configure(text=self.loc_func(self._checkbox_text))
            if self.tooltip:
                self.tooltip.set_text(self.loc_func(self._tooltip_text))

    def set_text(self, checkbox_text: str, tooltip_text: Optional[str] = None):
        self.configure(text=checkbox_text)
        if tooltip_text is not None:
            self.set_tooltip_text(tooltip_text)

    def create_tooltip(self, text: str, properties: Optional[dict] = None):
        if self.tooltip:
            raise ValueError("Tooltip already exists")
        self.tooltip = FWK_CustomTooltip(self, text=self.loc_func(text), **(properties or {}))

    def set_tooltip_text(self, text: str):
        if not self.tooltip:
            raise ValueError("No tooltip to set text to")
        self.tooltip.set_text(self.loc_func(text))

    def set_tooltip_delay(self, delay: int):
        if not self.tooltip:
            raise ValueError("No tooltip to set delay to")
        self.tooltip.set_delay(delay)
