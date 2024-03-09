# GuiFramework/utilities/gui_utils.py

from GuiFramework.utilities import CtkHelper, setup_default_logger


class GuiUtils:
    logger = setup_default_logger(log_name="GuiUtils", log_direrctory="logs/GuiFramework")

    @staticmethod
    def update_checkbox_state(checkbox, config_key, config_manager):
        """Updates the state of a checkbox based on a configuration value."""
        try:
            value = config_manager.get_variable(config_key).get()
            checkbox.select() if value else checkbox.deselect()
        except Exception as e:
            GuiUtils.logger.error(f"Failed to update checkbox state: {e}")

    @staticmethod
    def update_language(gui_manager, localize_func, frame_key):
        """Updates the language of the widgets in the given frame."""
        try:
            widgets = gui_manager.widgets.get(frame_key)
            for name_id, widget_ref in widgets.items():
                CtkHelper.update_widget_text(widget_ref, localize_func(name_id))
        except Exception as e:
            GuiUtils.logger.error(f"Failed to update language: {e}")

    @staticmethod
    def on_gui_build(class_ref, frame_key, gui_manager):
        """Sets the widget references for the given frame."""
        try:
            widgets = gui_manager.widgets.get(frame_key)
            for widget_name, widget_ref in widgets.items():
                setattr(class_ref, widget_name, widget_ref)
        except Exception as e:
            GuiUtils.logger.error(f"Failed to set widget references: {e}")
