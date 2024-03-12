import unittest
from unittest.mock import patch, MagicMock
from GuiFramework.utilities.config._config_file_handler import _ConfigFileHandler, ConfigFileHandlerConfig
from GuiFramework.utilities.file_ops import FileOps


class TestConfigFileHandler(unittest.TestCase):

    def setUp(self):
        self.config_name = "test_config"
        self.handler_config = ConfigFileHandlerConfig(
            config_path=FileOps.resolve_development_path(__file__, "config", ".root"),
            default_config_name="test_default.ini",
            custom_config_name="test_custom.ini",
            default_config_creator_func=lambda: {
                "section": {
                    "option": "value"
                }
            },
        )
        _ConfigFileHandler._add_config(self.config_name, self.handler_config)

    def test_add_config(self):
        with patch.object(_ConfigFileHandler, '_sync_default_config') as mock_sync_default, \
                patch.object(_ConfigFileHandler, '_sync_custom_config') as mock_sync_custom:
            _ConfigFileHandler._add_config("new_config", self.handler_config)
            mock_sync_default.assert_called_once()
            mock_sync_custom.assert_called_once()

    def test_sync_default_config(self):
        with patch.object(_ConfigFileHandler, '_sync_config') as mock_sync:
            _ConfigFileHandler._sync_default_config(self.config_name)
            mock_sync.assert_called_once_with(self.config_name, 'default')

    def test_sync_custom_config(self):
        with patch.object(_ConfigFileHandler, '_sync_config') as mock_sync:
            _ConfigFileHandler._sync_custom_config(self.config_name)
            mock_sync.assert_called_once_with(self.config_name, 'custom')

    def test_save_setting(self):
        with patch.object(_ConfigFileHandler, '_write_config_to_file') as mock_write:
            _ConfigFileHandler._save_setting(self.config_name, "section", "option", "value")
            mock_write.assert_called_once()

    def test_get_setting(self):
        # Setup: Add a section and an option to the configuration
        _ConfigFileHandler._save_setting(self.config_name, "section", "option", "value")

        # Test: Try to get the setting
        value = _ConfigFileHandler._get_setting(self.config_name, "section", "option", fallback_value="default")
        self.assertEqual(value, "value")

    def test_reset_setting(self):
        # Setup: Add a section and an option to the configuration
        _ConfigFileHandler._save_setting(self.config_name, "section", "option", "value")

        # Test: Try to reset the setting
        with patch.object(_ConfigFileHandler, '_write_config_to_file') as mock_write:
            _ConfigFileHandler._reset_setting(self.config_name, "section", "option")
            mock_write.assert_called_once()

    def test_reset_section(self):
        # Setup: Add a section to the configuration
        _ConfigFileHandler._save_setting(self.config_name, "section", "option", "value")

        # Test: Try to reset the section
        with patch.object(_ConfigFileHandler, '_write_config_to_file') as mock_write:
            _ConfigFileHandler._reset_section(self.config_name, "section")
            mock_write.assert_called_once()

        def test_reset_config(self):
            with patch.object(_ConfigFileHandler, '_write_config_to_file') as mock_write:
                _ConfigFileHandler._reset_config(self.config_name)
                mock_write.assert_called_once()


if __name__ == '__main__':
    unittest.main(exit=False)
    input("Press Enter to continue...")
