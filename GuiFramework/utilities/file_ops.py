# GuiFramework/utilities/file_ops.py

import os
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
        """Write content to a file."""
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
        """Load content from a file."""
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
        """Create a file with content, if provided."""
        FileOps.write_file(file_path, "", encoding='utf-8')

    @staticmethod
    def delete_file(file_path):
        """Delete a file."""
        with FileOps.lock:
            try:
                os.remove(file_path)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Failed to delete file {file_path}: {e}")

    @staticmethod
    def copy_file(source_file, destination, preserve_metadata=False):
        """Copy a file to a destination."""
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
        """Move a file to a destination."""
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
        """Change the file extension of a file."""
        with FileOps.lock:
            try:
                base, _ = os.path.splitext(file_path)
                os.rename(file_path, f"{base}.{new_extension}")
            except Exception as e:
                print(f"Error changing file extension of file {file_path}: {e}")

    # Directory Operations
    @staticmethod
    def create_directory(directory):
        """Create a directory."""
        with FileOps.lock:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {directory}: {e}")

    @staticmethod
    def delete_directory(directory, delete_contents=True):
        """Delete a directory."""
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
        """Purge a directory of all contents."""
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
        """List all files in a directory."""
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
        """List all directories in a directory."""
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
        """Get all files and directories in a directory as a plain list."""
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
        """Check if a file exists in a directory."""
        with FileOps.lock:
            return os.path.exists(file_path)

    @staticmethod
    def is_file(file_path):
        """Check if a path is a file."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.isfile(file_path)
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def is_file_empty(file_path):
        """Check if a file is empty."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.stat(file_path).st_size == 0
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def is_file_readable(file_path):
        """Check if a file is readable."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.access(file_path, os.R_OK)
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def is_file_writable(file_path):
        """Check if a file is writable."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.access(file_path, os.W_OK)
            print(f"File not found: {file_path}")
            return False

    @staticmethod
    def get_file_size(file_path):
        """Get the file size in bytes."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getsize(file_path)
            print(f"File not found: {file_path}")
            return 0

    @staticmethod
    def get_file_creation_time(file_path):
        """Get the file creation time."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getctime(file_path)
            print(f"File not found: {file_path}")
            return 0

    @staticmethod
    def get_file_modification_time(file_path):
        """Get the file modification time."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getmtime(file_path)
            print(f"File not found: {file_path}")
            return 0

    @staticmethod
    def get_file_access_time(file_path):
        """Get the file access time."""
        with FileOps.lock:
            if FileOps.file_exists(file_path):
                return os.path.getatime(file_path)
            print(f"File not found: {file_path}")
            return 0

    # Directory Information
    @staticmethod
    def is_directory(directory):
        """Check if a path is a directory."""
        with FileOps.lock:
            return os.path.isdir(directory)

    @staticmethod
    def directory_exists(directory):
        """Check if a directory exists."""
        with FileOps.lock:
            return os.path.isdir(directory)

    @staticmethod
    def is_directory_empty(directory):
        """Check if a directory is empty."""
        with FileOps.lock:
            return not os.listdir(directory)

    @staticmethod
    def is_directory_readable(directory):
        """Check if a directory is readable."""
        with FileOps.lock:
            return os.access(directory, os.R_OK)

    @staticmethod
    def is_directory_writable(directory):
        """Check if a directory is writable."""
        with FileOps.lock:
            return os.access(directory, os.W_OK)

    # Path Operations
    @staticmethod
    def join_paths(*args):
        """Join paths together."""
        with FileOps.lock:
            return os.path.join(*args)

    @staticmethod
    def get_file_name(file_path):
        """Get the file name from a file path."""
        with FileOps.lock:
            return os.path.basename(file_path)

    @staticmethod
    def get_file_name_without_extension(file_path):
        """Get the file name without extension from a file path."""
        with FileOps.lock:
            return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def get_file_extension(file_path):
        """Get the file extension from a file path."""
        with FileOps.lock:
            return os.path.splitext(file_path)[1]

    @staticmethod
    def _get_directory(file_path):
        """Get the directory from a file path."""
        with FileOps.lock:
            return os.path.dirname(file_path)

    @staticmethod
    def get_directory_name(file_path):
        """Get the directory name from a file path."""
        with FileOps.lock:
            return os.path.dirname(file_path)

    @staticmethod
    def get_parent_directory(file_path, directory):
        """Get the parent directory from a file path."""
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
    def resolve_development_path(start_path, sub_path='', root_marker="main.py"):
        """
        Resolves the absolute path for a given sub-path relative to the project's root directory,
        starting the search from the given start_path.

        :param start_path: The absolute path of the starting point for the search, typically __file__ of the calling script.
        :param sub_path: A relative path from the project's root directory.
        :return: The absolute path corresponding to the sub_path within the project's root directory.
        """
        current_dir = os.path.dirname(os.path.abspath(start_path))

        while not os.path.exists(os.path.join(current_dir, root_marker)):
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                raise FileNotFoundError(f"Could not find the root marker '{root_marker}' in any parent directories.")
            current_dir = parent_dir

        return os.path.join(current_dir, sub_path)

    @staticmethod
    def get_invalid_file_name_chars(file_name, valid_chars=""):
        """Get invalid characters in a file name."""
        with FileOps.lock:
            invalid_chars = set(file_name) - set(valid_chars)
            if invalid_chars:
                return ", ".join(invalid_chars)
            return ""

    @staticmethod
    def get_file_names_in_directory(directory, include_nested=False):
        """List all file names in a directory."""
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
        """List all directory names in a directory."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [dn for dp, dn, filenames in os.walk(directory) for dn in dn]
                else:
                    return [entry.name for entry in os.scandir(directory) if entry.is_dir()]
            except Exception as e:
                print(f"Error while listing directories in directory {directory}: {e}")
                return []
