# GuiFramework/utilities/localization/localizer.py

from dataclasses import dataclass
from typing import List, Optional

from .locales import Locales, Locale
from GuiFramework.mixins.event_mixin import StaticEventMixin, create_event_type_id


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


class Localizer(StaticEventMixin):
    """Provide localization services for the application."""
    settings: Optional[_LocalizationSettings] = None
    EVENT_LANGUAGE_CHANGED = create_event_type_id()

    @classmethod
    def _check_initialized(cls):
        if cls.settings is None:
            raise RuntimeError("Localizer has not been initialized")

    @classmethod
    def initialize(cls, setup: LocalizerSetup) -> None:
        """Initialize the Localizer with given setup."""
        cls.settings = _LocalizationSettings(
            _active_locale=setup.active_locale,
            _fall_back_locale=setup.fall_back_locale
        )

    @classmethod
    def set_active_locale(cls, locale_identifier: str | Locale) -> None:
        """Set the active locale for localization."""
        cls._check_initialized()
        if isinstance(locale_identifier, Locale):
            new_locale = locale_identifier
        elif isinstance(locale_identifier, str):
            new_locale = next((locale for locale in Locales.get_locales() if locale_identifier in {locale.locale, locale.locale_name, *locale.local_aliases}), None)
        if new_locale is None:
            raise ValueError("Supplied locale is not a valid Locale Object or a registered locale name, locale code, or alias.")
        cls.settings._active_locale = new_locale
        cls.notify(cls.EVENT_LANGUAGE_CHANGED, new_locale)

    @classmethod
    def set_fall_back_locale(cls, locale: Locale) -> None:
        """Set the fallback locale for localization."""
        cls._check_initialized()
        cls.settings._fall_back_locale = locale

    @classmethod
    def get_active_locale(cls) -> Locale:
        """Return the active locale for localization."""
        cls._check_initialized()
        return cls.settings._active_locale

    @classmethod
    def get_localized_string(cls, key: str, *args) -> str:
        """Return a localized string for a given key, using active or fallback locale."""
        cls._check_initialized()
        localized_string = cls.settings._active_locale.get_localized_string(key, *args)
        if localized_string == key and cls.settings._active_locale != cls.settings._fall_back_locale:
            localized_string = cls.settings._fall_back_locale.get_localized_string(key, *args)
        return localized_string

    @classmethod
    def get_localized_string_for_locale(cls, locale: Locale, key: str, *args) -> str:
        """Return a localized string for a given key in a specific locale."""
        cls._check_initialized()
        localized_string = locale.get_localized_string(key, *args)
        if localized_string == key and locale != cls.settings._fall_back_locale:
            localized_string = cls.settings._fall_back_locale.get_localized_string(key, *args)
        return localized_string

    @classmethod
    def get_localization_key_for_string(cls, key: str) -> str:
        """Return the localization key for a given string, using active or fallback locale."""
        cls._check_initialized()
        key_string = cls.settings._active_locale.get_localization_key_for_string(key)
        if key_string == key and cls.settings._active_locale != cls.settings._fall_back_locale:
            key_string = cls.settings._fall_back_locale.get_localization_key_for_string(key)
        return key_string
