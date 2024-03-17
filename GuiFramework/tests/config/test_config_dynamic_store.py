# GuiFramework/tests/config/test_config_dynamic_store.py

from GuiFramework.utilities.config import ConfigDynamicStore


class TestConfigDynamicStore:
    """Class to test the dynamic configuration store functionality."""

    def __init__(self) -> None:
        """Initialize the test class with default values."""
        self.store_name: str = "test_store"
        ConfigDynamicStore.add_store(store_name=self.store_name)
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
            initial_store = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({}, initial_store)

            # Adding single variable
            ConfigDynamicStore.add_variable(self.store_name, "test", "test_value")
            after_add_variable = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({"test": "test_value"}, after_add_variable)

            # Adding multiple variables
            ConfigDynamicStore.add_variables(self.store_name, {"test1": "test_value1", "test2": "test_value2"})
            after_add_variables = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({"test": "test_value", "test1": "test_value1", "test2": "test_value2"}, after_add_variables)

            # Setting single variable
            ConfigDynamicStore.set_variable(self.store_name, "test", "new_test_value")
            after_set_variable = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({"test": "new_test_value", "test1": "test_value1", "test2": "test_value2"}, after_set_variable)

            # Setting multiple variables
            ConfigDynamicStore.set_variables(self.store_name, {"test1": "new_test_value1", "test2": "new_test_value2"})
            after_set_variables = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({"test": "new_test_value", "test1": "new_test_value1", "test2": "new_test_value2"}, after_set_variables)

            # Getting all dynamic store keys
            dynamic_store_keys = ConfigDynamicStore.get_dynamic_store_keys(self.store_name)
            self.assert_equals(["test", "test1", "test2"], sorted(dynamic_store_keys))

            # Getting single variable
            single_variable = ConfigDynamicStore.get_variable(self.store_name, 'test')
            self.assert_equals("new_test_value", single_variable)

            # Deleting single variable
            ConfigDynamicStore.delete_variable(self.store_name, "test")
            after_delete_variable = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({"test1": "new_test_value1", "test2": "new_test_value2"}, after_delete_variable)

            # Deleting multiple variables
            ConfigDynamicStore.delete_variables(self.store_name, ["test1", "test2"])
            after_delete_variables = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({}, after_delete_variables)

            # Clearing the dynamic store
            ConfigDynamicStore.clear_dynamic_store(self.store_name)
            after_clear_dynamic_store = ConfigDynamicStore.get_store(self.store_name)
            self.assert_equals({}, after_clear_dynamic_store)

        except Exception as e:
            self.error_count += 1
            print(f"Error: {e}")

        # Print success, fail, and error counts
        print(f"\nTest completed with {self.success_count} successes, {self.fail_count} failures, and {self.error_count} errors.")


def main() -> None:
    """Main function to run the test."""
    try:
        test = TestConfigDynamicStore()
        test.test_method()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    input("Press any key to continue...")
