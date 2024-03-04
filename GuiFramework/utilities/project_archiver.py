# GuiFramework.utilities.project_archiver.py

import os
import shutil
import zipfile


class CopyType:
    ROOT_FOLDER = 1
    FOLDERS_ONLY = 2
    ALL = 3
    FILE = 4


class ProjectArchiver:
    """Class for archiving project files and folders."""

    def __init__(self, files_folders, zip_name, temp_folder, output_dir):
        """Initialize ProjectArchiver with files, folders, and paths."""
        self.files_folders = files_folders
        self.zip_name = zip_name
        self.temp_folder = temp_folder
        self.output_dir = output_dir

    def move_files_to_temp_folder(self):
        """Move files and folders to a temporary folder."""
        os.makedirs(self.temp_folder, exist_ok=True)
        for root, dirs, files in os.walk(self.temp_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        for file_folder, copy_type in self.files_folders.items():
            dest_path = os.path.join(self.temp_folder, os.path.basename(file_folder))
            if os.path.isdir(file_folder):
                if copy_type == CopyType.ROOT_FOLDER:
                    os.makedirs(dest_path, exist_ok=True)
                elif copy_type == CopyType.FOLDERS_ONLY:
                    for root, dirs, _ in os.walk(file_folder):
                        for dir in dirs:
                            os.makedirs(os.path.join(dest_path, dir), exist_ok=True)
                elif copy_type == CopyType.ALL:
                    shutil.copytree(file_folder, dest_path, dirs_exist_ok=True)
            elif os.path.isfile(file_folder) and copy_type == CopyType.FILE:
                shutil.copy(file_folder, dest_path)

    def create_zip_archive(self):
        """Create a zip archive of the files and folders in the temporary folder."""
        zip_path = os.path.join(self.output_dir, f"{self.zip_name}.zip")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.temp_folder):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    arcname = os.path.relpath(dir_path, start=self.temp_folder)
                    zipf.write(dir_path, arcname=arcname)
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=self.temp_folder)
                    zipf.write(file_path, arcname=arcname)