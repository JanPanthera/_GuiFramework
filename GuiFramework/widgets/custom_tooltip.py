# GuiFramework/widgets/custom_tooltip.py

import customtkinter as ctk


class CustomTooltip:
    def __init__(self, widget, text, delay=200):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.mouse_on_widget = False
        self.mouse_on_tooltip = False
        self.delay = delay
        self.show_id = None
        self.hide_id = None

        self.widget.bind("<Enter>", self.schedule_show_tooltip)
        self.widget.bind("<Leave>", self.schedule_hide_tooltip)

    def schedule_show_tooltip(self, event=None):
        self.cancel_scheduled_events()
        self.mouse_on_widget = True
        self.show_id = self.widget.after(self.delay, self.show_tooltip, event)

    def show_tooltip(self, event=None):
        if self.tooltip_window is not None:
            return

        x = event.x_root + 20
        y = event.y_root + 10

        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)

        label = ctk.CTkLabel(self.tooltip_window, text=self.text, corner_radius=10)
        label.pack(fill="none", expand=False)

        self.tooltip_window.update_idletasks()
        width = label.winfo_reqwidth()
        height = label.winfo_reqheight()

        self.tooltip_window.wm_geometry(f"{width}x{height}+{x}+{y}")

        self.tooltip_window.bind("<Enter>", self.enter_tooltip)
        self.tooltip_window.bind("<Leave>", self.schedule_hide_tooltip)

    def enter_tooltip(self, event=None):
        self.mouse_on_tooltip = True

    def schedule_hide_tooltip(self, event=None):
        self.cancel_scheduled_events()
        self.mouse_on_widget = False
        self.mouse_on_tooltip = False
        self.hide_id = self.widget.after(self.delay, self.hide_tooltip)

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def cancel_scheduled_events(self):
        if self.show_id:
            self.widget.after_cancel(self.show_id)
        if self.hide_id:
            self.widget.after_cancel(self.hide_id)
        self.show_id = None
        self.hide_id = None
