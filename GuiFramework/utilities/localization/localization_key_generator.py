# GuiFramework/utilities/localization/localization_key_generator.py

import json
import black

from pathlib import Path
from typing import Any, Dict


class LocalizationKeyGenerator:
    MAX_LINE_LENGTH = 3000

    @classmethod
    def generate_keys(cls, json_filepath: str, output_path: str = None, root_class_name: str = 'LocKeys', file_name: str = 'loc_keys.py') -> None:
        """Generate localization keys from a JSON file and write them to a Python file."""
        json_data = cls._load_json_data(json_filepath)

        python_code = cls._generate_class_def(root_class_name, json_data)
        full_code = f"# This file is generated by the LocalizationKeyGenerator class. Do not modify it manually.\n\nfrom GuiFramework.utilities.localization.localization_key import LocalizationKey\n\n{python_code}"

        output_path = cls._determine_output_path(output_path, file_name)
        cls._write_to_file(output_path, full_code)

        cls._format_with_black(output_path)

    @classmethod
    def _load_json_data(cls, json_filepath: str) -> Dict[str, Any]:
        """Load and return JSON data from a file."""
        json_path = Path(json_filepath)
        try:
            with json_path.open() as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to load JSON file at {json_filepath}: {e}")

    @classmethod
    def _determine_output_path(cls, output_path: str, file_name: str) -> Path:
        """Determine and return the output path for the generated Python file."""
        if output_path is None:
            return Path(__file__).parent / file_name
        output_path = Path(output_path)
        return output_path / file_name if output_path.is_dir() else output_path

    @classmethod
    def _write_to_file(cls, output_path: Path, content: str) -> None:
        """Write the given content to a file at the specified path."""
        output_path.write_text(content)

    @classmethod
    def _generate_class_def(cls, class_name: str, attributes: Dict[str, Any], path: str = "") -> str:
        """Generate and return the definition of a Python class for localization keys."""
        class_lines = [f"\nclass {class_name}:"]

        for name, value in attributes.items():
            attr_path = f"{path}.{name}" if path else name
            if isinstance(value, dict):
                nested_class = cls._generate_class_def(name, value, attr_path)
                class_lines.append('    ' + nested_class.replace('\n', '\n    '))
            else:
                class_lines.append(f"    {name.upper()} = LocalizationKey(\"{attr_path}\")")

        return "\n".join(class_lines)

    @classmethod
    def _format_with_black(cls, file_path: str) -> None:
        """Format the Python file at the specified path using the Black code formatter."""
        path = Path(file_path)
        if not path.is_file():
            raise Exception(f"The path {file_path} is not a valid file.")

        mode = black.Mode(line_length=cls.MAX_LINE_LENGTH)
        try:
            black.format_file_in_place(path, fast=True, mode=mode, write_back=black.WriteBack.YES)
        except black.NothingChanged:
            pass
        except Exception as e:
            raise Exception(f"An error occurred while formatting: {e}")
