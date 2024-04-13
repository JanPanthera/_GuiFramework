# GuiFramework/utilities/localization/locales.py

from dataclasses import dataclass
from typing import List

from .locale import Locale


@dataclass
class Locales:

    @classmethod
    def add_locale(cls, locale: Locale):
        """Add a locale to the class if it doesn't already exist."""
        locale_name_upper = locale.locale_name.upper()
        if hasattr(cls, locale_name_upper):
            raise ValueError(f"Locale '{locale.locale_name}' already exists.")
        setattr(cls, locale_name_upper, locale)

    @classmethod
    def add_locales(cls, locales: List[Locale]):
        """Add multiple locales to the class."""
        for locale in locales:
            cls.add_locale(locale)

    @classmethod
    def get_locale(cls, string: str) -> Locale:
        """Return a locale by its locale code."""
        for locale in cls.get_locales():
            if locale.locale == string or locale.locale_name == string or string in locale.local_aliases:
                return locale

    @classmethod
    def get_locales(cls) -> List[Locale]:
        """Return a list of all locales added to the class."""
        return [getattr(cls, locale_name) for locale_name in dir(cls) if not locale_name.startswith("_")]
