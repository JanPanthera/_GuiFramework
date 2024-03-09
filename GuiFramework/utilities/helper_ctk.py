# GuiFramework/utilities/helper_ctk.py

import customtkinter as ctk

from GuiFramework.utilities.file_ops import FileOps
from GuiFramework.utilities.utils import setup_default_logger


class CtkHelper:
    logger = setup_default_logger(log_name="CtkHelper", log_directory="logs/GuiFramework")

    @staticmethod
    def load_file_to_textbox(textbox, file_path, overwrite=False, append=False, encoding="utf-8"):
        """Load content from a file to a textbox widget."""
        try:
            if not FileOps.file_exists(file_path):
                CtkHelper.logger.error(f"File not found: {file_path}")
                return

            content = FileOps.load_file(file_path, encoding)
            if content:
                if overwrite or not textbox.get("1.0", "end-1c").strip():
                    textbox.delete("1.0", "end")
                if append or not textbox.get("1.0", "end-1c").strip():
                    textbox.insert("end", content)
                else:
                    textbox.insert("1.0", content)
        except Exception as e:
            CtkHelper.logger.error(f"Error while loading file {file_path}: {e}")

    @staticmethod
    def save_textbox_to_file(textbox, file_path, overwrite=False, append=False, encoding="utf-8"):
        """Write content from a textbox widget to a file."""
        try:
            content = textbox.get("1.0", "end-1c")
            if content:
                FileOps.write_file(file_path, content, overwrite, append, encoding)
        except Exception as e:
            CtkHelper.logger.error(f"Error while saving file {file_path}: {e}")

    @staticmethod
    def update_widget_text(widget, text):
        widget_types = (ctk.CTkLabel, ctk.CTkButton, ctk.CTkCheckBox)
        if isinstance(widget, widget_types):
            widget.configure(text=text)
        else:
            # CtkHelper.logger.warning(f"Unsupported widget type: {type(widget).__name__}")
            pass