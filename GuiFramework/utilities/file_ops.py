# file_ops.py

import os


def load_file(file_path, encoding='utf-8'):
    """Load content from a file."""
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return ""
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()
    except Exception as e:
        print(f"Error while loading file {file_path}: {e}")
        return ""


def save_file(file_path, file_contents, encoding='utf-8'):
    """Save content to a file."""
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(file_contents)
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")


def load_file_to_textbox(textbox, file_path, encoding='utf-8'):
    """Load file content into a textbox widget."""
    try:
        textbox.delete("1.0", "end")
        if not os.path.exists(file_path):
            textbox.insert("1.0", f"File not found: {file_path}")
            return
        with open(file_path, "r", encoding=encoding) as file:
            textbox.insert("1.0", file.read())
    except Exception as e:
        print(f"Error while loading file {file_path}: {e}")


def save_file_from_textbox(textbox, file_path, encoding='utf-8'):
    """Save content from a textbox widget to a file."""
    try:
        with open(file_path, "w", encoding=encoding) as file:
            file.write(textbox.get("1.0", "end-1c"))
    except Exception as e:
        print(f"Error while saving file {file_path}: {e}")


def create_file(file_path):
    """Create an empty file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Use 'x' mode to create the file if it does not exist
        with open(file_path, "x", encoding='utf-8') as file:
            pass
        print(f"File created: {file_path}")
    except Exception as e:
        print(f"Failed to create file {file_path}: {e}")


def delete_file(file_path):
    """Delete a file."""
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Failed to delete file {file_path}: {e}")


def get_all_file_names_in_directory(directory):
    """List all file names in a directory."""
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"Error while listing files in directory {directory}: {e}")
        return []
