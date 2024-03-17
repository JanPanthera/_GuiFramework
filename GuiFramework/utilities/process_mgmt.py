# GuiFrameworl/utilities/process_mgmt.py

import sys
import subprocess


def run_script(console_output, script, args, after_callback):
    def read_output(process, is_stderr=False):
        stream = process.stderr if is_stderr else process.stdout
        next_line = stream.readline()
        if next_line:
            console_output.configure(state="normal")
            console_output.insert("end", next_line)
            console_output.see("end")
            after_callback(1, lambda: read_output(process, is_stderr))
        elif process.poll() is None:
            after_callback(1, lambda: read_output(process, is_stderr))
        else:
            if not is_stderr:
                after_callback(1, lambda: read_output(process, True))
            else:
                console_output.configure(state="disabled")

    try:
        command = [sys.executable, script] + args
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        after_callback(1, lambda: read_output(process))
    except Exception as e:
        console_output.configure(state="normal")
        console_output.insert("end", f"Failed to run the script: {e}\n")
        console_output.configure(state="disabled")
