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
