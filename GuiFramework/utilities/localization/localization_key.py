# GuiFramework/utilities/localization/localization_key.py

import uuid
from .localizer import Localizer


class LocalizationKey:
    """Represent a localization key for retrieving localized strings."""

    def __init__(self, key=None):
        """Initialize with the specified localization key."""
        self.key = key or str(uuid.uuid4())

    def get_localized_string(self, *args):
        """Return the localized string associated with this key, formatted with optional arguments."""
        return Localizer.get_localized_string(self.key, *args)

    def get_localized_string_for_locale(self, locale, *args):
        """Return the localized string associated with this key in the specified locale, formatted with optional arguments."""
        return Localizer.get_localized_string_for_locale(locale, self.key, *args)
