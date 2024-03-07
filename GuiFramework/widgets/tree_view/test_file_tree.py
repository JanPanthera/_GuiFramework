import os
import customtkinter as ctk

from GuiFramework.widgets.tree_view.file_tree_view import FileTreeView
from GuiFramework.utilities.event_manager import EventManager


def main():
    root = ctk.CTk()
    root.title("Folder Structure View")
    root.geometry("1366x768")

    root_frame = ctk.CTkFrame(root)
    root_frame.pack(anchor="nw", fill="both", expand=True)

    root_frame.rowconfigure(0, weight=1)
    root_frame.columnconfigure(0, weight=1)
    root_frame.columnconfigure(1, weight=10)

    def handle_file_selected(file_node):
        file_node.rename(f"*{file_node.name}")

    def handle_file_deselected(file_node):
        file_node.rename(file_node.name.replace("*", ""))

    EventManager.subscribe("file_selected", handle_file_selected)
    EventManager.subscribe("file_deselected", handle_file_deselected)

    # Create the folder structure view
    file_path = r"C:\__JanPanthera__\_Workspace\_VS-Studio\_Projects\_PythonWorkspace\_AutoDriveTranslationTool\AutoDriveTranslationTool"
    # file_path = r"C:\__JanPanthera__\_Workspace\_VS-Studio\_Projects\_PythonWorkspace\_AutoDriveTranslationTool\AutoDriveTranslationTool\_output"
    folder_structure_view = FileTreeView(root_frame, file_path, multi_select=True)
    folder_structure_view.grid(row=0, column=0, sticky="nsew")

    button = ctk.CTkButton(root, text="Get selected files", command=lambda: print(folder_structure_view.get_selected_files()))
    button.pack(anchor="nw")

    select_all_button = ctk.CTkButton(root, text="Select all", command=folder_structure_view.select_all)
    select_all_button.pack(anchor="nw")

    deselect_all_button = ctk.CTkButton(root, text="Deselect all", command=folder_structure_view.deselect_all)
    deselect_all_button.pack(anchor="nw")

    expand_all_button = ctk.CTkButton(root, text="Expand all", command=folder_structure_view.expand_all)
    expand_all_button.pack(anchor="nw")

    collapse_all_button = ctk.CTkButton(root, text="Collapse all", command=folder_structure_view.collapse_all)
    collapse_all_button.pack(anchor="nw")

    root.mainloop()


if __name__ == "__main__":
    main()
