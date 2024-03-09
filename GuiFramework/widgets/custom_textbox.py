# GuiFramework/widgets/custom_textbox.py

import customtkinter as ctk

from GuiFramework.widgets.custom_context_menu import CustomContextMenu


class CustomTextbox(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.context_menu = None  # Reference to the open context menu
        self.menu_items = []  # Will hold the menu items with their labels and commands
        self.create_context_menu()

    def create_context_menu(self):
        self.menu_items = [
            {"text": "Copy", "command": self.copy_selection},
            {"text": "Paste", "command": self.paste},
            {"text": "Cut", "command": self.cut},
            {"text": "Clear", "command": self.clear_text},
            {"text": "Select All", "command": self.select_all},
        ]
        self.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        if self.context_menu and self.context_menu.winfo_exists():
            self.context_menu.destroy()  # Explicitly destroy the existing menu
        self.context_menu = CustomContextMenu(self, self.menu_items)
        self.context_menu.show(event.x_root, event.y_root)

    def refresh_context_menu_translations(self):
        self.menu_items = [
            {"text": self.loc("Copy"), "command": self.copy_selection},
            {"text": self.loc("Paste"), "command": self.paste},
            {"text": self.loc("Cut"), "command": self.cut},
            {"text": self.loc("Clear"), "command": self.clear_text},
            {"text": self.loc("Select All"), "command": self.select_all},
        ]

    def copy_selection(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.selection_get())
        except Exception as e:
            print(f"Error copying text: {e}")

    def paste(self):
        if self.selection_present():
            self.delete("sel.first", "sel.last")
        try:
            text_to_paste = self.clipboard_get()
            self.insert("insert", text_to_paste)
        except Exception as e:
            print(f"Error pasting text: {e}")

    def cut(self):
        self.copy_selection()
        self.delete("sel.first", "sel.last")

    def clear_text(self):
        self.delete("1.0", "end")

    def select_all(self):
        self.tag_add("sel", "1.0", "end")

    def selection_present(self):
        """Check if there is any text selected."""
        return bool(self._textbox.tag_ranges("sel"))

    def is_empty(self):
        return not bool(self.get("1.0", "end-1c"))