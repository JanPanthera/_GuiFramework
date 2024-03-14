# GuiFramework/tests/config/test_config_dynamic_store_mixin.py

from GuiFramework.utilities.config import ConfigDynamicStoreMixin


class TestConfigDynamicStoreMixin(ConfigDynamicStoreMixin):
    """Test class for ConfigDynamicStoreMixin functionality."""

    def __init__(self) -> None:
        """Initialize test class with default values."""
        super().__init__(config_name="test-config")
        self.success_count: int = 0
        self.fail_count: int = 0
        self.error_count: int = 0

    def assert_equals(self, expected: any, actual: any) -> None:
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
        """Run tests on dynamic store operations and log results."""
        try:
            # Initial store state
            initial_store = self.get_store()
            self.assert_equals({}, initial_store)

            # Adding single variable
            self.add_variable("test", "test_value")
            after_add_variable = self.get_store()
            self.assert_equals({"test": "test_value"}, after_add_variable)

            # Adding multiple variables
            self.add_variables({"test1": "test_value1", "test2": "test_value2"})
            after_add_variables = self.get_store()
            self.assert_equals({"test": "test_value", "test1": "test_value1", "test2": "test_value2"}, after_add_variables)

            # Setting single variable
            self.set_variable("test", "new_test_value")
            after_set_variable = self.get_store()
            self.assert_equals({"test": "new_test_value", "test1": "test_value1", "test2": "test_value2"}, after_set_variable)

            # Setting multiple variables
            self.set_variables({"test1": "new_test_value1", "test2": "new_test_value2"})
            after_set_variables = self.get_store()
            self.assert_equals({"test": "new_test_value", "test1": "new_test_value1", "test2": "new_test_value2"}, after_set_variables)

            # Getting all dynamic store keys
            dynamic_store_keys = self.get_dynamic_store_keys()
            self.assert_equals(["test", "test1", "test2"], sorted(dynamic_store_keys))

            # Getting single variable
            single_variable = self.get_variable('test')
            self.assert_equals("new_test_value", single_variable)

            # Deleting single variable
            self.delete_variable("test")
            after_delete_variable = self.get_store()
            self.assert_equals({"test1": "new_test_value1", "test2": "new_test_value2"}, after_delete_variable)

            # Deleting multiple variables
            self.delete_variables(["test1", "test2"])
            after_delete_variables = self.get_store()
            self.assert_equals({}, after_delete_variables)

            # Clearing the dynamic store
            self.clear_dynamic_store()
            after_clear_dynamic_store = self.get_store()
            self.assert_equals({}, after_clear_dynamic_store)

        except Exception as e:
            self.error_count += 1
            print(f"Error: {e}")

        # Print success, fail, and error counts
        print(f"\nTest completed with {self.success_count} successes, {self.fail_count} failures, and {self.error_count} errors.")


def main() -> None:
    """Main function to run the test."""
    try:
        test = TestConfigDynamicStoreMixin()
        test.test_method()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    input("Press any key to continue...")
