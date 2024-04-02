# GuiFramework/gui/window.py

import customtkinter as ctk

from enum import Enum, auto

from GuiFramework.utilities.logging import Logger
from GuiFramework.utilities.utils import Debouncer, Utils


class WindowState(Enum):
    FULLSCREEN = auto()
    FULLSCREEN_BORDERLESS = auto()
    BORDERLESS = auto()
    MAXIMIZED = auto()
    NORMAL = auto()


class WindowSettings:
    WINDOW_TITLE = "window_title"
    WINDOW_ICON = "window_icon"
    WINDOW_SIZE = "window_size"
    WINDOW_POSITION = "window_position"
    WINDOW_STATE = "window_state"
    UI_THEME = "ui_theme"
    UI_COLOR_THEME = "ui_color_theme"  # library default themes are green, blue, dark-blue
    RESIZEABLE = "resizeable"
    USE_HIGH_DPI = "use_high_dpi"
    CENTERED = "centered"
    ON_CLOSE_CALLBACK = "on_close_callback"
    LAZY_INIT = "lazy_init"


class Window(ctk.CTk):
    # Initialization and Configuration

    def __init__(self, **kwargs):
        super().__init__()
        self.logger = Logger.get_logger("GuiFramework")
        self.attributes("-alpha", 0)
        self.WINDOW_SETTINGS = {
            "window_title": "No Title Provided",
            "window_icon": None,
            "window_size": (1366, 768),
            "window_position": (0, 0),
            "window_state": WindowState.NORMAL,
            "ui_theme": "system",
            "ui_color_theme": "blue",
            "resizeable": True,
            "use_high_dpi": True,
            "centered": True,
            "on_close_callback": None,
            "lazy_init": False
        }
        self.configs = {**self.WINDOW_SETTINGS, **kwargs}
        self.initialized = False
        self._setup_window()
        self.after(1000, self.attributes, "-alpha", 1)

    def _setup_window(self):
        self.hide()
        self.window_size = self.configs[WindowSettings.WINDOW_SIZE]
        self.window_position = self.configs[WindowSettings.WINDOW_POSITION]
        self.window_size_before_fullscreen = self.window_size
        self.window_position_before_fullscreen = self.window_position
        self.high_dpi_scale = Utils.get_dpi_scaling_factor()
        
        self._on_window_resize_id = None
        self._on_window_move_id = None
        
        self.on_window_close_callback = None
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)
        self.bind("<Configure>", self._on_configure)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        if not self.configs[WindowSettings.LAZY_INIT]:
            self.apply_configuration()

    def apply_configuration(self, **kwargs):
        self.configs.update(kwargs)
        if self.configs[WindowSettings.WINDOW_TITLE] is not None:
            self.set_window_title(self.configs[WindowSettings.WINDOW_TITLE])
        if self.configs[WindowSettings.WINDOW_ICON] is not None:
            self.set_window_icon(self.configs[WindowSettings.WINDOW_ICON])
        if self.configs[WindowSettings.UI_THEME] is not None:
            self.set_ui_theme(self.configs[WindowSettings.UI_THEME])
        if self.configs[WindowSettings.UI_COLOR_THEME] is not None:
            self.set_ui_color_theme(self.configs[WindowSettings.UI_COLOR_THEME])
        if self.configs[WindowSettings.USE_HIGH_DPI] is not None:
            self.set_high_dpi(self.configs[WindowSettings.USE_HIGH_DPI])
        if self.configs[WindowSettings.WINDOW_STATE] is not None:
            self.set_window_state(self.configs[WindowSettings.WINDOW_STATE])
        if self.configs[WindowSettings.RESIZEABLE] is not None:
            self.set_window_resizeable(self.configs[WindowSettings.RESIZEABLE])
        if self.configs[WindowSettings.ON_CLOSE_CALLBACK] is not None:
            self.set_window_event_callback(self.configs[WindowSettings.ON_CLOSE_CALLBACK])
        if self.configs[WindowSettings.WINDOW_POSITION] is not None:
            self.set_window_position(self.configs[WindowSettings.WINDOW_POSITION])
        if self.configs[WindowSettings.WINDOW_SIZE] is not None:
            self.set_window_size(self.configs[WindowSettings.WINDOW_SIZE])
        if self.configs[WindowSettings.CENTERED]:
            self.center_window()
        self.initialized = True

    # UI Adjustment Methods
    def show(self):
        if not self.initialized:
            self.apply_configuration()
        self.deiconify()

    def hide(self):
        self.withdraw()

    def set_window_title(self, title):
        self.title(title)

    def set_window_icon(self, icon_path):
        if icon_path is None:
            self.logger.log_warning("No icon path provided, skipping setting window icon.", "Window")
            return
        self.iconbitmap(icon_path)

    def set_window_size(self, size):
        self.window_size = size
        width = int(size[0] // Utils.get_dpi_scaling_factor())
        height = int(size[1] // Utils.get_dpi_scaling_factor())
        pos_x, pos_y = self.window_position
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.update()

    def set_window_position(self, position):
        width, height = self.window_size
        width = int(width // Utils.get_dpi_scaling_factor())
        height = int(height // Utils.get_dpi_scaling_factor())
        pos_x, pos_y = max(int(position[0]), 0), max(int(position[1]), 0)
        self.window_position = (pos_x, pos_y)
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.update()

    def set_window_geometry(self, size, position):
        self.window_size = size
        self.window_position = position
        width = int(size[0] // Utils.get_dpi_scaling_factor())
        height = int(size[1] // Utils.get_dpi_scaling_factor())
        pos_x, pos_y = max(int(position[0]), 0), max(int(position[1]), 0)
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.update()

    def center_window(self):
        if not self.winfo_ismapped():
            self.deiconify()
        self.update_idletasks()
        high_dpi_scale = Utils.get_dpi_scaling_factor()
        screen_width = int(self.winfo_screenwidth() * high_dpi_scale)
        screen_height = int(self.winfo_screenheight() * high_dpi_scale)
        titlebar_height = int(self.winfo_rooty() - self.winfo_y())
        window_width, window_height = self.window_size
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height - titlebar_height) // 2
        self.set_window_position((pos_x, pos_y))

    def set_window_state(self, state: WindowState):
        try:
            if state == WindowState.FULLSCREEN:
                self._enable_fullscreen()
            elif state == WindowState.FULLSCREEN_BORDERLESS:
                self._enable_fullscreen_borderless()
            elif state == WindowState.BORDERLESS:
                self._enable_borderless()
            elif state == WindowState.MAXIMIZED:
                self._maximize_window()
            elif state == WindowState.NORMAL:
                self._restore_normal()
            else:
                self.logger.log_error(f"Unhandled window state: {state}", "Window")
        except Exception as e:
            self.logger.log_error(f"Failed to set window state: {e}", "Window")

    def _enable_fullscreen(self):
        self.window_size_before_fullscreen = self.window_size
        self.window_position_before_fullscreen = self.window_position
        self.state("zoomed")
        self.attributes("-fullscreen", True)
        self.update()

    def _enable_fullscreen_borderless(self):
        self.window_size_before_fullscreen = self.window_size
        self.window_position_before_fullscreen = self.window_position
        self.state("zoomed")
        self.overrideredirect(True)
        self.update()

    def _enable_borderless(self):
        self.overrideredirect(True)
        self.update()

    def _maximize_window(self):
        self.state("zoomed")
        self.update()

    def _restore_normal(self):
        was_fullscreen = self.attributes("-fullscreen")
        self.state("normal")
        self.overrideredirect(False)
        self._windows_set_titlebar_color(self._get_appearance_mode())
        if was_fullscreen:
            self.attributes("-fullscreen", False)
        self.set_window_geometry(self.window_size_before_fullscreen, self.window_position_before_fullscreen)
        self.update()

    def set_window_transparency(self, transparency):
        if not 0.0 <= transparency <= 1.0:
            raise ValueError("Transparency value must be between 0.0 and 1.0.")
        self.attributes("-alpha", transparency)

    def set_always_on_top(self, always_on_top):
        self.attributes("-topmost", always_on_top)
        state = "enabled" if always_on_top else "disabled"

    def set_ui_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def set_ui_color_theme(self, color_theme):
        ctk.set_default_color_theme(color_theme)

    def set_window_resizeable(self, resizeable):
        self.resizable(resizeable, resizeable)
        state = "enabled" if resizeable else "disabled"

    def set_high_dpi(self, enable):
        if enable:
            if hasattr(ctk, "activate_automatic_dpi_awareness"):
                ctk.activate_automatic_dpi_awareness()
                self.high_dpi_scale = Utils.get_dpi_scaling_factor()
            else:
                self.logger.log_warning("Reactivating Automatic DPI awareness is not supported on this customtkinter repository.", "Window")
        else:
            ctk.deactivate_automatic_dpi_awareness()
            self.high_dpi_scale = 1.0
            self.update()

    # Event Callback and Handling
    def set_window_event_callback(self, callback):
        if not callable(callback):
            raise ValueError("Provided callback is not callable.")
        self.on_window_close_callback = callback

    def _on_configure(self, event):
        if self.initialized:
            # If there's already a call to _on_window_resize scheduled, cancel it
            if self._on_window_resize_id is not None:
                self.after_cancel(self._on_window_resize_id)
    
            # Schedule _on_window_resize to be run after a delay
            self._on_window_resize_id = self.after(100, self._on_window_resize)
    
            # Do the same for _on_window_move
            if self._on_window_move_id is not None:
                self.after_cancel(self._on_window_move_id)
    
            self._on_window_move_id = self.after(100, self._on_window_move)

    def _on_window_resize(self):
        if self.window_size != (self.winfo_width(), self.winfo_height()):
            self.window_size = (self.winfo_width(), self.winfo_height())

    def _on_window_move(self):
        if self.window_position != (self.winfo_x(), self.winfo_y()):
            self.window_position = (self.winfo_x(), self.winfo_y())

    def _on_focus_in(self, event):
        pass

    def _on_focus_out(self, event):
        pass

    def _on_window_close(self):
        if self.on_window_close_callback:
            self.on_window_close_callback()
        self.destroy()

    # Utility and Helper Methods
    def get_size(self):
        return self.window_size

    def get_position(self):
        return self.window_position
