# GuiFramework/gui/gui_manager/widget_builder/scrollable_selection_frame_Builder.py

from GuiFramework.widgets import scrollable_selection_frame as ssf
from GuiFramework.gui.gui_manager.widget_builder.abstract_ctk_builder import AbstractCtkBuilder
from GuiFramework.utilities import setup_default_logger


class ScrollableSelectionFrameBuilder(AbstractCtkBuilder):
    def __init__(self, config_manager=None, localize_func=None, logger=None):
        super().__init__(config_manager, localize_func, logger)
        self.logger = logger or setup_default_logger(log_name="ScrollableSelectionFrameBuilder", log_directory="logs/GuiFramework")

    @property
    def widget_type(self):
        return "ScrollableSelectionFrame"

    def create_widget(self, master, widget_properties, instance):
        try:
            property_handlers = self.property_handlers
            # Apply ScrollableSelectionFrame specific property handlers to property_handlers dict if any

            # Create ScrollableSelectionFrame with processed properties
            for property_name, handler in self.property_handlers.items():
                if property_name in widget_properties:
                    widget_properties[property_name] = handler(widget_properties[property_name], instance)

            widget = ssf.ScrollableSelectionFrame(master, **widget_properties)
            self.logger.debug(f"ScrollableSelectionFrame created with properties: {widget_properties}")
            return widget
        except Exception as e:
            self.logger.error(f"Error creating ScrollableSelectionFrame: {e}")
            return None