# test_window.py / GuiFramework

# Make sure to have customtkinter installed: pip install customtkinter
# window.py / GuiFramework

import customtkinter as ctk

from GuiFramework.gui.window import Window
from GuiFramework.gui.window import WindowState


class SampleApp:
    def __init__(self):
        self.window = Window(lazy_init=True)
        # self.window = Window(window_title="Sample Window 22", window_icon="GuiFramework\\resources\\icon.ico",
        #                     window_size=(1920, 1080), window_position=(0, 0), window_state=WindowState.FULLSCREEN_BORDERLESS,
        #                     ui_theme="dark", resizeable=True, use_high_dpi=True, centered=True)
        self.window.apply_configuration(window_title="Sample Window 22", window_icon="GuiFramework\\resources\\icon.ico",
                                        window_size=(1920, 1080), window_position=(0, 0), window_state=WindowState.NORMAL,
                                        ui_theme="dark", resizeable=True, use_high_dpi=True, centered=True)
        self._setup_ui()

    def _setup_ui(self):
        # Button to enable fullscreen
        self.btn_fullscreen = ctk.CTkButton(self.window, text="Fullscreen", command=lambda: self.window.set_window_state(WindowState.FULLSCREEN))
        self.btn_fullscreen.pack(pady=10)

        # Button to enable fullscreen borderless mode
        self.btn_borderless = ctk.CTkButton(self.window, text="Fullscreen Borderless", command=lambda: self.window.set_window_state(WindowState.FULLSCREEN_BORDERLESS))
        self.btn_borderless.pack(pady=10)

        # Button to enable borderless mode
        self.btn_borderless = ctk.CTkButton(self.window, text="Borderless", command=lambda: self.window.set_window_state(WindowState.BORDERLESS))
        self.btn_borderless.pack(pady=10)

        # Button to maximize window
        self.btn_maximize = ctk.CTkButton(self.window, text="Maximize", command=lambda: self.window.set_window_state(WindowState.MAXIMIZED))
        self.btn_maximize.pack(pady=10)

        # Button to restore to normal
        self.btn_normal = ctk.CTkButton(self.window, text="Normal", command=lambda: self.window.set_window_state(WindowState.NORMAL))
        self.btn_normal.pack(pady=10)

        # Button set appearance mode to dark
        self.btn_dark = ctk.CTkButton(self.window, text="Dark", command=lambda: ctk.set_appearance_mode("dark"))
        self.btn_dark.pack(pady=10)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    try:
        app = SampleApp()
        app.run()
    except Exception as e:
        print(e)
        input("Press Enter to continue...")