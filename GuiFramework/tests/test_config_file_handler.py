
from GuiFramework.utilities.config._config_file_handler import _ConfigFileHandler, ConfigFileHandlerConfig
from GuiFramework.utilities.file_ops import FileOps


class TestConfigFileHandler:
    def __init__(self):
        self.config_name = "test_config"
        _ConfigFileHandler._add_config(
            config_name=self.config_name,
            handler_config=ConfigFileHandlerConfig(
                config_path=FileOps.resolve_development_path(start_path=__file__, sub_path="config", root_marker=".root"),
                default_config_name="test_default_config.ini",
                custom_config_name="test_custom_config.ini",
                default_config_creator_func=lambda: {
                    "section1": {
                        "option1": "value1"
                    }
                }
            )
        )

    def test_method(self):
        # _ConfigFileHandler._save_setting(config_name=self.config_name, section="section1", option="option2", value="value2")
        print(_ConfigFileHandler._get_setting(config_name=self.config_name, section="section1", option="option1"))
        print(_ConfigFileHandler._get_setting(config_name=self.config_name, section="section1", option="option2"))
        _ConfigFileHandler._save_settings(
            config_name=self.config_name,
            settings={
                "section2": {
                    "option1": "value1",
                    "option2": "value2"
                }
            },
            auto_save=False
        )
        test = _ConfigFileHandler._get_settings(
            config_name=self.config_name,
            settings={
                "section1": {
                    "option1": None,
                    "option2": None
                },
                "section2": {
                    "option1": None,
                    "option2": None
                }
            }
        )
        print(test)
        _ConfigFileHandler._save_custom_config_to_file(config_name=self.config_name)


if __name__ == '__main__':
    try:
        test = TestConfigFileHandler()
        test.test_method()
    except Exception as e:
        print(e)
    input("Press Enter to continue...")
