# GuiFramework/widgets/tree_view/test_dictionary_tree_view.py

import customtkinter as ctk

from GuiFramework.widgets.tree_view.dictionary_tree_view import DictionaryTreeView
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

    # multi level test dictionary data
    test_dictionary_data = {
        "level0": {
            "level0_data1": "level0_file1.txt",
            "level0_data2": "level0_file2.txt",
            "level1": {
                "level1_data1": "level1_file1.txt",
                "level1_data2": "level1_file2.txt",
                "level2": {
                    "level2_data1": "level2_file1.txt",
                    "level2_data2": "level2_file2.txt",
                    "level3": {
                        "level3_data1": "level3_file1.txt",
                        "level3_data2": "level3_file2.txt",
                    }
                }
            },
            "level1_2": {
                "level1_2_data1": "level1_2_file1.txt",
                "level1_2_data2": "level1_2_file2.txt",
            }
        }
    }

    dictionary_structure_view = DictionaryTreeView(root_frame, test_dictionary_data)
    dictionary_structure_view.grid(row=0, column=0, sticky="nsew")

    button = ctk.CTkButton(root, text="Get selected files", command=lambda: print(dictionary_structure_view.get_selected_files()))
    button.pack(anchor="nw")

    select_all_button = ctk.CTkButton(root, text="Select all", command=dictionary_structure_view.select_all)
    select_all_button.pack(anchor="nw")

    deselect_all_button = ctk.CTkButton(root, text="Deselect all", command=dictionary_structure_view.deselect_all)
    deselect_all_button.pack(anchor="nw")

    expand_all_button = ctk.CTkButton(root, text="Expand all", command=dictionary_structure_view.expand_all)
    expand_all_button.pack(anchor="nw")

    collapse_all_button = ctk.CTkButton(root, text="Collapse all", command=dictionary_structure_view.collapse_all)
    collapse_all_button.pack(anchor="nw")

    root.mainloop()


if __name__ == "__main__":
    main()
