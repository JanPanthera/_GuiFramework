# GuiFramework/widgets/custom_context_menu.py

import customtkinter as ctk
from functools import partial


class CustomContextMenu(ctk.CTkToplevel):
    def __init__(self, parent, menu_items, **kwargs):
        super().__init__(parent, **kwargs)

        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Keep the menu on top

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack()

        for item in menu_items:
            text, command = item.get("text"), item.get("command")
            button = ctk.CTkButton(self.menu_frame, text=text, command=partial(self.on_menu_select, command), corner_radius=0)
            button.pack(fill="x")

        self.bind("<FocusOut>", self.on_focus_out)

    def on_menu_select(self, command):
        try:
            command()
        except Exception as e:
            print(f"Error executing menu command: {e}")
        finally:
            self.after(200, self.destroy)

    def on_focus_out(self, event):
        # Add a slight delay to prevent immediate dismissal in case of rapid focus changes
        self.after(100, self.destroy)

    def show(self, x, y):
        offset_x, offset_y = 10, 10
        adjusted_x, adjusted_y = x + offset_x, y + offset_y
        self.geometry(f"+{adjusted_x}+{adjusted_y}")
        self.deiconify()
        self.after(100, self.focus_set)  # Delay focus setting to ensure menu visibility
        # self.after(100, self.grab_set)  # Set the input focus to the menu window after a slight delay
