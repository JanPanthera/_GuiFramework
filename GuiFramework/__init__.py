# GuiFramework/__init__.py


from GuiFramework.core import *
from GuiFramework.gui import *
from GuiFramework.widgets import *
from GuiFramework.utilities import *

Logger.add_logger(
    LoggerConfig(
        logger_name="GuiFramework",
        log_name="gui_framework",
        log_directory=FileOps.resolve_development_path(__file__, "logs", ".root"),
        log_level=LOG_LEVEL.DEBUG,  # Change this to LOG_LEVEL.INFO for production
        module_name="GuiFramework"
    ),
    rotate_on_add=True
)
