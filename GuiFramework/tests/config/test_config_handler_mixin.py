# GuiFramework/tests/config/test_config_handler_mixin.py

from GuiFramework.utilities import FileOps
from GuiFramework.utilities.config import ConfigHandlerMixin, ConfigFileHandlerConfig, CustomTypeHandlerBase


# Custom type handler for serializing and deserializing tuples as strings
class TupleTypeHandler(CustomTypeHandlerBase):
    def serialize(self, tuple_value: tuple) -> str:
        """Convert tuple to comma-separated string."""
        self.validate_type(tuple_value, tuple, "tuple")
        return ",".join(map(str, tuple_value)) if tuple_value else ""

    def deserialize(self, tuple_string: str) -> tuple:
        """Convert comma-separated string to tuple."""
        self.validate_type(tuple_string, str, "string")
        return tuple((int(item) if item.isdigit() else item) for item in map(str.strip, tuple_string.split(","))) if tuple_string else ()

    def get_type(self) -> type:
        """Return the Python type this handler is responsible for."""
        return tuple


# Custom type handler for serializing and deserializing matrices (lists of lists) as strings
class MatrixTypeHandler(CustomTypeHandlerBase):
    def serialize(self, matrix_value: list) -> str:
        """Convert matrix to semicolon and comma-separated string."""
        self.validate_type(matrix_value, list, "list")
        return ";".join(",".join(map(str, row)) for row in matrix_value) if matrix_value else ""

    def deserialize(self, matrix_string: str) -> list:
        """Convert semicolon and comma-separated string to matrix."""
        self.validate_type(matrix_string, str, "string")
        return [list(map(str.strip, item.split(","))) for item in matrix_string.split(";")] if matrix_string else []

    def get_type(self) -> type:
        """Return the Python type this handler is responsible for."""
        return list


class TestConfigHandlerMixin(ConfigHandlerMixin):

    def __init__(self) -> None:
        """Initialize test configuration with default settings and custom type handlers."""
        # Purge to ensure a clean state
        config_dir = FileOps.resolve_development_path(__file__, "config", ".root")
        FileOps.purge_directory(config_dir)

        super().__init__(
            config_name="test-config",
            handler_config=ConfigFileHandlerConfig(
                config_path=config_dir,
                default_config_name="default-config.ini",
                custom_config_name="custom-config.ini",
            ),
            default_config={
                "window": {
                    "title": "Test Application",
                    "size": "1920, 1080",
                    "position": "300, 100",
                    "test_value": "test_value",
                }
            },
            custom_type_handlers={
                tuple: TupleTypeHandler(),
            },
        )

    def test_method(self) -> None:
        """Demonstrate saving, retrieving, and resetting settings using custom type handlers."""
        # Add custom type handler for matrices after the config was already added
        self.add_custom_type_handler(MatrixTypeHandler())

        # Demonstrate saving and retrieving settings
        self.save_setting("window", "title", "Test Application")
        title = self.get_setting("window", "title", fallback_value="default_value")
        print(f"Title: {title}")

        # Demonstrate using custom type handlers
        self.save_setting("window", "test_value", (1, 2, 3))
        tuple_value = self.get_setting("window", "test_value", fallback_value=(0, 0, 0))
        print(f"Tuple value: {tuple_value}")

        self.save_setting("window", "test_value", [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix_value = self.get_setting("window", "test_value", fallback_value=[])
        print(f"Matrix value: {matrix_value}")

        # Demonstrate saving and retrieving multiple settings at once
        settings_to_save = {
            "window": {
                "title": "Test Application",
                "size": (1920, 1080),
                "position": (300, 100),
                "test_value": "test_value",
            }
        }
        self.save_settings(settings_to_save)
        retrieved_settings = self.get_settings(settings_to_save)
        print(f"Retrieved settings: {retrieved_settings}")

        # Demonstrate resetting settings, sections, and entire config
        self.reset_setting("window", "title")
        self.reset_section("window")
        self.reset_custom_config()

        # Demonstrate saving and loading custom config to/from a file
        self.save_custom_config_to_file()
        self.load_custom_config_from_file()

        # Print the current configuration
        print(self.get_custom_config())

        print("Manual test script executed successfully.")


def main() -> None:
    """Execute manual test script for configuration handling."""
    try:
        test = TestConfigHandlerMixin()
        test.test_method()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    input("Press any key to continue...")
