import customtkinter as ctk

from file_tree_view.file_tree_view import FileTreeView
from file_tree_view.folder_node import FolderNode

from GuiFramework.utilities import FileOps


class Test(ctk.CTkFrame):
    def __init__(self, parent_widget, *args, **kwargs):
        super().__init__(parent_widget, *args, **kwargs)

        path = FileOps.resolve_development_path(__file__, "test_dir", ".root")
        #  path = FileOps.resolve_development_path(__file__, "test_dir/folder 1", ".root")

        self.tree_view = FileTreeView(self, root_path=path)
        self.tree_view.pack(fill="both", expand=True)
        #  self.file_tree_view.refresh()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1366x768")
    test = Test(root)
    test.pack(side="left", fill="both", expand=True)
    root.mainloop()
