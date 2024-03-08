# GuiFramework/utilities/file_ops.py

import os
import json
import shutil
import threading

from GuiFramework.utilities.utils import setup_default_logger


class FileOps:
    logger = setup_default_logger(log_name="FileOps", log_directory="GuiFramework")
    lock = threading.RLock()

    # File Operations
    @staticmethod
    def write_file(file_path, content, append=False, encoding='utf-8'):
        """Write content to a file."""
        with FileOps.lock:
            try:
                mode = "a" if append else "w"
                with open(file_path, mode, encoding=encoding) as file:
                    if isinstance(content, str):
                        file.write(content)
                    else:
                        file.writelines(str(line) for line in content)
            except Exception as e:
                FileOps.logger.error(f"Error saving file {file_path}: {e}")

    @staticmethod
    def load_file(file_path, encoding='utf-8'):
        """Load content from a file."""
        with FileOps.lock:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except FileNotFoundError:
                FileOps.logger.error(f"File not found: {file_path}")
                return ""
            except Exception as e:
                FileOps.logger.error(f"Error while loading file {file_path}: {e}")
                return ""

    @staticmethod
    def create_file(file_path, encoding='utf-8'):
        """Create a file with content, if provided."""
        with FileOps.lock:
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding=encoding) as file:
                    pass
            except Exception as e:
                FileOps.logger.error(f"Failed to create file {file_path}: {e}")

    @staticmethod
    def delete_file(file_path):
        """Delete a file."""
        with FileOps.lock:
            try:
                os.remove(file_path)
            except FileNotFoundError:
                FileOps.logger.warning(f"File not found: {file_path}")
            except Exception as e:
                FileOps.logger.error(f"Failed to delete file {file_path}: {e}")

    @staticmethod
    def copy_file(source_file, destination, preserve_metadata=False):
        """Copy a file to a destination."""
        with FileOps.lock:
            try:
                if preserve_metadata:
                    shutil.copy2(source_file, destination)
                else:
                    shutil.copy(source_file, destination)
            except FileNotFoundError as e:
                FileOps.logger.error(f"File not found: {source_file}")
            except Exception as e:
                FileOps.logger.error(f"Error copying file {source_file} to {destination}: {e}")

    @staticmethod
    def move_file(source_file, destination):
        """Move a file to a destination."""
        with FileOps.lock:
            try:
                shutil.move(source_file, destination)
            except FileNotFoundError as e:
                FileOps.logger.error(f"File not found: {source_file}")
            except Exception as e:
                FileOps.logger.error(f"Error moving file {source_file} to {destination}: {e}")

    @staticmethod
    def write_json(file_path, data, encoding='utf-8'):
        """Write JSON data to a file."""
        with FileOps.lock:
            try:
                with open(file_path, 'w', encoding=encoding) as file:
                    json.dump(data, file, indent=4)
            except Exception as e:
                FileOps.logger.error(f"Error writing JSON to file {file_path}: {e}")

    # Directory Operations
    @staticmethod
    def create_directory(directory):
        """Create a directory."""
        with FileOps.lock:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                FileOps.logger.error(f"Failed to create directory {directory}: {e}")

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
                FileOps.logger.warning(f"Directory not found: {directory}")
            except Exception as e:
                FileOps.logger.error(f"Failed to delete directory {directory}: {e}")

    @staticmethod
    def get_all_files_in_directory(directory, include_nested=False):
        """List all files in a directory."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames]
                else:
                    return [entry.path for entry in os.scandir(directory) if entry.is_file()]
            except Exception as e:
                FileOps.logger.error(f"Error while listing files in directory {directory}: {e}")
                return []

    @staticmethod
    def get_all_directories_in_directory(directory, include_nested=False):
        """List all directories in a directory."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [dp for dp, dn, filenames in os.walk(directory) for dn in dn]
                else:
                    return [entry.path for entry in os.scandir(directory) if entry.is_dir()]
            except Exception as e:
                FileOps.logger.error(f"Error while listing directories in directory {directory}: {e}")
                return []

    @staticmethod
    def get_all_contents_in_directory(directory, include_nested=False):
        """Get all files and directories in a directory as a plain list."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames]
                else:
                    return [entry.path for entry in os.scandir(directory)]
            except Exception as e:
                FileOps.logger.error(f"Error while listing contents in directory {directory}: {e}")
                return []

    # File Information
    @staticmethod
    def is_file(file_path):
        """Check if a path is a file."""
        with FileOps.lock:
            return os.path.isfile(file_path)

    @staticmethod
    def file_exists(file_path):
        """Check if a file exists in a directory."""
        with FileOps.lock:
            return os.path.exists(file_path)

    @staticmethod
    def is_file_empty(file_path):
        """Check if a file is empty."""
        with FileOps.lock:
            return os.path.getsize(file_path) == 0

    @staticmethod
    def is_file_readable(file_path):
        """Check if a file is readable."""
        with FileOps.lock:
            return os.access(file_path, os.R_OK)

    @staticmethod
    def is_file_writable(file_path):
        """Check if a file is writable."""
        with FileOps.lock:
            return os.access(file_path, os.W_OK)

    @staticmethod
    def get_file_size(file_path):
        """Get the file size in bytes."""
        with FileOps.lock:
            return os.path.getsize(file_path)

    @staticmethod
    def get_file_creation_time(file_path):
        """Get the file creation time."""
        with FileOps.lock:
            return os.path.getctime(file_path)

    @staticmethod
    def get_file_modification_time(file_path):
        """Get the file modification time."""
        with FileOps.lock:
            return os.path.getmtime(file_path)

    @staticmethod
    def get_file_access_time(file_path):
        """Get the file access time."""
        with FileOps.lock:
            return os.path.getatime(file_path)

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
    def is_file_name_valid(file_name, invalid_chars=""):
        """Check if a file name is valid."""
        with FileOps.lock:
            return not any(char in invalid_chars for char in file_name)

    @staticmethod
    def get_all_file_names_in_directory(directory, include_nested=False):
        """List all file names in a directory."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [f for dp, dn, filenames in os.walk(directory) for f in filenames]
                else:
                    return [entry.name for entry in os.scandir(directory) if entry.is_file()]
            except Exception as e:
                FileOps.logger.error(f"Error while listing files in directory {directory}: {e}")
                return []

    @staticmethod
    def get_all_directory_names_in_directory(directory, include_nested=False):
        """List all directory names in a directory."""
        with FileOps.lock:
            try:
                if include_nested:
                    return [dn for dp, dn, filenames in os.walk(directory) for dn in dn]
                else:
                    return [entry.name for entry in os.scandir(directory) if entry.is_dir()]
            except Exception as e:
                FileOps.logger.error(f"Error while listing directories in directory {directory}: {e}")
                return []
