# abstract_builder.py ~ GuiFramework/gui/gui_manager/abstract_builder.py

import abc
from ...utilities import setup_default_logger


class AbstractBuilder(abc.ABC):
    def __init__(self, logger=None):
        self.logger = logger if logger else setup_default_logger('AbstractBuilder')

    @property
    @abc.abstractmethod
    def widget_type(self):
        """Return the widget type name."""
        pass

    @abc.abstractmethod
    def create_widget(self, master, widget_properties):
        """Create a widget and return it."""
        pass

    @property
    @abc.abstractmethod
    def property_handlers(self):
        """Handle passed properties like text, font etc."""
        pass

    def default_property_handlers(self):
        """Return the default property handlers."""
        return {
            'text': self.handle_text_property,
            'font': self.handle_font_property,
            'value': self.handle_value_property,
            'variable': self.handle_variable_property,
            'command': self.handle_command_property
        }

    def handle_text_property(self, value):
        """Handle the 'text' property with a default or overridden implementation."""
        return value

    def handle_font_property(self, value):
        """Handle the 'font' property with a default or overridden implementation."""
        default_font = ("Helvetica", 12)
        if isinstance(value, dict):
            font_family = value.get('family', default_font[0])
            font_size = value.get('size', default_font[1])
            return (font_family, font_size)
        elif isinstance(value, list):
            value.extend(default_font[len(value):])
            return tuple(value)
        else:
            return default_font

    def handle_value_property(self, value):
        # Implement value property handling with error checking
        return value

    def handle_variable_property(self, value):
        # Implement variable property handling with error checking
        return value

    def handle_command_property(self, value):
        # Implement command property handling with error checking
        return value

    def apply_packing(self, widget, packing_properties):
        try:
            for key in ['padx', 'pady', 'ipadx', 'ipady']:
                if key in packing_properties:
                    packing_properties[key] = tuple(packing_properties[key])
            packing_type = packing_properties.pop("packing_type", "pack")
            getattr(widget, packing_type)(**packing_properties)
        except Exception as e:
            self.logger.error(f"Error applying packing properties: {e}")

    def apply_grid_configuration(self, widget, grid_configuration):
        """Apply grid configuration to the widget or its master."""
        for row, config in grid_configuration.get("rows", {}).items():
            widget.rowconfigure(row, **config)
        for column, config in grid_configuration.get("columns", {}).items():
            widget.columnconfigure(column, **config)
