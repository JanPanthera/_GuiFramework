# GuiFramework/__init__.py


from GuiFramework.gui import *
from GuiFramework.widgets import *
from GuiFramework.utilities import *


config = LoggerConfig(
    log_name="GuiFramework",
    log_directory=FileOps.resolve_development_path(__file__, "logs", ".root"),
    log_level=LOG_LEVEL.DEBUG,
    enabled=True,
)
Logger.add_config(logger_name="GuiFramework", config=config)
Logger.rotate_file(logger_name="GuiFramework")
