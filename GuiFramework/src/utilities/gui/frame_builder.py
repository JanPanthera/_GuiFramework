# frame_builder.py


class FrameBuilder:
    def __init__(self, widget_builder, apply_packing_func, logger=None):
        self.logger = logger
        self.widget_builder = widget_builder
        self.apply_packing = apply_packing_func

    def create_frame(self, name, frame_config, parent, instance):
        frame = self.widget_builder.create_widget("CTkFrame", frame_config.get("widget_properties", {}), parent, instance)
        self.apply_packing(frame, frame_config.get("packing_properties", {}))
        self.apply_grid_configuration(frame, frame_config.get("grid_configuration", {}))
        return frame

    @staticmethod
    def apply_grid_configuration(frame, grid_config):
        for row, conf in grid_config.get("rows", {}).items():
            frame.rowconfigure(int(row), **conf)
        for col, conf in grid_config.get("columns", {}).items():
            frame.columnconfigure(int(col), **conf)
