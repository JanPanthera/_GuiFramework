# localization_manager.py

import json
import glob
import threading
from babel import Locale
from pathlib import Path
from collections import defaultdict


class LocalizationManager:
    DEFAULT_LOCALES_DIR = "locales"
    DEFAULT_LANGUAGE = "en"

    def __init__(self, locales_dir=None, default_language=None, logger=None):
        self.locale_dir = Path(locales_dir) or Path(self.DEFAULT_LOCALES_DIR)
        self.language = default_language or self.DEFAULT_LANGUAGE
        self.logger = logger
        self.language_map = self._map_languages()
        self.dictionaries = defaultdict(dict)
        self.reverse_dictionaries = defaultdict(dict)
        self.active_dict = {}
        self.active_reverse_dict = {}
        self.observers = []
        self.lock = threading.RLock()

        for language_code in self.language_map.values():
            self._load_language(language_code)

    def set_language(self, language_code):
        with self.lock:
            language_code = self.language_map.get(language_code.lower(), language_code)
            self.language = language_code
            self._load_language(language_code)
            self._log_info(f"Language set to {language_code}")

    def get_language(self):
        return self.language

    def get_key(self, translation):
        for language_code, reverse_dict in self.reverse_dictionaries.items():
            if translation in reverse_dict:
                return reverse_dict[translation]
        return translation

    def available_languages(self):
        return [Locale.parse(lang).display_name for lang in self.dictionaries]

    def translate(self, key):
        if not key:
            return key
        return self.active_dict.get(key, self.active_dict.get(key.lower(), key))

    def translate_in_language(self, key, language_code):
        language_code = self.language_map.get(language_code.lower(), language_code)
        return self.reverse_dictionaries[language_code].get(key, key)

    def reverse_translate(self, translation):
        return self.active_reverse_dict.get(translation, translation)

    def subscribe(self, observer):
        with self.lock:
            if not callable(getattr(observer, "update_language", None)):
                raise ValueError("Observer must implement update_language method")
            self.observers.append(observer)
            self._log_info(f"Subscribed observer: {observer}")

    def unsubscribe(self, observer):
        with self.lock:
            self.observers.remove(observer)
            self._log_info(f"Unsubscribed observer: {observer}")

    def _load_language(self, language_code):
        with self.lock:
            if language_code not in self.dictionaries:
                self._load_dictionaries_from_file(language_code)
            self.active_dict = self.dictionaries[language_code]
            self.active_reverse_dict = self.reverse_dictionaries[language_code]
            self._notify_observers()

    def _map_languages(self):
        mapping = {}
        for file_path in glob.glob(str(self.locale_dir / "locale_*.json")):
            code = Path(file_path).stem.split("_")[1]
            locale = Locale.parse(code)
            mapping[locale.get_display_name("en").lower()] = code
        return mapping

    def _load_dictionaries_from_file(self, language_code):
        file_path = self.locale_dir / f"locale_{language_code}.json"
        if file_path.is_file():
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                flat_dict = {k: v for _, translations in data.items() for k, v in translations.items()}
                self.dictionaries[language_code] = flat_dict
                self.reverse_dictionaries[language_code] = {v: k for k, v in flat_dict.items()}

    def _notify_observers(self):
        for observer in self.observers:
            observer.update_language()

    def _log_info(self, message):
        if self.logger:
            self.logger.info(message)
