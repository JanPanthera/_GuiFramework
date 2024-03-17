# GuiFramework/core/window.py

import glfw
import OpenGL.GL as gl

from GuiFramework.core.constants import FRAMEWORK_NAME
from GuiFramework.mixins import EventMixin
from GuiFramework.utilities.logging import Logger


class Window(EventMixin):

    def __init__(self, title="Window", width=800, height=600):
        self.logger = Logger(FRAMEWORK_NAME)

        EventMixin.__init__(self)

        if not glfw.init():
            self.logger.log_error("Failed to initialize GLFW", "Window")
            raise Exception("Failed to initialize GLFW")

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            self.logger.log_error("Failed to create GLFW window", "Window")
            raise Exception("Failed to create GLFW window")

        glfw.make_context_current(self.window)
        self.setup_event_callbacks()

        self.frame_count = 0
        self.last_time = glfw.get_time()

    # Application-specific methods
    def update(self):
        # self.frame_count += 1
        # current_time = glfw.get_time()
        # if current_time - self.last_time >= 1.0:  # if one second has passed
        #     fps = self.frame_count / (current_time - self.last_time)
        #     glfw.set_window_title(self.window, f"Window - {fps:.2f}")
        #     self.frame_count = 0
        #     self.last_time = current_time
        pass

    def render(self):
        gl.glClearColor(0.529, 0.808, 0.922, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def event(self, event_type, *args):
        pass

    # GLFW window management
    def poll_events(self):
        glfw.poll_events()

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def get_glfw_window(self):
        return self.window

    def close(self):
        glfw.set_window_should_close(self.window, True)

    def cleanup(self):
        glfw.terminate()

    # GLFW window properties
    def set_title(self, title):
        glfw.set_window_title(self.window, title)

    def set_size(self, width, height):
        glfw.set_window_size(self.window, width, height)

    def set_position(self, x, y):
        glfw.set_window_pos(self.window, x, y)

    # GLFW utility functions
    def center_on_screen(self):
        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)
        window_width, window_height = glfw.get_window_size(self.window)
        window_x = (mode.width - window_width) // 2
        window_y = (mode.height - window_height) // 2
        glfw.set_window_pos(self.window, window_x, window_y)

    # Event handling
    def setup_event_callbacks(self):
        glfw.set_key_callback(self.window, self.key_callback)

    def key_callback(self, window, key, scancode, action, mods):
        self.notify("key_event", key, scancode, action, mods)
