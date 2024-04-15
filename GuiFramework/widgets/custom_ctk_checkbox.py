# _GuiFramework/widgets/custom_ctk_checkbox.py

from typing import Optional, Union

from customtkinter import CTkCheckBox
from .custom_tooltip import CustomTooltip as FWK_CustomTooltip

from GuiFramework.utilities.localization.localizer import Localizer
from GuiFramework.utilities.localization.localization_key import LocalizationKey


class CustomCTKCheckbox(CTkCheckBox):
    def __init__(self, checkbox_text: Union[str, LocalizationKey], checkbox_properties: dict, tooltip_text: Optional[Union[str, LocalizationKey]] = None, tooltip_properties: Optional[dict] = None, pack_type: str = "grid", pack_properties: Optional[dict] = None):
        if not checkbox_properties.get("master"):
            raise ValueError("master must be provided in checkbox_properties")
        self.tooltip = None

        self._checkbox_text: Union[str, LocalizationKey] = checkbox_text
        self._tooltip_text: Optional[Union[str, LocalizationKey]] = tooltip_text

        super().__init__(text=Localizer.get_localized_string(self._checkbox_text), **checkbox_properties)

        if tooltip_text:
            self.tooltip = FWK_CustomTooltip(self, text=Localizer.get_localized_string(self._tooltip_text), **(tooltip_properties or {}))

        pack_func = self.grid if pack_type == "grid" else self.pack
        pack_func(**(pack_properties or {}))

        Localizer.subscribe(Localizer.EVENT_LANGUAGE_CHANGED, self.update_localization)

    def update_localization(self, *args, **kwargs):
        self.configure(text=Localizer.get_localized_string(self._checkbox_text))
        if self.tooltip:
            self.tooltip.set_text(Localizer.get_localized_string(self._tooltip_text))

    def set_text(self, checkbox_text: str, tooltip_text: Optional[str] = None):
        self.configure(text=checkbox_text)
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
