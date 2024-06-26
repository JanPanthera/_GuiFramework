# GuiFramework/gui/gui_manager/widget_builder/abstract_ctk_builder.py

import customtkinter as ctk

from GuiFramework.gui.gui_manager.widget_builder.abstract_builder import AbstractBuilder
from GuiFramework.utilities.logging import Logger

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

class AbstractCtkBuilder(AbstractBuilder):
    def __init__(self, localize_func=None):
        self.logger = Logger.get_logger("GuiFramework")
        super().__init__()
        self.loc = localize_func
        self.property_handlers = {
            "text": self.handle_text_property,
            "font": self.handle_font_property,
            "values": self.handle_value_property,
            "variable": self.handle_variable_property,
            "textvariable": self.handle_text_variable_property,
            "command": self.handle_command_property,
        }

    def handle_text_property(self, value, instance):
        try:
            if callable(self.loc):
                value = self.loc(value)
                self.logger.log_debug(f"Translated text: {value}", "AbstractCtkBuilder")
            return value
        except Exception as e:
            self.logger.log_error(f"Error handling text property: {e}", "AbstractCtkBuilder")
            return value

    def handle_font_property(self, value, instance):
        default_font = ("Arial", 12)
        if not isinstance(value, (dict, list)):
            return default_font
        if isinstance(value, dict):
            font_family = value.get("family", default_font[0])
            font_size = value.get("size", default_font[1])
            font_weight = value.get("weight", "")
            return (font_family, font_size, font_weight) if font_weight else (font_family, font_size)
        if isinstance(value, list):
            if len(value) < 2:
                return default_font
            font_family = value[0] if isinstance(value[0], str) else default_font[0]
            font_size = value[1] if isinstance(value[1], (int, float)) else default_font[1]
            font_weight = value[2] if len(value) > 2 and isinstance(value[2], str) else ""
            return (font_family, font_size, font_weight) if font_weight else (font_family, font_size)

    def handle_value_property(self, value, instance):
        return self._handle_property(value, instance)

    def handle_variable_property(self, variable, instance):
        return self._handle_property(variable, instance)

    def handle_text_variable_property(self, text_variable, instance):
        text_variable = self._handle_property(text_variable, instance)
        if text_variable is not None and not isinstance(text_variable, ctk.StringVar):
            try:
                text_variable = ctk.StringVar(value=str(text_variable))
            except Exception as e:
                self.logger.log_error(f"Error handling text_variable property: {e}", "AbstractCtkBuilder")
                text_variable = None
        return text_variable

    def handle_command_property(self, command, instance):
        _command = self._handle_property(command, instance)
        if _command is not None and not callable(_command):
            self.logger.log_warning(f"Command property {command} is not callable.", "AbstractCtkBuilder")
            _command = None
        return _command

    def _handle_property(self, property_name, instance):
        try:
            _property = getattr(instance, property_name, None)
            if _property is None and hasattr(instance, "get_var"):
                _property = instance.get_var(property_name)
            if _property is None and hasattr(instance, "get_variable"):
                _property = instance.get_variable(property_name)
            if _property is None and hasattr(CKL, property_name.upper()):
                _property = CH.get_variable_value(getattr(CKL, property_name.upper()))
            if _property is None:
                self.logger.log_warning(f"{property_name.capitalize()} property not found.", "AbstractCtkBuilder")
            return _property
        except Exception as e:
            self.logger.log_error(f"Error handling {property_name} property: {e}", "AbstractCtkBuilder")
            return None

    def apply_packing(self, widget, packing_properties):
        try:
            for key in ["padx", "pady", "ipadx", "ipady"]:
                if key in packing_properties:
                    packing_properties[key] = tuple(packing_properties[key])
            packing_type = packing_properties.pop("packing_type", "pack")
            getattr(widget, packing_type)(**packing_properties)
        except Exception as e:
            self.logger.log_error(f"Error applying packing properties: {e}", "AbstractCtkBuilder")

    def apply_grid_configuration(self, widget, grid_configuration):
        for row, config in grid_configuration.get("rows", {}).items():
            widget.rowconfigure(row, **config)
        for column, config in grid_configuration.get("columns", {}).items():
            widget.columnconfigure(column, **config)