# GuiFramework/utilities/localization/locale.py

from dataclasses import dataclass

from .locale_file import LocaleFile


@dataclass
class Locale:
    locale: str
    locale_name: str
    file: LocaleFile

    def __post_init__(self):
        """Populate locale data from file."""
        self.file._populate_data()

    def __str__(self):
        """Return the locale name."""
        return self.locale_name

    def get_localized_string(self, key: str, *args) -> str:
        """Return a localized string for a given key, formatted with optional arguments."""
        localized_string = self.file.get_dictionary().get(key, f"Missing key: {key}")
        return localized_string.format(*args) if args else localized_string

    def get_localization_key_for_string(self, key: str) -> str:
        """Return the localization key for a given string."""
        return self.file.get_reverse_dictionary().get(key, f"Missing key: {key}")
