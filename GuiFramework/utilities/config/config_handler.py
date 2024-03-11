# GuiFramework/utilities/config_handler.py

from typing import Dict
from ._config_handler_core import _ConfigHandlerCore, ConfigFileHandlerConfig, CustomTypeHandlerBase


class ConfigHandler:

    @staticmethod
    def add_config(config_name: str, handler_config: ConfigFileHandlerConfig, custom_type_handlers: Dict[str, CustomTypeHandlerBase] = None):
        _ConfigHandlerCore._add_config(config_name, handler_config, custom_type_handlers)

    @staticmethod
    def add_custom_type_handler(type_: str, handler):
        _ConfigHandlerCore._add_custom_type_handler(type_, handler)

    @staticmethod
    def add_custom_type_handlers(handlers):
        _ConfigHandlerCore._add_custom_type_handlers(handlers)

    # file configuration methods
    @staticmethod
    def save_setting(config_name, section, option, value):
        _ConfigHandlerCore._save_setting(config_name, section, option, value)

    @staticmethod
    def get_setting(config_name, section, option, fallback_value=None, force_default=False):
        return _ConfigHandlerCore._get_setting(config_name, section, option, fallback_value, force_default)

    @staticmethod
    def reset_setting(config_name, section, option):
        _ConfigHandlerCore._reset_setting(config_name, section, option)

    @staticmethod
    def reset_section(config_name, section):
        _ConfigHandlerCore._reset_section(config_name, section)

    @staticmethod
    def reset_config(config_name):
        _ConfigHandlerCore._reset_config(config_name)

    # dynamic store management methods
    @staticmethod
    def add_variable(config_name, variable_name, value, section=None):
        _ConfigHandlerCore._add_variable(config_name, variable_name, value, section)

    @staticmethod
    def add_variables(config_name, variables):
        _ConfigHandlerCore._add_variables(config_name, variables)

    @staticmethod
    def _set_variable(config_name, variable_name, value, save_override=False):
        _ConfigHandlerCore._set_variable(config_name, variable_name, value, save_override)

    @staticmethod
    def set_variables(config_name, variables):
        _ConfigHandlerCore._set_variables(config_name, variables)

    @staticmethod
    def get_variable(config_name, variable_name):
        return _ConfigHandlerCore._get_variable(config_name, variable_name)

    @staticmethod
    def delete_variable(config_name, variable_name):
        _ConfigHandlerCore._delete_variable(config_name, variable_name)

    @staticmethod
    def delete_variables(config_name, variable_names):
        _ConfigHandlerCore._delete_variables(config_name, variable_names)

    @staticmethod
    def clear_dynamic_store(config_name):
        _ConfigHandlerCore._clear_dynamic_store(config_name)

    @staticmethod
    def get_dynamic_store_keys(config_name):
        return _ConfigHandlerCore._get_dynamic_store_keys(config_name)
