# GuiFramework/tests/config/test_config_dynamic_store.py
# TODO:

from GuiFramework.utilities.config import ConfigDynamicStore


class TestConfigDynamicStore:
    def __init__(self):
        self.store_name = "test_store"
        ConfigDynamicStore.add_store(store_name=self.store_name)

    def test_method(self):
        pass


def main():
    try:
        test = TestConfigDynamicStore()
        test.test_method()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    input("Press any key to continue...")
