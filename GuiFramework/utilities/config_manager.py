# GuiFramework/utilities/config_manager.py

import os
import configparser
from pathlib import Path

from GuiFramework.utilities.utils import setup_default_logger


class ConfigManager():
    DEFAULT_CONFIG_PATH = "config"
    DEFAULT_CONFIG_NAME = "default-config.ini"
    CUSTOM_CONFIG_NAME = "custom-config.ini"

    def __init__(self, default_config_creator_func, config_path=None, default_config_name=None, custom_config_name=None, logger=None):
        config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.default_config_path = Path(config_path) / (default_config_name or self.DEFAULT_CONFIG_NAME)
        self.custom_config_path = Path(config_path) / (custom_config_name or self.CUSTOM_CONFIG_NAME)
        self.default_config = configparser.ConfigParser()
        self.custom_config = configparser.ConfigParser()
        self.default_config.optionxform = str
        self.custom_config.optionxform = str
        self.dynamic_store = {}
        self.type_creators = {}
        self.type_savers = {}
        self.default_values = default_config_creator_func()
        self.logger = logger or setup_default_logger(log_name="ConfigManager", log_directory="logs/GuiFramework")
        self._check_default_config()
        self.load_config()

    # Public methods
    def register_variable_type(self, type_name, creator, saver):
        self.type_creators[type_name] = creator
        self.type_savers[type_name] = saver

    def load_config(self):
        try:
            if not self.custom_config_path.exists() and self.default_config_path.exists():
                self.custom_config_path.write_text(self.default_config_path.read_text(encoding="utf-8"), encoding="utf-8")

            self.default_config.read(self.default_config_path, encoding="utf-8")
            self.custom_config.read([self.default_config_path, self.custom_config_path], encoding="utf-8")
        except (FileNotFoundError, configparser.Error) as e:
            if self.logger:
                self.logger.error(f"Failed to load configuration: {e}")
            raise RuntimeError(f"Failed to load configuration: {e}")

    def save_setting(self, section, option, value):
        self._save_to_config(self.custom_config, section, option, value)

    def save_settings(self, section, settings):
        for option, value in settings.items():
            self._save_to_config(self.custom_config, section, option, value)

    def load_setting(self, section, option, default_value=None, force_default=False):
        try:
            if force_default:
                return self.default_config.get(section, option)
            else:
                return self.custom_config.get(section, option, fallback=default_value)
        except configparser.NoSectionError:
            if self.logger:
                self.logger.error(f"Section \"{section}\" not found in configuration. Using default value.")
            raise ValueError(f"Section \"{section}\" not found in configuration.")
        except configparser.Error as e:
            if self.logger:
                self.logger.error(f"Failed to load setting \"{option}\" in section \"{section}\": {e}")
            if default_value is None:
                raise ValueError(f"No default value provided for \"{option}\" in section \"{section}\"")
            return default_value

    def reset_setting(self, section, option):
        self._reset_to_default(section, option)

    def reset_settings(self, section_option_pairs):
        for section, option in section_option_pairs:
            self._reset_to_default(section, option)

    def reset_all_settings(self):
        self.custom_config.clear()
        self.custom_config.read(self.default_config_path, encoding="utf-8")
        self._write_config_to_file(self.custom_config, self.custom_config_path)

    def add_variable(self, name, value=None, section=None):
        if name in self.dynamic_store:
            if self.logger:
                self.logger.warning(f"Variable \"{name}\" already exists in dynamic store.")
            raise ValueError(f"Variable \"{name}\" already exists in dynamic store.")
        if section:
            _value = self.load_setting(section, name)
            if _value is not None:
                creator = self.type_creators.get(type(value))
                if creator:
                    value = creator(_value)
                else:
                    value = _value
            self.save_setting(section, name, value)
        self.dynamic_store[name] = {"value": value, "section": section}

    def set_variable(self, name, value, save=True):
        if name in self.dynamic_store:
            section = self.dynamic_store[name].get("section")
            if section and save:
                self.save_setting(section, name, value)
            self.dynamic_store[name]["value"] = value
        else:
            if self.logger:
                self.logger.warning(f"Variable \"{name}\" not found in dynamic store.")
            raise ValueError(f"Variable \"{name}\" not found in dynamic store.")

    def get_variable(self, name):
        return self.dynamic_store.get(name, {}).get("value")

    def remove_variable(self, name):
        if name in self.dynamic_store:
            del self.dynamic_store[name]
        else:
            if self.logger:
                self.logger.warning(f"Variable \"{name}\" not found in dynamic store.")
            raise ValueError(f"Variable \"{name}\" not found in dynamic store.")

    def is_variable_in_dynamic_store(self, name):
        return name in self.dynamic_store

    def clear_dynamic_store(self):
        self.dynamic_store.clear()

    def get_dynamic_store_keys(self):
        return list(self.dynamic_store.keys())

    # Private methods
    def _check_default_config(self):
        self._generate_default_config()

    def _generate_default_config(self):
        for section, options in self.default_values.items():
            if not self.default_config.has_section(section):
                self.default_config.add_section(section)
            for option, value in options.items():
                self.default_config.set(section, option, value)
        os.makedirs(os.path.dirname(self.default_config_path), exist_ok=True)
        self._write_config_to_file(self.default_config, self.default_config_path)

    def _write_config_to_file(self, config, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as configfile:
                config.write(configfile)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to write to configuration file: {e}")
            raise RuntimeError(f"Failed to write to configuration file: {e}")

    def _save_to_config(self, config, section, option, value):
        try:
            if not config.has_section(section):
                config.add_section(section)
            saver = self.type_savers.get(type(value))
            if saver:
                value = saver(value)
            config.set(section, option, str(value))
            self._write_config_to_file(config, self.custom_config_path)
        except configparser.Error as e:
            if self.logger:
                self.logger.error(f"Failed to save \"{option}\" in section \"{section}\": {e}")
            raise ValueError(f"Failed to save \"{option}\" in section \"{section}\": {e}")

    def _reset_to_default(self, section, option):
        try:
            default_value = self.default_config.get(section, option)
            self.custom_config.set(section, option, default_value)
            self._write_config_to_file(self.custom_config, self.custom_config_path)
            if option in self.dynamic_store:
                creator = self.type_creators.get(type(self.dynamic_store[option]["value"]))
                if creator:
                    default_value = creator(default_value)
                self.dynamic_store[option]["value"] = default_value
        except configparser.NoSectionError:
            if self.logger:
                self.logger.error(f"Section \"{section}\" not found in default configuration.")
            raise ValueError(f"Section \"{section}\" not found in default configuration.")
        except configparser.NoOptionError:
            if self.logger:
                self.logger.error(f"Option \"{option}\" not found in section \"{section}\" of default configuration.")
            raise ValueError(f"Option \"{option}\" not found in section \"{section}\" of default configuration.")
        except configparser.Error as e:
            if self.logger:
                self.logger.error(f"Failed to reset setting \"{option}\" in section \"{section}\": {e}")
            raise ValueError(f"Failed to reset setting \"{option}\" in section \"{section}\": {e}")