# GuiFramework/utilities/localization/locale_file.py

from dataclasses import dataclass
from typing import Optional, Dict

from .locale_dictionary import LocaleDictionary


@dataclass
class LocaleFile:
    file_path: str
    file_encoding: str = "utf8"
    _file_data: Optional[LocaleDictionary] = None

    def _populate_data(self):
        """Populate the locale data if not already populated."""
        if self._file_data is None:
            self._file_data = LocaleDictionary(self.file_path, self.file_encoding)

    def get_dictionary(self) -> Dict[str, str]:
        """Return the locale dictionary."""
        if self._file_data is None:
            self._populate_data()
        return self._file_data.dictionary

    def get_reverse_dictionary(self) -> Dict[str, str]:
        """Return the reverse locale dictionary."""
        if self._file_data is None:
            self._populate_data()
        return self._file_data.reverse_dictionary
