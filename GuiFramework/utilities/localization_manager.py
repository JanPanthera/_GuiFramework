# localization_manager.py

from concurrent.futures import ThreadPoolExecutor
import json
import glob
import threading
from babel import Locale
from pathlib import Path
from collections import defaultdict
from .utils import setup_default_logger
from .bimap import BiMap


class LocalizationManager:
    DEFAULT_LOCALES_DIR = "locales"
    DEFAULT_FALLBACK_LANGUAGE = "en"
    DEFAULT_LANGUAGE = "en"

    def __init__(self, locales_dir=None, active_language=None, fallback_language=None, lazy_load=True, logger=None):
        self.logger = logger or setup_default_logger("LocalizationManager")
        self.lock = threading.RLock()
        self.observers = []
        self.locale_dir = Path(locales_dir) or Path(self.DEFAULT_LOCALES_DIR)
        if not self.locale_dir.exists() or not self.locale_dir.is_dir():
            self.locale_dir.mkdir(parents=True, exist_ok=True)
            self.logger.warning(f"Locales directory not found, creating: {self.locale_dir}")
        self.language_map = self._map_languages()
        self.lazy_load = lazy_load

        self.fallback_language = fallback_language or self.DEFAULT_FALLBACK_LANGUAGE
        self.active_language = active_language or self.DEFAULT_LANGUAGE
        self.dictionaries = defaultdict(BiMap)

        if not self.lazy_load:
            self._load_all_languages()
        else:
            self._load_language_dict_from_file(self.active_language)
            if self.fallback_language != self.active_language:
                self._load_language_dict_from_file(self.fallback_language)

    def set_active_language(self, language_code):
        """Sets a new active language."""
        self._set_language(language_code, "active")

    def set_fallback_language(self, language_code):
        """Sets a new fallback language."""
        self._set_language(language_code, "fallback")

    def _set_language(self, language_code, language_type):
        """Sets a new language, with validation and fallback."""
        with self.lock:
            try:
                if language_code.lower() in self.language_map:
                    normalized_language_code = self.language_map[language_code.lower()]
                elif language_code.lower() in self.language_map.values():
                    normalized_language_code = language_code.lower()
                else:
                    raise KeyError(f"Language '{language_code}' is not available.")

                if normalized_language_code not in self.dictionaries:
                    self._load_language_dict_from_file(normalized_language_code)

                if language_type == "active":
                    self.active_language = normalized_language_code
                elif language_type == "fallback":
                    self.fallback_language = normalized_language_code

                self.logger.info(f"{language_type.capitalize()} language set to: {normalized_language_code}")
                self._notify_observers(normalized_language_code, language_type)

            except KeyError as e:
                self.logger.warning(f"{e} Falling back to default {language_type} language.")
                if language_type == "active":
                    self.active_language = self.DEFAULT_LANGUAGE
                elif language_type == "fallback":
                    self.fallback_language = self.DEFAULT_FALLBACK_LANGUAGE

            except (FileNotFoundError, IOError) as e:
                self.logger.error(f"Error loading {language_type} language dictionary for '{language_code}': {e}")
                if language_type == "active":
                    self.active_language = self.DEFAULT_LANGUAGE
                elif language_type == "fallback":
                    self.fallback_language = self.DEFAULT_FALLBACK_LANGUAGE

    def get_language(self):
        """Returns the active language."""
        return self.active_language

    def available_languages(self):
        """Returns a list of available languages."""
        return [Locale.parse(lang).display_name for lang in self.dictionaries]

    def localize(self, key, target_language=None):
        """Localizes a key to the active language or a specified target language."""
        def _load_and_localize(language_code, key):
            if language_code not in self.dictionaries:
                self._load_language_dict_from_file(language_code)
            return self.dictionaries[language_code].get(key, key)
        if not key:
            self.logger.warning("Localization key is empty")
            return "key_error"
        with self.lock:
            if not target_language or target_language.lower() == self.active_language.lower():
                return self.dictionaries[self.active_language].get(key, key)
            target_language = self.language_map.get(target_language.lower(), None)
            if target_language:
                result = _load_and_localize(target_language, key)
                if result != key:
                    return result
            return self.dictionaries[self.active_language].get(key, key)

    def reverse_localize(self, translation):
        """Attempts to reverse localize a translation to the original key."""
        def _load_and_reverse_localize(language_code, translation):
            if language_code not in self.dictionaries:
                self._load_language_dict_from_file(language_code)
            reverse_dict = self.dictionaries[language_code].inverse()
            return reverse_dict.get(translation, translation)
        with self.lock:
            if translation in self.dictionaries[self.active_language].inverse():
                return self.dictionaries[self.active_language].inverse().get(translation, translation)
            results = [_load_and_reverse_localize(lang, translation) for lang in self.language_map.values()]
            for result in results:
                if result != translation:
                    return result
            return translation

    def localize_with_params(self, key, **params):
        """Localizes a key to the active language with parameters."""
        translation = self.localize(key)
        for placeholder, value in params.items():
            translation = translation.replace(f"{{placeholder}}", str(value))
        return translation

    def subscribe(self, observer):
        """Subscribes an observer to language updates."""
        with self.lock:
            if not callable(getattr(observer, "on_language_updated", None)):
                observer_name = observer.__class__.__name__
                raise ValueError(f"Observer must implement 'on_language_updated' method: {observer_name}")
            self.observers.append(observer)

    def unsubscribe(self, observer):
        """Unsubscribes an observer from language updates."""
        with self.lock:
            self.observers.remove(observer)
            self.logger.info(f"Unsubscribed observer: {observer}")

    def _notify_observers(self, language_code, change_type):
        """Notifies all observers that the language has been updated."""
        for observer in self.observers:
            observer.on_language_updated(language_code, change_type)

    def _process_file(self, file_path):
        try:
            code = Path(file_path).stem.split("_")[1]
            if not Locale.parse(code):
                raise ValueError(f"Invalid locale code in file name: {file_path}")
            return code.lower(), code
        except (IndexError, ValueError) as e:
            self.logger.warning(f"Skipping invalid dictionary file '{file_path}': {e}")
            return None

    def _map_languages(self):
        """Generates a map of available languages based on dictionary files."""
        mapping = {}
        for file_path in glob.glob(str(self.locale_dir / "locale_*.json")):
            result = self._process_file(file_path)
            if result is not None:
                locale_code = result[1]
                locale_obj = Locale.parse(locale_code)
                english_name = locale_obj.get_display_name('en').lower()
                mapping[english_name] = locale_code
        if not mapping:
            self.logger.error("No valid language dictionaries found. Please check the locales directory.")
        return mapping

    def _load_all_languages(self):
        """Loads all available languages into memory."""
        with ThreadPoolExecutor() as executor:
            executor.map(self._load_language_dict_from_file, self.language_map.values())

    def _load_language_dict_from_file(self, language_code):
        """Loads a language dictionary from file into memory."""
        file_path = self.locale_dir / f"locale_{language_code}.json"
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    for _, translations in data.items():
                        for k, v in translations.items():
                            self.dictionaries[language_code][k] = v
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                self.logger.error(f"Failed to load language dictionary '{language_code}': {e}")