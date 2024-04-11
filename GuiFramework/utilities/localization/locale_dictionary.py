# GuiFramework/utilities/localization/locale_dictionary.py

import json
import collections

from typing import Dict


class LocaleDictionary:

    def __init__(self, file_path: str, encoding: str = "utf8"):
        """Initialize the locale dictionary with a file path and encoding."""
        self.dictionary: Dict[str, str] = {}
        self.reverse_dictionary: Dict[str, str] = {}
        self._load_dictionary(file_path, encoding)

    def _load_dictionary(self, file_path: str, encoding: str):
        """Load and flatten the dictionary from the specified file."""
        try:
            with open(file_path, "r", encoding=encoding) as file:
                data = json.load(file)
                self._flatten_dictionary(data)
        except Exception as e:
            raise ValueError(f"Error loading dictionary from {file_path}") from e

    def _flatten_dictionary(self, dictionary: dict, parent_key=''):
        """Flatten a nested dictionary, populating `dictionary` and `reverse_dictionary`."""
        items = collections.deque([(parent_key, dictionary)])
        while items:
            parent_key, curr_dict = items.pop()
            for key, value in curr_dict.items():
                new_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, dict):
                    items.appendleft((new_key, value))
                else:
                    self.dictionary[new_key] = value
                    self.reverse_dictionary[value] = new_key
