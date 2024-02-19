# custom_console_textbox.py

import customtkinter as ctk

from GuiFramework.widgets.custom_context_menu import CustomContextMenu


class CustomConsoleTextbox(ctk.CTkTextbox):
    def __init__(self, master, autoscroll=True, max_lines=1000, **kwargs):
        if 'font' in kwargs:
            font = kwargs['font']
            if isinstance(font, list):
                kwargs['font'] = tuple(font)
        super().__init__(master, **kwargs)
        self.master = master
        self.autoscroll = autoscroll
        self.max_lines = max_lines
        self.configure(state='disabled')
        self.context_menu = None
        self._create_context_menu()

    def write_console(self, text):
        self.configure(state='normal')
        self.insert('end', text)
        self._limit_text_length()
        if self.autoscroll:
            self.see('end')
        self.configure(state='disabled')
        self.update_idletasks()

    def clear_console(self):
        self.configure(state='normal')
        self.delete("1.0", 'end')
        self.configure(state='disabled')

    def _create_context_menu(self):
        menu_items = [
            {"text": "Clear", "command": self._on_clear},
            {"text": "Copy", "command": self._on_copy},
            {"text": "Select All", "command": self._on_select_all},
        ]
        self.bind("<Button-3>", lambda event: self._show_context_menu(event, menu_items))

    def _show_context_menu(self, event, menu_items):
        if self.context_menu and self.context_menu.winfo_exists():
            self.context_menu.destroy()
        self.context_menu = CustomContextMenu(self, menu_items)
        self.context_menu.show(event.x_root, event.y_root)

    def _on_copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.selection_get())

    def _on_clear(self):
        self.clear_text()

    def _on_select_all(self):
        self.tag_add("sel", "1.0", "end")

    def _limit_text_length(self):
        lines = int(self.index('end-1c').split('.')[0])
        if lines > self.max_lines:
            self.delete('1.0', f'{lines - self.max_lines + 1}.0')