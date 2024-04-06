# GuiFramework/utilities/file_ops.py

import os
import sys
import json
import shutil
import fnmatch
import threading
import logging

from enum import Enum


class FileSizes(Enum):
    KB_1 = 1024
    KB_10 = 10240
    KB_100 = 102400
    MB_1 = 1048576
    MB_10 = 10485760
    MB_100 = 104857600
    GB_1 = 1073741824
    GB_10 = 10737418240
    GB_100 = 107374182400
    TB_1 = 1099511627776


class FileOps:
    lock = threading.RLock()

    # File Operations
    @staticmethod
    def write_file(file_path, content, append=False, encoding='utf-8'):
        """Write or append content to a file."""
        with FileOps.lock:
            try:
                FileOps.ensure_directory_exists(file_path)
                mode = "a" if append else "w"
                with open(file_path, mode, encoding=encoding) as file:
                    if isinstance(content, str):
                        file.write(content)
                    else:
                        file.writelines(str(line) for line in content)
            except Exception as e:
                print(f"Error saving file {file_path}: {e}")

    @staticmethod
    def append_file(file_path, content, encoding='utf-8'):
        """Append content to a file."""
        FileOps.write_file(file_path, content, append=True, encoding=encoding)

    @staticmethod
    def clear_file(file_path):
        """Clear the content of a file."""
        FileOps.write_file(file_path, "", encoding='utf-8')

    @staticmethod
    def load_file(file_path, encoding='utf-8'):
        """Load and return content from a file."""
        with FileOps.lock:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                return ""
            except Exception as e:
                print(f"Error while loading file {file_path}: {e}")
                return ""

    @staticmethod
    def create_file(file_path, encoding='utf-8'):
        """Create an empty file."""
        FileOps.write_file(file_path, "", encoding='utf-8')

    @staticmethod
    def delete_file(file_path):
        """Delete a specified file."""
        with FileOps.lock:
            try:
                os.remove(file_path)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Failed to delete file {file_path}: {e}")

    @staticmethod
    def copy_file(source_file, destination, preserve_metadata=False):
        """Copy a file to a specified destination."""
        with FileOps.lock:
            try:
                FileOps.ensure_directory_exists(destination)
                if preserve_metadata:
                    shutil.copy2(source_file, destination)
                else:
                    shutil.copy(source_file, destination)
            except FileNotFoundError as e:
                print(f"File not found: {source_file}")
            except Exception as e:
                print(f"Error copying file {source_file} to {destination}: {e}")

    @staticmethod
    def move_file(source_file, destination):
        """Move a file to a specified destination."""
        with FileOps.lock:
            try:
                FileOps.ensure_directory_exists(destination)
                shutil.move(source_file, destination)
            except FileNotFoundError as e:
                print(f"File not found: {source_file}")
            except Exception as e:
                print(f"Error moving file {source_file} to {destination}: {e}")

    @staticmethod
    def write_json(file_path, data, encoding='utf-8'):
        """Write JSON data to a file."""
        FileOps.write_file(file_path, json.dumps(data, indent=4), encoding=encoding)

    @staticmethod
    def change_file_extension(file_path, new_extension):
        """Change the extension of a specified file."""
        with FileOps.lock:
            try:
                base, _ = os.path.splitext(file_path)
                os.rename(file_path, f"{base}.{new_extension}")
            except Exception as e:
                print(f"Error changing file extension of file {file_path}: {e}")

    # Directory Operations
    @staticmethod
    def create_directory(directory):
        """Create a directory if it doesn't exist."""
        with FileOps.lock:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {directory}: {e}")

    @staticmethod
    def delete_directory(directory, delete_contents=True):
        """Delete a directory, optionally including its contents."""
        with FileOps.lock:
            try:
                if delete_contents:
                    shutil.rmtree(directory)
                else:
                    os.rmdir(directory)
            except FileNotFoundError:
                print(f"Directory not found: {directory}")
            except Exception as e:
                print(f"Failed to delete directory {directory}: {e}")

    @staticmethod
    def purge_directory(directory):
        """Remove all contents from a directory."""
        with FileOps.lock:
            try:
                for entry in os.scandir(directory):
                    if entry.is_file():
                        os.remove(entry.path)
                    else:
                        shutil.rmtree(entry.path)
            except FileNotFoundError:
                print(f"Directory not found: {directory}")
            except Exception as e:
                print(f"Failed to purge directory {directory}: {e}")

    @staticmethod
    def get_files_in_directory(directory, pattern="", include_nested=False):
        """List files in a directory, optionally matching a pattern and including nested directories."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if fnmatch.fnmatch(f, pattern)]
                else:
                    return [entry.path for entry in os.scandir(directory) if entry.is_file() and fnmatch.fnmatch(entry.name, pattern)]
            except Exception as e:
                print(f"Error while listing files in directory {directory}: {e}")
                return []

    @staticmethod
    def get_directories_in_directory(directory, pattern="", include_nested=False):
        """List directories in a directory, optionally matching a pattern and including nested directories."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [dp for dp, dn, filenames in os.walk(directory) for d in dn if fnmatch.fnmatch(d, pattern)]
                else:
                    return [entry.path for entry in os.scandir(directory) if entry.is_dir() and fnmatch.fnmatch(entry.name, pattern)]
            except Exception as e:
                print(f"Error while listing directories in directory {directory}: {e}")
                return []

    @staticmethod
    def get_contents_in_directory(directory, pattern="", include_nested=False):
        """List all contents in a directory, optionally matching a pattern and including nested directories."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if fnmatch.fnmatch(f, pattern)]
                else:
                    return [entry.path for entry in os.scandir(directory) if fnmatch.fnmatch(entry.name, pattern)]
            except Exception as e:
                print(f"Error while listing contents in directory {directory}: {e}")
                return []

    # File Information
    @staticmethod
    def file_exists(file_path):
        """Return True if the specified file exists."""
        with FileOps.lock:
            return os.path.exists(file_path)

    @staticmethod
    def is_file(file_path):
        """Return True if the path is a file; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.isfile(file_path)
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def is_file_empty(file_path):
        """Return True if the file is empty; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.stat(file_path).st_size == 0
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def is_file_readable(file_path):
        """Return True if the file is readable; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.access(file_path, os.R_OK)
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def is_file_writable(file_path):
        """Return True if the file is writable; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.access(file_path, os.W_OK)
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def get_file_size(file_path):
        """Return the file size in bytes; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getsize(file_path)
            print(f"File not found: {file_path}")
            return 0

    @staticmethod
    def get_file_creation_time(file_path):
        """Return the file creation time; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getctime(file_path)
            print(f"File not found: {file_path}")
            return 0

    @staticmethod
    def get_file_modification_time(file_path):
        """Return the file modification time; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getmtime(file_path)
            print(f"File not found: {file_path}")
            return 0

    @staticmethod
    def get_file_access_time(file_path):
        """Return the file access time; print an error if not found."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getatime(file_path)
            print(f"File not found: {file_path}")
            return 0

    @staticmethod
    def validate_file_name(file_name):
        """Return invalid characters in a file name."""
        with FileOps.lock:
            return FileOps.get_invalid_file_name_chars(file_name)

    # Directory Information
    @staticmethod
    def is_directory(directory):
        """Return True if the path is a directory."""
        with FileOps.lock:
            return os.path.isdir(directory)

    @staticmethod
    def directory_exists(directory):
        """Return True if the directory exists."""
        with FileOps.lock:
            return os.path.isdir(directory)

    @staticmethod
    def is_directory_empty(directory):
        """Return True if the directory is empty."""
        with FileOps.lock:
            return not os.listdir(directory)

    @staticmethod
    def is_directory_readable(directory):
        """Return True if the directory is readable."""
        with FileOps.lock:
            return os.access(directory, os.R_OK)

    @staticmethod
    def is_directory_writable(directory):
        """Return True if the directory is writable."""
        with FileOps.lock:
            return os.access(directory, os.W_OK)

    @staticmethod
    def validate_directory_name(directory_name):
        """Return invalid characters in a directory name."""
        with FileOps.lock:
            return FileOps.get_invalid_file_name_chars(directory_name)

    # Path Operations
    @staticmethod
    def join_paths(*args):
        """Join and return the combined paths."""
        with FileOps.lock:
            return os.path.join(*args)

    @staticmethod
    def get_file_name(file_path):
        """Return the file name from a file path."""
        with FileOps.lock:
            return os.path.basename(file_path)

    @staticmethod
    def get_file_name_without_extension(file_path):
        """Return the file name without its extension from a file path."""
        with FileOps.lock:
            return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def get_file_extension(file_path):
        """Return the file extension from a file path."""
        with FileOps.lock:
            return os.path.splitext(file_path)[1]

    @staticmethod
    def _get_directory(file_path):
        """Return the directory from a file path."""
        with FileOps.lock:
            return os.path.dirname(file_path)

    @staticmethod
    def get_directory_name(file_path):
        """Return the directory name from a file path."""
        with FileOps.lock:
            return os.path.dirname(file_path)

    @staticmethod
    def get_parent_directory(file_path, directory):
        """Return the parent directory from a file path."""
        with FileOps.lock:
            while file_path:
                file_path, tail = os.path.split(file_path)
                if tail == directory:
                    return FileOps.join_paths(file_path, tail)
            return None

    # Utility Operations
    @staticmethod
    def ensure_directory_exists(file_path):
        """Ensure the directory of the given file path exists."""
        directory = os.path.dirname(file_path)
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def resolve_development_path(start_path, sub_path='', root_marker="GuiFramework"):
        """Resolve and return the absolute path for a given sub-path relative to the project's root,
        adapting for both development environments and packaged EXE environments."""
        # Check if running as a standalone EXE
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), sub_path)
        else:
            current_dir = os.path.dirname(os.path.abspath(start_path))

            while not os.path.basename(current_dir) == root_marker:
                parent_dir = os.path.dirname(current_dir)
                if parent_dir == current_dir:
                    raise FileNotFoundError(f"Could not find the root marker '{root_marker}' in any parent directories.")
                current_dir = parent_dir

            return os.path.join(current_dir, sub_path)

    @staticmethod
    def get_invalid_file_name_chars(file_name):
        """Return invalid characters in a file name, 'Empty file name' if empty or the file_name if valid."""
        with FileOps.lock:
            if not file_name.strip():
                return "Empty file name"

            # Including control characters and spaces in the set of invalid characters
            invalid_chars = set('\\/:*?"<>|' + ''.join(chr(i) for i in range(32)))  # ASCII 0-31 are control chars
            found_invalid_chars = {char for char in file_name if char in invalid_chars}

            # Check for OS reserved names (mainly for Windows)
            reserved_names = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
            base_name, ext = os.path.splitext(file_name)
            if base_name.upper() in reserved_names:
                found_invalid_chars.add(base_name)

            if found_invalid_chars:
                return ', '.join(found_invalid_chars)
            else:
                return file_name

    @staticmethod
    def get_file_names_in_directory(directory, include_nested=False):
        """List and return all file names in a directory."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [f for dp, dn, filenames in os.walk(directory) for f in filenames]
                else:
                    return [entry.name for entry in os.scandir(directory) if entry.is_file()]
            except Exception as e:
                print(f"Error while listing files in directory {directory}: {e}")
                return []

    @staticmethod
    def get_directory_names_in_directory(directory, include_nested=False):
        """List and return all directory names in a directory."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [dn for dp, dn, filenames in os.walk(directory) for dn in dn]
                else:
                    return [entry.name for entry in os.scandir(directory) if entry.is_dir()]
            except Exception as e:
                print(f"Error while listing directories in directory {directory}: {e}")
                return []
