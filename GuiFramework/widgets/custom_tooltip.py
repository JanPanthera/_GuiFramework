# GuiFramework/widgets/custom_tooltip.py

import customtkinter as ctk

from typing import Optional, Tuple
from GuiFramework.utilities.utils import Utils


class CustomTooltip:
    DEFAULT_FONT = ("Arial", 14)
    DEFAULT_BG_COLOR = "#FFFFE0"
    DEFAULT_TEXT_COLOR = "#000000"
    DEFAULT_SHOW_DELAY = 200
    DEFAULT_HIDE_DELAY = 200
    DEFAULT_TEXT_WRAP_LENGTH = 300
    DEFAULT_CURSOR_X_OFFSET = 20
    DEFAULT_CURSOR_Y_OFFSET = 10

    def __init__(self, widget, text: str, show_delay: int = DEFAULT_SHOW_DELAY, hide_delay: int = DEFAULT_HIDE_DELAY,
                 bg_color: str = DEFAULT_BG_COLOR, text_color: str = DEFAULT_TEXT_COLOR, text_wrap_length: int = DEFAULT_TEXT_WRAP_LENGTH,
                 font: Tuple[str, int] = DEFAULT_FONT, cursor_x_offset: int = DEFAULT_CURSOR_X_OFFSET, cursor_y_offset: int = DEFAULT_CURSOR_Y_OFFSET
                 ):
        """Initialize a CustomTooltip instance."""
        self.widget = widget
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.x_offset = cursor_x_offset
        self.y_offset = cursor_y_offset
        self.show_delay = show_delay
        self.hide_delay = hide_delay
        self.text_wrap_length = text_wrap_length

        self.tooltip_window = None
        self.show_id = None
        self.hide_id = None
        self.is_mouse_on_widget = False
        self.is_mouse_on_tooltip = False

        self.widget.bind("<Enter>", self._on_mouse_enter)
        self.widget.bind("<Leave>", self._on_mouse_leave)

    def set_text(self, text: str) -> None:
        """Set the text of the tooltip."""
        self.text = text

    def set_font(self, font: Tuple[str, int]) -> None:
        """Set the font of the tooltip."""
        self.font = font

    def set_bg_color(self, color: str) -> None:
        """Set the background color of the tooltip."""
        self.bg_color = color

    def set_text_color(self, color: str) -> None:
        """Set the text color of the tooltip."""
        self.text_color = color

    def _display_tooltip(self, event=None) -> None:
        """Display the tooltip with adjusted position."""
        if self.tooltip_window:
            return

        x, y = event.x_root + self.x_offset, event.y_root + self.y_offset

        self.tooltip_window = ctk.CTkToplevel(self.widget, fg_color=self.bg_color)
        self.tooltip_window.wm_overrideredirect(True)

        label = ctk.CTkLabel(self.tooltip_window, text=self.text, corner_radius=10, wraplength=self.text_wrap_length,
                             fg_color=self.bg_color, text_color=self.text_color, font=self.font)
        label.pack()

        self.tooltip_window.update_idletasks()
        width, height = label.winfo_reqwidth(), label.winfo_reqheight()

        x, y = self._adjust_position(x, y, width, height)

        self.tooltip_window.wm_geometry(f"{width}x{height}+{x}+{y}")

        self.tooltip_window.bind("<Enter>", self._on_tooltip_enter)
        self.tooltip_window.bind("<Leave>", self._on_mouse_leave)

    def _adjust_position(self, x: int, y: int, width: int, height: int) -> Tuple[int, int]:
        """Adjust the tooltip's position to ensure it stays on-screen."""
        dpi_scaling = Utils.get_dpi_scaling_factor()
        screen_width = self.widget.winfo_screenwidth() * dpi_scaling
        screen_height = self.widget.winfo_screenheight() * dpi_scaling

        if x + width > screen_width:
            x = screen_width - width
        if y + height > screen_height:
            y = screen_height - height

        return x, y

    def _remove_tooltip(self) -> None:
        """Remove the tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def _on_tooltip_enter(self, event=None) -> None:
        """Handle mouse entering the tooltip."""
        self.is_mouse_on_tooltip = True

    def _on_mouse_enter(self, event=None) -> None:
        """Schedule the tooltip to be displayed."""
        self._cancel_scheduled_events()
        self.is_mouse_on_widget = True
        self.show_id = self.widget.after(self.show_delay, self._display_tooltip, event)

    def _on_mouse_leave(self, event=None) -> None:
        """Schedule the tooltip to be removed."""
        self._cancel_scheduled_events()
        self.is_mouse_on_widget = False
        self.is_mouse_on_tooltip = False
        self.hide_id = self.widget.after(self.hide_delay, self._remove_tooltip)

    def _cancel_scheduled_events(self) -> None:
        """Cancel any scheduled show or hide events."""
        if self.show_id:
            self.widget.after_cancel(self.show_id)
            self.show_id = None
        if self.hide_id:
            self.widget.after_cancel(self.hide_id)
            self.hide_id = None
