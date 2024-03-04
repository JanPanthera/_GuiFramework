# window.py / GuiFramework

import customtkinter as ctk
from enum import Enum, auto
from GuiFramework.utilities import get_dpi_scaling_factor
from GuiFramework.utilities.utils import Debouncer, setup_default_logger


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
    UI_COLOR_THEME = "ui_color_theme"  # library themse are green, blue, dark-blue
    RESIZEABLE = "resizeable"
    USE_HIGH_DPI = "use_high_dpi"
    CENTERED = "centered"
    ON_CLOSE_CALLBACK = "on_close_callback"
    LAZY_INIT = "lazy_init"


class Window(ctk.CTk):
    # Initialization and Configuration
    def __init__(self, logger=None, **kwargs):
        super().__init__()
        self.attributes('-alpha', 0)
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
        self.logger = logger or setup_default_logger()
        self.configs = {**self.WINDOW_SETTINGS, **kwargs}
        self.initialized = False
        self._setup_window()
        self.after(1000, self.attributes, '-alpha', 1)

    def _setup_window(self):
        self.hide()
        self.window_size = self.configs[WindowSettings.WINDOW_SIZE]
        self.window_position = self.configs[WindowSettings.WINDOW_POSITION]
        self.window_size_before_fullscreen = self.window_size
        self.window_position_before_fullscreen = self.window_position
        self.high_dpi_scale = get_dpi_scaling_factor()
        self.resize_debouncer = Debouncer(delay=0.1)
        self.move_debouncer = Debouncer(delay=0.1)
        self._on_window_resize_debounced = self.resize_debouncer(self._on_window_resize)
        self._on_window_move_debounced = self.move_debouncer(self._on_window_move)
        self.on_window_close_callback = None
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)
        self.bind("<Configure>", self._on_configure)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        if not self.configs[WindowSettings.LAZY_INIT]:
            self.apply_configuration()

    def apply_configuration(self, **kwargs):
        self.configs.update(kwargs)
        try:
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
        except Exception as e:
            self.logger.error(f"Error applying settings: {e}")
        self.initialized = True
        self.logger.info("Window configuration applied.")

    # UI Adjustment Methods
    def show(self):
        if not self.initialized:
            self.apply_configuration()
        self.deiconify()
        self.logger.info("Window shown.")

    def hide(self):
        self.withdraw()
        self.logger.info("Window hidden.")

    def set_window_title(self, title):
        try:
            self.title(title)
            self.logger.info(f"Window title set to '{title}'.")
        except Exception as e:
            self.logger.error(f"Failed to set window title to '{title}': {e}")

    def set_window_icon(self, icon_path):
        if icon_path is None:
            self.logger.warning("No icon path provided, skipping setting window icon.")
            return
        try:
            self.iconbitmap(icon_path)
            self.logger.info(f"Window icon set to {icon_path}")
        except Exception as e:
            self.logger.error(f"Failed to set window icon from {icon_path}: {e}")

    def set_window_size(self, size):
        try:
            self.window_size = size
            width = int(size[0] // get_dpi_scaling_factor())
            height = int(size[1] // get_dpi_scaling_factor())
            pos_x, pos_y = self.window_position
            self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
            self.update()
            self.logger.info(f"Window size set to {self.window_size}.")
        except ValueError:
            self.logger.error(f"Invalid window size values: size={size}. Must be integers.")
        except Exception as e:
            self.logger.error(f"Failed to set window size to {size}: {e}")

    def set_window_position(self, position):
        try:
            width, height = self.window_size
            width = int(width // get_dpi_scaling_factor())
            height = int(height // get_dpi_scaling_factor())
            pos_x, pos_y = max(int(position[0]), 0), max(int(position[1]), 0)
            self.window_position = (pos_x, pos_y)
            self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
            self.update()
            self.logger.info(f"Window position set to {self.window_position}.")
        except ValueError:
            self.logger.error(f"Invalid window position values: position={position}. Must be integers.")
        except Exception as e:
            self.logger.error(f"Failed to set window position to {position}: {e}")

    def set_window_geometry(self, size, position):
        try:
            self.window_size = size
            self.window_position = position
            width = int(size[0] // get_dpi_scaling_factor())
            height = int(size[1] // get_dpi_scaling_factor())
            pos_x, pos_y = max(int(position[0]), 0), max(int(position[1]), 0)
            self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
            self.update()
            self.logger.info(f"Window geometry set to {self.window_size}+{self.window_position}.")
        except ValueError:
            self.logger.error(f"Invalid window geometry values: size={size}, position={position}. Must be integers.")
        except Exception as e:
            self.logger.error(f"Failed to set window geometry to {size}+{position}: {e}")

    def center_window(self):
        if not self.winfo_ismapped():
            self.deiconify()
        self.update_idletasks()
        high_dpi_scale = get_dpi_scaling_factor()
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
                self.logger.error(f"Unhandled window state: {state}")
        except Exception as e:
            self.logger.error(f"Failed to set window state: {e}")

    def _enable_fullscreen(self):
        self.window_size_before_fullscreen = self.window_size
        self.window_position_before_fullscreen = self.window_position
        self.state('zoomed')
        self.attributes('-fullscreen', True)
        self.update()
        self.logger.info("Fullscreen mode enabled.")

    def _enable_fullscreen_borderless(self):
        self.window_size_before_fullscreen = self.window_size
        self.window_position_before_fullscreen = self.window_position
        self.state('zoomed')
        self.overrideredirect(True)
        self.update()
        self.logger.info("Borderless fullscreen mode enabled.")

    def _enable_borderless(self):
        self.overrideredirect(True)
        self.update()
        self.logger.info("Borderless mode enabled.")

    def _maximize_window(self):
        self.state('zoomed')
        self.update()
        self.logger.info("Maximized mode enabled.")

    def _restore_normal(self):
        was_fullscreen = self.attributes('-fullscreen')
        self.state('normal')
        self.overrideredirect(False)
        self._windows_set_titlebar_color(self._get_appearance_mode())
        if was_fullscreen:
            self.attributes('-fullscreen', False)
        self.set_window_geometry(self.window_size_before_fullscreen, self.window_position_before_fullscreen)
        self.update()
        self.logger.info("Window restored to normal mode.")

    def set_window_transparency(self, transparency):
        try:
            if not 0.0 <= transparency <= 1.0:
                raise ValueError("Transparency value must be between 0.0 and 1.0.")
            self.attributes('-alpha', transparency)
            self.logger.info(f"Window transparency set to {transparency}.")
        except ValueError as ve:
            self.logger.error(ve)
        except Exception as e:
            self.logger.error(f"Failed to set window transparency: {e}")

    def set_always_on_top(self, always_on_top):
        try:
            self.attributes('-topmost', always_on_top)
            state = 'enabled' if always_on_top else 'disabled'
            self.logger.info(f"Always-on-top mode {state}.")
        except Exception as e:
            self.logger.error(f"Failed to set always-on-top mode: {e}")

    def set_ui_theme(self, theme):
        try:
            ctk.set_appearance_mode(theme)
            self.logger.info(f"UI theme set to {theme}.")
        except Exception as e:
            self.logger.error(f"Failed to set UI theme to {theme}: {e}")
            self.set_ui_theme("system")

    def set_ui_color_theme(self, color_theme):
        try:
            ctk.set_default_color_theme(color_theme)
            self.logger.info(f"UI color theme set to {color_theme}.")
        except Exception as e:
            self.logger.error(f"Failed to set UI color theme to {color_theme}: {e}")
            self.set_ui_color_theme("blue")

    def set_window_resizeable(self, resizeable):
        try:
            self.resizable(resizeable, resizeable)
            state = 'enabled' if resizeable else 'disabled'
            self.logger.info(f"Window resizeability {state}.")
        except Exception as e:
            self.logger.error(f"Failed to change window resizeability to {resizeable}: {e}")

    def set_high_dpi(self, enable):
        if enable:
            if hasattr(ctk, 'activate_automatic_dpi_awareness'):
                ctk.activate_automatic_dpi_awareness()
                self.high_dpi_scale = get_dpi_scaling_factor()
                self.logger.info(f"High DPI mode activated. Scale: {self.high_dpi_scale}")
            else:
                self.logger.error("Reactivating Automatic DPI awareness is not supported on this customtkinter repository.")
        else:
            ctk.deactivate_automatic_dpi_awareness()
            self.high_dpi_scale = 1.0
            self.update()
            self.logger.info(f"High DPI mode deactivated.")

    # Event Callback and Handling
    def set_window_event_callback(self, callback):
        try:
            if not callable(callback):
                raise ValueError("Provided callback is not callable.")
            self.on_window_close_callback = callback
            self.logger.info("Window event callback set successfully.")
        except ValueError as ve:
            self.logger.error(ve)
        except Exception as e:
            self.logger.error(f"Failed to set window event callback: {e}")

    def _on_configure(self, event):
        if self.initialized:
            try:
                self._on_window_resize_debounced()
                self._on_window_move_debounced()
            except Exception as e:
                self.logger.error(f"Error handling window configuration change: {e}")

    def _on_window_resize(self):
        try:
            if self.window_size != (self.winfo_width(), self.winfo_height()):
                self.window_size = (self.winfo_width(), self.winfo_height())
                self.logger.info(f"Window resized to {self.window_size}")
        except Exception as e:
            self.logger.error(f"Error handling window resize: {e}")

    def _on_window_move(self):
        try:
            if self.window_position != (self.winfo_x(), self.winfo_y()):
                self.window_position = (self.winfo_x(), self.winfo_y())
                self.logger.info(f"Window moved to {self.window_position}")
        except Exception as e:
            self.logger.error(f"Error handling window move: {e}")

    def _on_focus_in(self, event):
        self.logger.info("Window gained focus.")

    def _on_focus_out(self, event):
        self.logger.info("Window lost focus.")

    def _on_window_close(self):
        if self.on_window_close_callback:
            self.on_window_close_callback()
        self.destroy()
        self.logger.info("Window closed.")

    # Utility and Helper Methods
    def get_size(self):
        return self.window_size

    def get_position(self):
        return self.window_position
