import customtkinter as ctk

from GuiFramework.utilities.file_ops import FileOps
from GuiFramework.utilities.logging import Logger, LoggerConfig, LOG_LEVEL
from GuiFramework.utilities.config import ConfigFileHandlerConfig
from GuiFramework.custom_type_handlers import ListTypeHandler, TupleTypeHandler, CtkStringVarTypeHandler, CtkBooleanVarTypeHandler

from GuiFramework.utilities.config import ConfigHandler
from GuiFramework.utilities.config.config_types import ConfigKeyList


LOGGER_NAME = "GuiFramework"
LOG_NAME = "gui_framework"
APP_NAME = "GuiFramework"
CONFIG_NAME = "Default"

UI_THEMES = ["light", "dark", "system"]
UI_COLOR_THEMES = ["blue", "dark-blue", "green", "ad-green"]
UI_LANGUAGES = ["english", "german", "french", "italian", "russian"]


class TestClass():

    def __init__(self):
        config_root = FileOps.resolve_development_path(__file__, "config", ".root")
        FileOps.purge_directory(config_root)

        self.window = ctk.CTk()

        logger_config = LoggerConfig(
            logger_name=LOGGER_NAME,
            log_name=LOG_NAME,
            log_directory=FileOps.resolve_development_path(__file__, "logs", ".root"),
            log_level=LOG_LEVEL.DEBUG,
            module_name=APP_NAME
        )
        self.logger = Logger(logger_config, rotate_on_init=True)

        ConfigHandler.add_config(
            config_name=CONFIG_NAME,
            handler_config=ConfigFileHandlerConfig(
                config_path=config_root,
                default_config_name="default-config.ini",
                custom_config_name="custom-config.ini",
            ),
            default_config=self._create_default_config(),
            custom_type_handlers=[
                ListTypeHandler(),
                TupleTypeHandler(),
                CtkStringVarTypeHandler(self.window),
                CtkBooleanVarTypeHandler(self.window),
            ]
        )
        self.create_config_keys()

    def create_config_keys(self):
        # Define the ConfigKeys
        config_data = [
            {"name": "locale_updater", "section": "AppSettings", "type_": ctk.BooleanVar, "config_name": CONFIG_NAME, "value": ctk.BooleanVar(value=False)},

            {"name": "locales_path", "section": "AppSettings", "type_": str, "config_name": CONFIG_NAME, "value": "locales"},
            {"name": "resources_path", "section": "AppSettings", "type_": str, "config_name": CONFIG_NAME, "value": "resources"},
            {"name": "input_path", "section": "AppSettings", "type_": str, "config_name": CONFIG_NAME, "value": "_input"},
            {"name": "output_path", "section": "AppSettings", "type_": str, "config_name": CONFIG_NAME, "value": "_output"},
            {"name": "dictionaries_path", "section": "AppSettings", "type_": str, "config_name": CONFIG_NAME, "value": "_dictionaries"},

            {"name": "save_window_size", "section": "WindowSettings", "type_": ctk.BooleanVar, "config_name": CONFIG_NAME, "value": ctk.BooleanVar(value=True)},
            {"name": "save_window_pos", "section": "WindowSettings", "type_": ctk.BooleanVar, "config_name": CONFIG_NAME, "value": ctk.BooleanVar(value=True)},
            {"name": "center_window_on_startup", "section": "WindowSettings", "type_": ctk.BooleanVar, "config_name": CONFIG_NAME, "value": ctk.BooleanVar(value=True)},
            {"name": "window_size", "section": "WindowSettings", "type_": ctk.StringVar, "config_name": CONFIG_NAME, "value": ctk.StringVar(value="1366x768")},
            {"name": "window_position", "section": "WindowSettings", "type_": ctk.StringVar, "config_name": CONFIG_NAME, "value": ctk.StringVar(value="0+0")},
            {"name": "resizeable", "section": "WindowSettings", "type_": ctk.BooleanVar, "config_name": CONFIG_NAME, "value": ctk.BooleanVar(value=True)},

            {"name": "use_high_dpi_scaling", "section": "AppearanceSettings", "type_": ctk.BooleanVar, "config_name": CONFIG_NAME, "value": ctk.BooleanVar(value=True)},
            {"name": "ui_theme", "section": "AppearanceSettings", "type_": ctk.StringVar, "config_name": CONFIG_NAME, "value": ctk.StringVar(value="System")},
            {"name": "ui_color_theme", "section": "AppearanceSettings", "type_": ctk.StringVar, "config_name": CONFIG_NAME, "value": ctk.StringVar(value="Blue")},
            {"name": "ui_language", "section": "AppearanceSettings", "type_": ctk.StringVar, "config_name": CONFIG_NAME, "value": ctk.StringVar(value="English")},

            {"name": "selected_languages", "section": "TranslationSettings", "type_": list, "config_name": CONFIG_NAME, "value": [""]},
            {"name": "supported_languages", "section": "TranslationSettings", "type_": list, "config_name": CONFIG_NAME, "value": ["English", "French", "German", "Italian", "Russian"]},
            {"name": "whole_word_replacement", "section": "TranslationSettings", "type_": ctk.BooleanVar, "config_name": CONFIG_NAME, "value": ctk.BooleanVar(value=True)},

            {"name": "dropdown_ui_themes", "section": "DropdownSettings", "type_": list, "config_name": CONFIG_NAME, "value": UI_THEMES},
            {"name": "dropdown_ui_color_themes", "section": "DropdownSettings", "type_": list, "config_name": CONFIG_NAME, "value": UI_COLOR_THEMES},
            {"name": "dropdown_ui_languages", "section": "DropdownSettings", "type_": list, "config_name": CONFIG_NAME, "value": UI_LANGUAGES}
        ]
        for data in config_data:
            # Add the ConfigKey's to the convenience class
            ConfigKeyList.add_ConfigKey(
                name=data["name"],
                section=data.get("section", "Default"),
                type_=data.get("type_", None),
                save_to_file=data.get("save_to_file", True),
                auto_save=data.get("auto_save", True),
                config_name=data.get("config_name", "Default")
            )
            # Create the actual ConfigVariable's by adding the appropriate ConfigKey's to the ConfigHandler
            ConfigHandler.add_variable(
                config_key=getattr(ConfigKeyList, data["name"].upper()),
                value=data.get("value", None),
                default_value=data.get("default_value", None),
                init_from_file=data.get("init_from_file", True)
            )

    def test_one(self):
        # With the help of the ConfigKeyList, we can now easily pass the ConfigKey's to the ConfigHandler
        test = ConfigHandler.get_variable(ConfigKeyList.LOCALE_UPDATER)
        test.subscribe("value_changed", lambda event_type, *args, **kwargs: self.logger.log_info(f"Value changed: {kwargs.get('new_value').get()}"))
        test.set_value(ctk.BooleanVar(value=True))
        print(test.get_value().get())

    def test_method(self):
        try:
            self.test_one()
        except Exception as e:
            self.logger.log_error(f"An error occurred: {str(e)}", "main")

    def _create_default_config(self):
        """Creates the default configuration."""
        return {
            "AppSettings": {
                "locale_updater": "False"
            },
            "WindowSettings": {
                "save_window_size": "True",
                "save_window_pos": "True",
                "center_window_on_startup": "True",
                "window_size": "1366x768",
                "window_position": "0+0",
                "resizeable": "True",
            },
            "AppearanceSettings": {
                "use_high_dpi_scaling": "True",
                "ui_theme": "System",
                "ui_color_theme": "Blue",
                "ui_language": "English"
            },
            "TranslationSettings": {
                "selected_languages": "English",
                "supported_languages": "English,French,German,Italian,Russian",
                "whole_word_replacement": "True"
            }
        }


def main():
    test_class = TestClass()
    test_class.test_method()


if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
