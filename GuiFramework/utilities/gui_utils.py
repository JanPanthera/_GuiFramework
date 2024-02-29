# utilities/gui_utils.py

from .utils import setup_default_logger
from .helper_ctk import update_widget_text


def update_checkbox_state(checkbox, config_key, config_manager, logger=None):
    """Updates the state of a checkbox based on a configuration value."""
    logger = logger or setup_default_logger()
    try:
        value = config_manager.get_variable(config_key).get()
        checkbox.select() if value else checkbox.deselect()
    except Exception as e:
        logger.error(f"Failed to update checkbox state: {e}")


def update_language(gui_manager, localize_func, frame_key, logger=None):
    """Updates the language of the widgets in the given frame."""
    logger = logger or setup_default_logger()
    try:
        widgets = gui_manager.widgets.get(frame_key)
        for name_id, widget_ref in widgets.items():
            update_widget_text(widget_ref, localize_func(name_id))
    except Exception as e:
        logger.error(f"Failed to update language: {e}")


def set_widget_references(class_ref, frame_key, gui_manager, logger=None):
    """Sets the widget references for the given frame."""
    logger = logger or setup_default_logger()
    try:
        widgets = gui_manager.widgets.get(frame_key)
        for widget_name, widget_ref in widgets.items():
            setattr(class_ref, widget_name, widget_ref)
    except Exception as e:
        logger.error(f"Failed to set widget references: {e}")
