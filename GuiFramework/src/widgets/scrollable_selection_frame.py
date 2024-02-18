import customtkinter as ctk
from src.utilities.utils import handle_exception, trigger_debug_break


class ScrollableSelectionFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, variable=None, values=None, widget_type='checkbox', single_select=False, command=None, font=None, logger=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.custom_font = font
        self.widget_type = widget_type
        self.single_select = single_select
        self.logger = logger
        self.widgets = {}
        self.states = {}

        if variable:
            if isinstance(variable, str):
                variable = variable.split(',')
            self.add_entries(variable)

        if values:
            if isinstance(values, str):
                values = values.split(',')
            self.set_entries_state(values, True)

    # Public Methods
    def add_entry(self, entry):
        if entry in self.states:
            self._log_warning(f"Attempted to add a duplicate entry: '{entry}'")
            return
        self.states[entry] = False
        self._create_and_place_widget(entry)

    def add_entries(self, entries):
        for entry in entries:
            self.add_entry(entry)

    def remove_entry(self, entry):
        widget = self.widgets.pop(entry, None)
        if widget:
            widget.destroy()
            self.states.pop(entry, None)

    def remove_entries(self, entries):
        for entry in entries:
            self.remove_entry(entry)

    def remove_checked_entries(self):
        checked_entries = self.get_checked_entries()
        self.remove_entries(checked_entries)

    def remove_all_entries(self):
        while self.widgets:
            self.remove_entry(next(iter(self.widgets)))

    def set_entry_state(self, entry, state):
        if entry not in self.states:
            self._log_warning(f"Attempted to set state for non-existent entry: '{entry}'")
            return
        self.states[entry] = state
        self._update_widget_for_entry(entry)

    def set_entries_state(self, entries, state):
        for entry in entries:
            self.set_entry_state(entry, state)

    def set_all_entries_state(self, state):
        for entry in self.states:
            self.set_entry_state(entry, state)

    def get_checked_entries(self):
        return [entry for entry, state in self.states.items() if state]

    def get_all_entries(self):
        return list(self.states)

    def toggle_entry(self, entry):
        if self.single_select:
            if not self.states[entry]:
                for key in self.states.keys():
                    self.states[key] = False
                self.states[entry] = True
                self._update_all_widgets()
        else:
            self._toggle_entry_state(entry)
        self._execute_command(entry)
        self._update_widget_state(self.widgets.get(entry))

    def toggle_entries(self, entries):
        for entry in entries:
            self.toggle_entry(entry)

    def toggle_selected_entries(self):
        checked_entries = self.get_checked_entries()
        self.toggle_entries(checked_entries)

    def toggle_all_entries(self):
        self.toggle_entries(self.states)

    def sort_entries(self, key=None):
        key = key or str.lower
        sorted_entries = sorted(self.states, key=key)
        self._rearrange_widgets(sorted_entries)

    # Private Methods
    def _create_and_place_widget(self, entry):
        def widget_command(entry=entry): return self.toggle_entry(entry)
        widget = self._create_widget(entry, widget_command)
        widget.grid(row=len(self.widgets), column=0, pady=(0, 5), sticky='nw')
        self.widgets[entry] = widget
        self._update_widget_state(widget)

    def _toggle_entry_state(self, entry):
        self.states[entry] = not self.states.get(entry, False)

    def _create_widget(self, entry, command):
        widget_factory = {
            'checkbox': lambda: ctk.CTkCheckBox(self, text=entry, command=command, font=self.custom_font),
            'radio': lambda: self._create_radio_button(entry, command),
            'label': lambda: self._create_label(entry, command)
        }
        return widget_factory.get(self.widget_type, lambda: None)()

    def _create_radio_button(self, entry, command):
        widget = ctk.CTkRadioButton(self, text=entry, font=self.custom_font, command=lambda: None)
        widget.bind("<Button-1>", lambda event: command(), add=True)
        return widget

    def _create_label(self, entry, command):
        widget = ctk.CTkLabel(self, text=entry, font=self.custom_font)
        widget.bind("<Button-1>", lambda event: command(), add=True)
        return widget

    def _execute_command(self, entry):
        try:
            if self.command:
                self.command(entry)
        except Exception as e:
            self._log_error(f"Error executing command for entry '{entry}': {e}")
            handle_exception(e, f"Error executing command for entry '{entry}'")

    def _log_warning(self, message):
        if self.logger:
            self.logger.warning(message)

    def _log_error(self, message):
        if self.logger:
            self.logger.error(message)

    def _update_widget_state(self, widget):
        entry = widget.cget("text")
        is_selected = self.states[entry]
        if self.widget_type in ['checkbox', 'radio']:
            widget.select() if is_selected else widget.deselect()
        elif self.widget_type == 'label':
            self._update_label_widget_state(widget, is_selected)

    def _update_label_widget_state(self, widget, is_selected):
        widget.configure(bg_color="gray75" if is_selected else "transparent", text_color="gray14" if is_selected else "gray84")

    def _update_all_widgets(self):
        for entry, widget in self.widgets.items():
            self._update_widget_state(widget)

    def _place_widget_in_grid(self, widget, position):
        widget.grid(row=position, column=0, pady=(0, 5), sticky='nw')

    def _rearrange_widgets(self, sorted_entries):
        for index, entry in enumerate(sorted_entries):
            widget = self.widgets.get(entry)
            if widget:
                widget.grid(row=index, column=0, pady=(0, 5), sticky='nw')
        self.widgets = {entry: self.widgets[entry] for entry in sorted_entries}

    def _update_widget_for_entry(self, entry):
        widget = self.widgets.get(entry)
        if widget:
            self._update_widget_state(widget)
