# widget_builder.py

import customtkinter as ctk


class WidgetBuilder:
    def __init__(self, config_manager=None, localization_function=None, logger=None):
        self.logger = logger
        self.loc = localization_function
        self.config_manager = config_manager
        self.widget_creators = {
            "CTkFrame": ctk.CTkFrame,
            "CTkLabel": ctk.CTkLabel,
            "CTkEntry": ctk.CTkEntry,
            "CTkButton": ctk.CTkButton,
            "CTkTextbox": ctk.CTkTextbox,
            "CTkCheckBox": ctk.CTkCheckBox,
            "CTkOptionMenu": ctk.CTkOptionMenu
        }
        self.default_font = ("Helvetica", 16)

    def register_widget_creator(self, widget_type, widget_creator):
        self.widget_creators[widget_type] = widget_creator

    def create_widget(self, widget_type, widget_properties, master, instance):
        loc = self.loc
        config_manager = self.config_manager
        widget_creators = self.widget_creators

        if 'text' in widget_properties and loc:
            widget_properties['text'] = loc(widget_properties['text'])
        if 'font' in widget_properties:
            widget_properties['font'] = self._convert_font_property(widget_properties['font'])

        if 'values' in widget_properties:
            values = getattr(instance, widget_properties['values'], None)
            if values is None and config_manager:
                values = config_manager.get_variable(widget_properties['values'])
            if isinstance(values, ctk.StringVar) and loc:
                values.set(loc(values.get()))
            if isinstance(values, str) and loc:
                values = loc(values)
            if isinstance(values, list) and all(isinstance(v, str) for v in values):
                values = [loc(v) for v in values]
            widget_properties['values'] = values

        if 'variable' in widget_properties:
            variable = getattr(instance, widget_properties['variable'], None)
            if variable is None and config_manager:
                variable = config_manager.get_variable(widget_properties['variable'])
            if isinstance(variable, ctk.StringVar) and loc:
                variable.set(loc(variable.get()))
                print(variable.get())
            if isinstance(variable, str) and loc:
                variable = loc(variable)
            widget_properties['variable'] = variable

        if 'command' in widget_properties:
            command = getattr(instance, widget_properties['command'], None)
            if command is None and config_manager:
                command = config_manager.get_variable(widget_properties['command'])
            widget_properties['command'] = command

        widget_class = widget_creators.get(widget_type)
        if not widget_class:
            raise ValueError(f"Unsupported widget type: {widget_type}")

        return widget_class(master=master, **widget_properties)

    def _convert_font_property(self, font_prop):
        if isinstance(font_prop, dict):
            font_family = font_prop.get('family', self.default_font[0])
            font_size = font_prop.get('size', self.default_font[1])
            font_weight = font_prop.get('weight')
            return (font_family, font_size, font_weight) if font_weight else (font_family, font_size)
        elif isinstance(font_prop, list):
            font_prop.extend(self.default_font[len(font_prop):])
            return tuple(font_prop)
        else:
            return font_prop
