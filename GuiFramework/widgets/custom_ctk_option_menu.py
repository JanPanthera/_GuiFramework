# _GuiFramework/widgets/custom_ctk_option_menu.py

from typing import Optional, Callable

from customtkinter import CTkOptionMenu, StringVar
from .custom_tooltip import CustomTooltip as FWK_CustomTooltip


class CustomCTKOptionMenu(CTkOptionMenu):
    def __init__(self, placeholder_text: str, options: list[str], optionmenu_properties: Optional[dict] = None, tooltip_text: Optional[str] = None, tooltip_properties: Optional[dict] = None, pack_type: str = "grid", pack_properties: Optional[dict] = None, loc_func: Optional[Callable] = lambda x: x):
        self.tooltip = None
        self.loc_func = loc_func

        self._placeholder_text = placeholder_text  # The original text of the placeholder
        self._options_list = options  # The original text of the options
        self._tooltip_text = tooltip_text  # The original text of the tooltip

        translated_options = [self.loc_func(option) for option in self._options_list]
        self.selected_option = StringVar(master=optionmenu_properties.get("master"), value=self.loc_func(self._placeholder_text))
        super().__init__(variable=self.selected_option, values=translated_options, **(optionmenu_properties or {}))

        if tooltip_text:
            self.tooltip = FWK_CustomTooltip(self, text=self.loc_func(self._tooltip_text), **(tooltip_properties or {}))

        pack_func = self.grid if pack_type == "grid" else self.pack
        pack_func(**(pack_properties or {}))

    def update_localization(self):
        if self.loc_func:
            self.selected_option.set(self.loc_func(self.selected_option.get()))
            translated_options = [self.loc_func(option) for option in self._options_list]
            self.configure(values=translated_options)
            self.update()

    def set_selected_text(self, new_selected_text: str, tooltip_text: Optional[str] = None):
        self.selected_option.set(self.loc_func(new_selected_text))
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
