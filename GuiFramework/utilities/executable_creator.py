# GuiFramework.utilities.executable_creator.py

import os
import shutil
import subprocess
import threading

from pathlib import Path
from GuiFramework.utilities.logging import Logger


class ExecutableCreator:
    def __init__(self, main_script_path, exe_name, dist_path, work_path, no_console=False, additional_flags=None):
        """Initialize ExecutableCreator with script, paths, and flags."""
        self.logger = Logger.get_logger("GuiFramework")
        self.main_script_path = Path(main_script_path)
        self.exe_name = exe_name
        self.dist_path = Path(dist_path)
        self.work_path = Path(work_path)
        self.no_console = no_console
        self.additional_flags = additional_flags or []
        self.output_exe_path = self.dist_path / f"{self.exe_name}.exe"
        self._validate_inputs()

    def add_hidden_import(self, import_name):
        """Add a hidden import."""
        self.additional_flags.append(f"--hidden-import={import_name}")

    def add_additional_flag(self, flag):
        """Add an additional flag."""
        self.additional_flags.append(flag)

    def set_icon(self, icon_path):
        """Set the icon for the executable."""
        self.additional_flags.append(f"--icon={icon_path}")

    def add_data_file(self, source, destination):
        """Add a data file to the executable."""
        self.additional_flags.append(f"--add-data={source}{os.pathsep}{destination}")

    def create_executable(self):
        """Create the executable file."""
        try:
            pyinstaller_command = [
                "pyinstaller",
                "--onefile",
                f"--distpath={self.dist_path}",
                f"--workpath={self.work_path}",
                f"--name={self.exe_name}",
                "--debug=all",
                *self.additional_flags,
                str(self.main_script_path)
            ]

            if self.no_console:
                pyinstaller_command.append("--noconsole")

            def handle_stream(stream):
                for line in iter(stream.readline, ""):
                    print(line.strip())
                stream.close()

            process = subprocess.Popen(pyinstaller_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

            stdout_thread = threading.Thread(target=handle_stream, args=(process.stdout,))
            stderr_thread = threading.Thread(target=handle_stream, args=(process.stderr,))

            stdout_thread.start()
            stderr_thread.start()

            stdout_thread.join()
            stderr_thread.join()

            return_code = process.wait()

            if return_code != 0:
                self.logger.log_error("Error occurred while creating the executable.", "ExecutableCreator")
            else:
                self._clean_up_temporary_files()
                self._validate_output_executable()

        except FileNotFoundError as e:
            self.logger.log_error(f"File not found: {e}", "ExecutableCreator")
        except Exception as e:
            self.logger.log_error(f"An unexpected error occurred: {e}", "ExecutableCreator")

    def _clean_up_temporary_files(self):
        """Clean up temporary files after creating the executable."""
        shutil.rmtree(self.work_path, ignore_errors=True)

    def _validate_inputs(self):
        """Validate the inputs for creating the executable."""
        if not self.main_script_path.exists():
            raise FileNotFoundError(f"Main script not found: {self.main_script_path}")

        if not shutil.which("pyinstaller"):
            raise EnvironmentError("PyInstaller is not installed or not in the system's PATH.")

    def _validate_output_executable(self):
        """Validate the output executable file."""
        if not self.output_exe_path.is_file():
            raise ValueError(f"Output executable is not a valid file: {self.output_exe_path}")
