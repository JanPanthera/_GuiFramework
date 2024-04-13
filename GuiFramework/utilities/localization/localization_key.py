# GuiFramework/utilities/localization/localization_key.py

from .localizer import Localizer


class LocalizationKey:
    """Represent a localization key for retrieving localized strings."""

    def __init__(self, key):
        """Initialize with the specified localization key."""
        self.key = key

    def get_localized_string(self, *args):
        """Return the localized string associated with this key, formatted with optional arguments."""
        return Localizer.get_localized_string(self.key, *args)

    def get_localized_string_for_locale(self, locale, *args):
        """Return the localized string associated with this key in the specified locale, formatted with optional arguments."""
        return Localizer.get_localized_string_for_locale(locale, self.key, *args)

    def get_localization_key_for_string(self, string):
        """Return the localization key for a given string."""
        return Localizer.get_localization_key_for_string(string)
