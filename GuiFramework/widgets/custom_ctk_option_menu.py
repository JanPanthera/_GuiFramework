# _GuiFramework/widgets/custom_ctk_option_menu.py

from typing import Optional, Union, List

from customtkinter import CTkOptionMenu, StringVar
from .custom_tooltip import CustomTooltip as FWK_CustomTooltip

from GuiFramework.utilities.localization.localizer import Localizer
from GuiFramework.utilities.localization.localization_key import LocalizationKey


class CustomCTKOptionMenu(CTkOptionMenu):
    def __init__(self, placeholder_text: Union[str, LocalizationKey], options: List[Union[str, LocalizationKey]], optionmenu_properties: Optional[dict] = None, tooltip_text: Optional[Union[str, LocalizationKey]] = None, tooltip_properties: Optional[dict] = None, pack_type: str = "grid", pack_properties: Optional[dict] = None):
        self.tooltip = None

        self._placeholder_text: Union[str, LocalizationKey] = placeholder_text
        self._options_list: List[Union[str, LocalizationKey]] = options
        self._tooltip_text: Optional[Union[str, LocalizationKey]] = tooltip_text

        self.selected_option = StringVar(master=optionmenu_properties.get("master"), value=Localizer.get_localized_string(self._placeholder_text))
        super().__init__(variable=self.selected_option, values=[Localizer.get_localized_string(option) for option in self._options_list], **(optionmenu_properties or {}))

        if tooltip_text:
            self.tooltip = FWK_CustomTooltip(self, text=Localizer.get_localized_string(self._tooltip_text), **(tooltip_properties or {}))

        pack_func = self.grid if pack_type == "grid" else self.pack
        pack_func(**(pack_properties or {}))

        Localizer.subscribe(Localizer.EVENT_LANGUAGE_CHANGED, self.update_localization)

    def update_localization(self, *args, **kwargs):
        selected_option_key = Localizer.get_localization_key_for_string(self.selected_option.get())
        self.selected_option.set(Localizer.get_localized_string(selected_option_key))
        translated_options = [Localizer.get_localized_string(option) for option in self._options_list]
        self.configure(values=translated_options)
        self.update()

    def set_selected_text(self, new_selected_text: str, tooltip_text: Optional[str] = None):
        self.selected_option.set(Localizer.get_localized_string(new_selected_text))
        if tooltip_text is not None:
            self.set_tooltip_text(tooltip_text)

    def create_tooltip(self, text: str, properties: Optional[dict] = None):
        if self.tooltip:
            raise ValueError("Tooltip already exists")
        self.tooltip = FWK_CustomTooltip(self, text=Localizer.get_localized_string(text), **(properties or {}))

    def set_tooltip_text(self, text: str):
        if not self.tooltip:
            raise ValueError("No tooltip to set text to")
        self.tooltip.set_text(Localizer.get_localized_string(text))

    def set_tooltip_delay(self, delay: int):
        if not self.tooltip:
            raise ValueError("No tooltip to set delay to")
        self.tooltip.set_delay(delay)
