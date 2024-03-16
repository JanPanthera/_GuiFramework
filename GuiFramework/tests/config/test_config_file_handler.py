# GuiFramework/tests/config/test_config_file_handler.py

from typing import Any, Dict

from GuiFramework.utilities.file_ops import FileOps
from GuiFramework.utilities.config import ConfigFileHandler, ConfigFileHandlerConfig


class TestConfigFileHandler:
    """Test class for ConfigFileHandler functionality."""

    def __init__(self) -> None:
        """Initialize test configuration file handler."""
        # Purge to ensure a clean state
        FileOps.purge_directory(FileOps.resolve_development_path(__file__, "config", ".root"))
        self.config_name: str = "test_config"
        ConfigFileHandler.add_config(
            config_name=self.config_name,
            handler_config=ConfigFileHandlerConfig(
                config_path=FileOps.resolve_development_path(__file__, "config", ".root"),
                default_config_name="test_default_config.ini",
                custom_config_name="test_custom_config.ini"
            ),
            default_config={
                "window": {
                    "title": "Test Application",
                    "size": "1920, 1080",
                    "position": "300, 100",
                    "test_value": "test_value"
                }
            }
        )
        self.success_count: int = 0
        self.fail_count: int = 0
        self.error_count: int = 0

    def assert_equals(self, expected: Any, actual: Any) -> None:
        """Assert if expected equals actual, incrementing the respective count."""
        try:
            if expected == actual:
                self.success_count += 1
            else:
                print(f"Expected: {expected}, Actual: {actual}")
                self.fail_count += 1
        except Exception as e:
            self.error_count += 1
            print(f"Error: {e}\n")

    def test_method(self) -> None:
        """Run tests on config file handler operations and log results."""
        try:
            # Initial config state
            initial_config: Dict[str, Any] = ConfigFileHandler.get_custom_config(self.config_name)
            self.assert_equals({
                "window": {
                    "title": "Test Application",
                    "size": "1920, 1080",
                    "position": "300, 100",
                    "test_value": "test_value",
                }
            }, initial_config)

            # Save single setting
            ConfigFileHandler.save_setting(self.config_name, "window", "title", "Test Application1")
            initial_config["window"]["title"] = "Test Application1"
            self.assert_equals(initial_config, ConfigFileHandler.get_custom_config(self.config_name))

            # Save multiple settings
            ConfigFileHandler.save_settings(self.config_name, {
                "window": {
                    "size": "900, 800",
                    "position": "100, 300",
                },
                "test": {
                    "value": "test_value1",
                }
            })
            initial_config["window"]["size"] = "900, 800"
            initial_config["window"]["position"] = "100, 300"
            initial_config.setdefault("test", {})["value"] = "test_value1"
            self.assert_equals(initial_config, ConfigFileHandler.get_custom_config(self.config_name))

            # Get single setting
            self.assert_equals("Test Application1", ConfigFileHandler.get_setting(self.config_name, "window", "title"))

            # Get multiple settings
            # Dict[section, Dict[option, fallback_value]]
            settings = ConfigFileHandler.get_settings(self.config_name,
                                                      {
                                                          "window": {"size": None, "position": None},
                                                          "test": {"value": None},
                                                      })
            self.assert_equals({
                "window": {
                    "size": "900, 800",
                    "position": "100, 300",
                },
                "test": {
                    "value": "test_value1",
                }
            }, settings)

            # Reset a single setting
            ConfigFileHandler.reset_setting(self.config_name, "window", "title")
            initial_config["window"]["title"] = "Test Application"
            self.assert_equals(initial_config, ConfigFileHandler.get_custom_config(self.config_name))

            # Reset multiple settings
            ConfigFileHandler.reset_settings(self.config_name, {
                "window": ["size", "position"],
            })
            initial_config["window"]["size"] = "1920, 1080"
            initial_config["window"]["position"] = "300, 100"
            self.assert_equals(initial_config, ConfigFileHandler.get_custom_config(self.config_name))

            # Reset an entire section
            ConfigFileHandler.reset_section(self.config_name, "window")
            initial_config["window"] = {
                "title": "Test Application",
                "size": "1920, 1080",
                "position": "300, 100",
                "test_value": "test_value",
            }
            self.assert_equals(initial_config, ConfigFileHandler.get_custom_config(self.config_name))

            # Reset config
            ConfigFileHandler.reset_custom_config(self.config_name)
            self.assert_equals(ConfigFileHandler.get_default_config(self.config_name), ConfigFileHandler.get_custom_config(self.config_name))

        except Exception as e:
            self.error_count += 1
            print(f"Error: {e}")

        # Print success, fail, and error counts
        print(f"\nTest completed with {self.success_count} successes, {self.fail_count} failures, and {self.error_count} errors.")


def main() -> None:
    """Main function to run the test."""
    try:
        test = TestConfigFileHandler()
        test.test_method()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    input("Press any key to continue...")
