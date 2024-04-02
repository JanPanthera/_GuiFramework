# GuiFramework/widgets/custom_popup_message_box.py

import customtkinter as ctk


class CustomPopupMessageBox(ctk.CTkToplevel):
    def __init__(self, main_window, title="Popup", message="Your message here",
                 message_font=("Arial", 18), button_font=("Arial", 18, "bold"),
                 buttons=None, show_entry=False, entry_placeholder="Enter text here...",
                 entry_font=("Arial", 18), *args, **kwargs):
        super().__init__(master=main_window, *args, **kwargs)
        self.title(title)
        self.resizable(False, False)

        self.attributes("-alpha", 0)
        self.attributes("-toolwindow", True)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_message = ctk.CTkLabel(self.frame, text=message, wraplength=250, font=message_font)
        self.label_message.pack(pady=10, padx=10)

        self.entry = None
        if show_entry:
            self.entry = ctk.CTkEntry(self.frame, placeholder_text=entry_placeholder, font=entry_font)
            self.entry.pack(pady=10, padx=10)

        self.buttons = buttons
        for button in self.buttons:
            btn = ctk.CTkButton(self.frame, text=button["text"], command=lambda b=button: self.handle_button_press(b["callback"]), font=button_font)
            btn.pack(pady=10, padx=10, side="left", expand=True)

        self.after(100, self.position_center_main_window)
        self.after(200, self.attributes, "-alpha", 1)
        self.grab_set()

    def position_center_main_window(self):
        title_bar_height = int(self.winfo_rooty() - self.winfo_y())
        main_window_center_x = self.master.winfo_rootx() + self.master.winfo_width() // 2
        main_window_center_y = self.master.winfo_rooty() + self.master.winfo_height() // 2
        popup_x = main_window_center_x - self.winfo_width() // 2
        popup_y = main_window_center_y - self.winfo_height() // 2 - title_bar_height // 2
        self.geometry(f"+{popup_x}+{popup_y}")

    def handle_button_press(self, callback):
        if callback:
            callback()
        self.destroy()

    def get_entry_text(self):
        return self.entry.get()
