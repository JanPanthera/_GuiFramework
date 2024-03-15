# GuiFramework/tests/config/test_config_file_handler_mixin.py

from typing import Any, Dict

from GuiFramework.utilities import FileOps
from GuiFramework.utilities.config import ConfigFileHandlerMixin, ConfigFileHandlerConfig


class TestConfigFileHandlerMixin(ConfigFileHandlerMixin):
    """Test class for ConfigFileHandlerMixin functionality."""

    def __init__(self) -> None:
        """Initialize test configuration file handler."""
        # Purge to ensure a clean slate
        FileOps.purge_directory(FileOps.resolve_development_path(__file__, "config", ".root"))
        super().__init__(
            config_name="test-config",
            handler_config=ConfigFileHandlerConfig(
                config_path=FileOps.resolve_development_path(__file__, "config", ".root"),
                default_config_name="default-config.ini",
                custom_config_name="custom-config.ini"
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
            initial_config: Dict[str, Any] = self.get_custom_config()
            self.assert_equals({
                "window": {
                    "title": "Test Application",
                    "size": "1920, 1080",
                    "position": "300, 100",
                    "test_value": "test_value",
                }
            }, initial_config)

            # Save single setting
            self.save_setting("window", "title", "Test Application1")
            initial_config["window"]["title"] = "Test Application1"
            self.assert_equals(initial_config, self.get_custom_config())

            # Save multiple settings
            self.save_settings({
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
            self.assert_equals(initial_config, self.get_custom_config())

            # Get single setting
            self.assert_equals("Test Application1", self.get_setting("window", "title"))

            # Get multiple settings
            # Dict[section, Dict[option, fallback_value]]
            settings = self.get_settings({
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
            self.reset_setting("window", "title")
            initial_config["window"]["title"] = "Test Application"
            self.assert_equals(initial_config, self.get_custom_config())

            # Reset multiple settings
            self.reset_settings({
                "window": ["size", "position"],
            })
            initial_config["window"]["size"] = "1920, 1080"
            initial_config["window"]["position"] = "300, 100"
            self.assert_equals(initial_config, self.get_custom_config())

            # Reset an entire section
            self.reset_section("window")
            initial_config["window"] = {
                "title": "Test Application",
                "size": "1920, 1080",
                "position": "300, 100",
                "test_value": "test_value",
            }
            self.assert_equals(initial_config, self.get_custom_config())

            # Reset config
            self.reset_custom_config()
            self.assert_equals(self.get_default_config(), self.get_custom_config())

        except Exception as e:
            self.error_count += 1
            print(f"Error: {e}")

        # Print success, fail, and error counts
        print(f"\nTest completed with {self.success_count} successes, {self.fail_count} failures, and {self.error_count} errors.")


def main():
    """Main function to run the test."""
    try:
        test = TestConfigFileHandlerMixin()
        test.test_method()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    input("Press any key to continue...")