import customtkinter as ctk

from file_tree_view.file_tree_view import FileTreeView
from file_tree_view.folder_node import FolderNode
from file_tree_view.file_node import FileNode

from GuiFramework.utilities import FileOps


class Test(ctk.CTkFrame):
    def __init__(self, parent_widget, *args, **kwargs):
        super().__init__(parent_widget, *args, **kwargs)

        path = FileOps.resolve_development_path(__file__, "test_dir", ".root")
        #path = FileOps.resolve_development_path(__file__, "test_dir/folder 1", ".root")

        self.tree_view = FileTreeView(self, root_path=path)
        self.tree_view.pack(side="top", anchor="w", fill="both", expand=True)
        self.tree_view.root_node.node_container.update_idletasks()
        print(f"node_container width: {self.tree_view.root_node.node_container.winfo_width()}")
        print(f"node_container height: {self.tree_view.root_node.node_container.winfo_height()}")
        self.tree_view.root_node.state_icon_widget.update_idletasks()
        print(f"state_icon_widget width: {self.tree_view.root_node.state_icon_widget.winfo_width()}")
        print(f"state_icon_widget height: {self.tree_view.root_node.state_icon_widget.winfo_height()}")
        
        def print_selected_nodes():
            for node in self.tree_view.get_selected_nodes():
                print(node.text_widget_str)
        
        test_button = ctk.CTkButton(self, text="Test Button", command=print_selected_nodes)
        test_button.pack(side="top", anchor="w", fill="both", expand=True)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1366x768")
    test = Test(root)
    test.pack(side="left", fill="both", expand=True)
    root.mainloop()
