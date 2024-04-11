from dataclasses import dataclass
from typing import List, Optional

from .locales import Locales, Locale


@dataclass
class LocalizerSetup:
    """Define setup configuration for Localizer."""
    active_locale: Locale
    fall_back_locale: Locale


@dataclass
class _LocalizationSettings:
    """Store active and fallback locales for localization."""
    _active_locale: Locale
    _fall_back_locale: Locale

    @property
    def _available_locales(self) -> List[Locale]:
        """Return a list of available locales."""
        return Locales.get_locales()


class Localizer:
    """Provide localization services for the application."""
    settings: Optional[_LocalizationSettings] = None

    @classmethod
    def initialize(cls, setup: LocalizerSetup) -> None:
        """Initialize the Localizer with given setup."""
        if cls.settings is not None:
            raise RuntimeError("Localizer has already been initialized")
        cls.settings = _LocalizationSettings(
            _active_locale=setup.active_locale,
            _fall_back_locale=setup.fall_back_locale
        )

    @classmethod
    def set_active_locale(cls, locale: Locale) -> None:
        """Set the active locale for localization."""
        if cls.settings is None:
            raise RuntimeError("Localizer has not been initialized")
        cls.settings._active_locale = locale

    @classmethod
    def set_fall_back_locale(cls, locale: Locale) -> None:
        """Set the fallback locale for localization."""
        if cls.settings is None:
            raise RuntimeError("Localizer has not been initialized")
        cls.settings._fall_back_locale = locale

    @classmethod
    def get_localized_string(cls, key: str, *args) -> str:
        """Return a localized string for a given key, using active or fallback locale."""
        if cls.settings is None:
            raise RuntimeError("Localizer has not been initialized")
        localized_string = cls.settings._active_locale.get_localized_string(key, *args)
        if localized_string.startswith("Missing key"):
            localized_string = cls.settings._fall_back_locale.get_localized_string(key, *args)
        return localized_string

    @classmethod
    def get_localization_key_for_string(cls, key: str) -> str:
        """Return the localization key for a given string, using active or fallback locale."""
        if cls.settings is None:
            raise RuntimeError("Localizer has not been initialized")
        key_string = cls.settings._active_locale.get_localization_key_for_string(key)
        if key_string.startswith("Missing key"):
            key_string = cls.settings._fall_back_locale.get_localization_key_for_string(key)
        return key_string
