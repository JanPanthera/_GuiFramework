# helper_ctk.py

import customtkinter as ctk


def update_widget_text(widget, text):
    if isinstance(widget, ctk.CTkLabel):
        widget.configure(text=text)
    elif isinstance(widget, ctk.CTkButton):
        widget.configure(text=text)
    elif isinstance(widget, ctk.CTkCheckBox):
        widget.configure(text=text)
    else:
        # raise ValueError(f"Unsupported widget type: {type(widget)}")
        pass