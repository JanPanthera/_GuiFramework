# locale_updater.py

import os
import re
import json
import copy
import threading
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


class LocaleUpdater:
    DEFAULT_LOCALES_DIR = "locales"
    DEFAULT_SOURCE_LANGUAGE = "en"
    DEFAULT_TARGET_LANGUAGES = ["de", "fr", "it", "ru"]
    SORT_LOCALE_FILE_KEYS = True
    LOCALIZE_CALL_PATTERN = re.compile(r'(?:translate|localize|loc)\("([^"]+)"\)')
    GUI_FILE_PATTERN = re.compile(r"(.+)\.gui\.json$")

    def __init__(self, locales_dir=None, source_language=None, target_languages=None, extract_strings=False,
                 localize_call_patterns=None, sort_locale_file_keys=None, logger=None):
        self.extract_strings = extract_strings
        self.sort_locale_file_keys = sort_locale_file_keys or self.SORT_LOCALE_FILE_KEYS
        self.locales_dir = locales_dir or self.DEFAULT_LOCALES_DIR
        self.source_language = source_language or self.DEFAULT_SOURCE_LANGUAGE
        self.source_locale_file = os.path.join(self.locales_dir, f"locale_{self.source_language}.json")
        self.target_languages = target_languages or self.DEFAULT_TARGET_LANGUAGES
        self.localize_call_patterns = localize_call_patterns or [self.LOCALIZE_CALL_PATTERN]
        self.extracted_strings = set()
        self.lock = threading.RLock()

        self.logger = logger

    def update_settings(self, **kwargs):
        with self.lock:
            self.locales_dir = kwargs.get("locales_dir", self.locales_dir)
            self.source_language = kwargs.get("source_language", self.source_language)
            self.source_locale_file = os.path.join(self.locales_dir, f"locale_{self.source_language}.json")
            self.target_languages = kwargs.get("target_languages", self.target_languages)
            self.localize_call_patterns = kwargs.get("localize_call_patterns", self.localize_call_patterns)
            self.sort_locale_file_keys = kwargs.get("sort_locale_file_keys", self.sort_locale_file_keys)
            self.logger = kwargs.get("logger", self.logger)

    def update_locales(self, source_dir):
        if self.extract_strings:
            self.extracted_strings.clear()
            self._extract_locale_strings(source_dir)
        self._merge_extracted_strings_with_source_file()
        self._update_target_locales()

    def _extract_locale_strings(self, source_dir):
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".py"):
                    self._process_python_file(file_path)
                elif self.GUI_FILE_PATTERN.match(file):
                    self._process_gui_file(file_path)

    def _process_python_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as py_file:
                lines = py_file.read()
                for pattern in self.localize_call_patterns:
                    matches = pattern.findall(lines)
                    with self.lock:
                        self.extracted_strings.update(matches)
        except OSError as e:
            if self.logger:
                self.logger.error(f"Error opening file {file_path}: {str(e)}")

    def _process_gui_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as gui_file:
                for line in gui_file:
                    # Trim leading and trailing whitespace from the line
                    line = line.strip()
                    # Check if the line contains the pattern '"text":'
                    if '"text":' in line:
                        # Find the starting position of the value enclosed in double quotes
                        start_quote_index = line.find('"', line.find('"text":') + len('"text":')) + 1
                        # Find the ending position of the value enclosed in double quotes
                        end_quote_index = line.find('"', start_quote_index)
                        # Extract the value between the double quotes, which is the translation key
                        text_value = line[start_quote_index:end_quote_index]

                        # Add the extracted translation key to the set of extracted strings
                        with self.lock:
                            self.extracted_strings.add(text_value)
        except OSError as e:
            if self.logger:
                self.logger.error(f"Error opening file {file_path}: {str(e)}")

    def _merge_extracted_strings_with_source_file(self):
        with self.lock:
            if not self.extracted_strings:
                if self.logger:
                    self.logger.info("No strings to merge with source locale file")
                return

        source_locale_data = self._load_json_locale_file(self.source_locale_file)
        if source_locale_data is None:
            return

        for string in self.extracted_strings:
            string_exists = any(string in section for section in source_locale_data.values())
            if string_exists:
                print(f"String '{string}' already exists in source locale file: {self.source_locale_file}")
                continue

        for string in self.extracted_strings:
            if not any(string in section for section in source_locale_data.values()):
                source_locale_data["default"][string] = string
                if self.logger:
                    self.logger.info(f"Added string '{string}' to section 'default' in source locale file: {self.source_locale_file}")

        for section in source_locale_data:
            for string in list(source_locale_data[section]):
                if string not in self.extracted_strings and section != "unused":
                    source_locale_data["unused"][string] = source_locale_data[section].pop(string)
                    if self.logger:
                        self.logger.info(f"Moved string '{string}' from section '{section}' to section 'unused' in source locale file: {self.source_locale_file}")

        if self.sort_locale_file_keys:
            for section in source_locale_data:
                source_locale_data[section] = OrderedDict(sorted(source_locale_data[section].items(), key=lambda x: x[0].lower()))

        with open(self.source_locale_file, "w", encoding="utf-8") as file:
            json.dump(source_locale_data, file, ensure_ascii=False, indent=3)

    def _update_target_locales(self):
        with self.lock:
            source_locale_data = self._load_json_locale_file(self.source_locale_file)
            if source_locale_data is None:
                if self.logger:
                    self.logger.error(f"Failed to load source locale file: {self.source_locale_file}")
                return

            for language in self.target_languages:
                target_locale_data = self._load_json_locale_file(os.path.join(self.locales_dir, f"locale_{language}.json"))
                if target_locale_data is None:
                    if self.logger:
                        self.logger.error(f"Failed to load target locale file: {language}")
                    continue

                target_keys = {}
                for section in target_locale_data:
                    for key in target_locale_data[section]:
                        target_keys[key] = target_locale_data[section][key]

                new_target_locale_data = copy.deepcopy(source_locale_data)
                for section in new_target_locale_data:
                    for key in target_keys:
                        if key in new_target_locale_data[section]:
                            new_target_locale_data[section][key] = target_locale_data[section].get(key, key)

                with open(os.path.join(self.locales_dir, f"locale_{language}.json"), "w", encoding="utf-8") as file:
                    json.dump(new_target_locale_data, file, ensure_ascii=False, indent=3)

    def _load_json_locale_file(self, file_path):
        with self.lock:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    locale_data = json.load(file, object_pairs_hook=OrderedDict)
            except FileNotFoundError:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump({}, file, ensure_ascii=False, indent=3)
                    if self.logger:
                        self.logger.info(f"Locale file: {file_path} was not found. Created new file with valid JSON format.")
                locale_data = OrderedDict()
            except json.JSONDecodeError:
                if os.path.getsize(file_path) == 0:
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump({}, file, ensure_ascii=False, indent=3)
                        if self.logger:
                            self.logger.info(f"Locale file: {file_path} was empty. Added valid JSON format to file.")
                    locale_data = OrderedDict()
                else:
                    if self.logger:
                        self.logger.error(f"Invalid JSON format in {file_path}. Review the file and try again.")
                    return None

            locale_data.setdefault("default", OrderedDict())
            locale_data.setdefault("unused", OrderedDict())
            locale_data.move_to_end("default", last=False)
            locale_data.move_to_end("unused")

            return locale_data
