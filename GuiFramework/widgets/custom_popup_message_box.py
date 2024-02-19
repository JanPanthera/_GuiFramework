# custom_popup_message_box.py

from turtle import width
import customtkinter as ctk


class CustomPopupMessageBox(ctk.CTkToplevel):
    def __init__(self, main_window, title="Popup", message="Your message here",
                 close_button_text="Close", message_font=("Helvetica", 18), button_font=("Helvetica", 18, "bold"),
                 interactive=False, yes_button_text="Yes", no_button_text="No", on_yes=None, on_no=None, *args, **kwargs):
        super().__init__(master=main_window, *args, **kwargs)
        self.position_center_main_window()

        self.title(title)
        self.overrideredirect(True)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_message = ctk.CTkLabel(self.frame, text=message, wraplength=250, font=message_font)
        self.label_message.pack(pady=10, padx=10)
        # Check if the message box is interactive (Yes/No options) or just a simple message box
        if interactive:
            self.button_yes = ctk.CTkButton(self.frame, text=yes_button_text, command=lambda: self.handle_response(True, on_yes), font=button_font)
            self.button_yes.pack(side="left", pady=10, padx=10)

            self.button_no = ctk.CTkButton(self.frame, text=no_button_text, command=lambda: self.handle_response(False, on_no), font=button_font)
            self.button_no.pack(side="right", pady=10, padx=10)
        else:
            self.button_close = ctk.CTkButton(self.frame, text=close_button_text, command=self.close_popup, font=button_font)
            self.button_close.pack(pady=10)

        self.after(1, self.position_center_main_window)

        # Needed to prevent the main window from being interacted with
        self.grab_set()

    def position_center_main_window(self):
        self.update_idletasks()
        x = self.master.winfo_rootx() + self.master.winfo_width() // 2 - self.winfo_width() // 2
        y = self.master.winfo_rooty() + self.master.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")

    def close_popup(self):
        self.destroy()

    def handle_response(self, is_yes, callback):
        if callback:
            callback(is_yes)
        self.close_popup()
