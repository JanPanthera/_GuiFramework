# test_config_manager.py

import unittest
from GuiFramework.src.utilities import ConfigManager


def create_default_config():
    return {
        'Settings': {
            'use_high_dpi_scaling': 'True',
            'ui_theme': 'System',
            'ui_language': 'English',
            'selected_languages': 'English',
            'supported_languages': 'Chinese,English,French,German,Italian,Japanese,Korean,Portuguese,Russian,Spanish',
            'input_path': '_input',
            'output_path': '_output',
            'dictionaries_path': '_dictionaries'
        },
        'TranslationSettings': {
            'whole_word_replacement': 'False'
        },
        'SaveOnWindowClose': {
            'save_window_size': 'True',
            'save_window_pos': 'True',
            'save_selected_languages': 'False'
        },
        'WindowGeometry': {
            'width': '1366',
            'height': '768',
            'pos_x': '0',
            'pos_y': '0'
        }
    }


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_manager = ConfigManager(create_default_config, "AutoDriveTranslationTool/config/default_config.ini", "AutoDriveTranslationTool/config/custom_config.ini")

    def test_register_type_creator(self):
        # Test case for register_type_creator method...
        pass

    def test_load_config(self):
        # Test that the configuration files are loaded correctly
        self.config_manager.load_config()
        self.assertTrue(self.config_manager.default_config.sections())
        self.assertTrue(self.config_manager.custom_config.sections())

    def test_save_setting(self):
        # Test that a setting is saved correctly
        self.config_manager.save_setting('TestSection', 'TestOption', 'TestValue')
        self.assertEqual(self.config_manager.custom_config.get('TestSection', 'TestOption'), 'TestValue')

    def test_save_settings(self):
        # Test that multiple settings are saved correctly
        self.config_manager.save_settings('TestSection', {'TestOption1': 'TestValue1', 'TestOption2': 'TestValue2'})
        self.assertEqual(self.config_manager.custom_config.get('TestSection', 'TestOption1'), 'TestValue1')
        self.assertEqual(self.config_manager.custom_config.get('TestSection', 'TestOption2'), 'TestValue2')

    def test_load_setting(self):
        # Test that a setting is loaded correctly
        value = self.config_manager.load_setting('TestSection', 'TestOption')
        self.assertEqual(value, 'TestValue')

    def test_reset_setting(self):
        # Test that a setting is reset correctly
        self.config_manager.default_config.add_section('TestSection')
        self.config_manager.default_config.set('TestSection', 'TestOption', 'DefaultValue')
        self.config_manager.reset_setting('TestSection', 'TestOption')
        self.assertEqual(self.config_manager.custom_config.get('TestSection', 'TestOption'), self.config_manager.default_config.get('TestSection', 'TestOption'))

    def test_reset_settings(self):
        # Test that all settings in a section are reset correctly
        self.config_manager.default_config.add_section('TestSection')
        self.config_manager.default_config.set('TestSection', 'TestOption1', 'DefaultValue1')
        self.config_manager.default_config.set('TestSection', 'TestOption2', 'DefaultValue2')
        self.config_manager.reset_settings('TestSection')
        self.assertEqual(self.config_manager.custom_config.items('TestSection'), self.config_manager.default_config.items('TestSection'))

    def test_reset_all_settings(self):
        # Test that all settings in all sections are reset correctly
        self.config_manager.reset_all_settings()
        for section in self.config_manager.default_config.sections():
            self.assertEqual(self.config_manager.custom_config.items(section), self.config_manager.default_config.items(section))

    def test_add_variable(self):
        # Test that a variable is added correctly
        self.config_manager.add_variable('TestVariable', 'TestValue')
        self.assertEqual(self.config_manager.dynamic_store.get('TestVariable'), 'TestValue')

    def test_get_variable(self):
        # Test that a variable is retrieved correctly
        self.config_manager.add_variable('TestVariable', 'TestValue')
        value = self.config_manager.get_variable('TestVariable')
        self.assertEqual(value, 'TestValue')

    def test_set_variable(self):
        # Test that a variable is set correctly
        self.config_manager.set_variable('TestVariable', 'NewValue')
        self.assertEqual(self.config_manager.dynamic_store.get('TestVariable'), 'NewValue')


if __name__ == '__main__':
    unittest.main(exit=False)
    input("Press Enter to continue...")
