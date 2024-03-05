import os
import customtkinter as ctk


class Node(ctk.CTkButton):
    def __init__(self, parent, path, level=1, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(text=os.path.basename(path), bg_color='transparent', anchor='nw')
        self.level = level
        self.is_root = False

    def show(self):
        padx_left = 0 if self.is_root else 20 * (self.level - 1)
        self.pack(padx=(padx_left, 5), pady=(2, 2), anchor='nw', fill='none', expand=False)

    def hide(self):
        self.pack_forget()


class FileNode(Node):
    pass


class FolderNode(Node):
    def __init__(self, parent, folder_path, level=1, *args, **kwargs):
        super().__init__(parent, folder_path, level, *args, **kwargs)
        self.subnodes = []
        self.expanded = False
        self.folder_path = str(folder_path)
        self.configure(command=self.toggle_subnodes)
        self.populate_subnodes(parent)

    def populate_subnodes(self, root):
        for entry in os.scandir(self.folder_path):
            entry_path = entry.path
            if entry.is_dir():
                self.subnodes.append(FolderNode(root, entry_path, self.level + 1))
            elif entry.is_file():
                self.subnodes.append(FileNode(root, entry_path, self.level + 1))

    def toggle_subnodes(self):
        if self.expanded:
            self.hide_subnodes()
        else:
            self.show_subnodes()

    def show_subnodes(self):
        for subnode in self.subnodes:
            subnode.show()
        self.expanded = True

    def hide_subnodes(self):
        for subnode in self.subnodes:
            subnode.hide()
            if isinstance(subnode, FolderNode) and subnode.expanded:
                subnode.hide_subnodes()
        self.expanded = False


class TreeStructure(ctk.CTkFrame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(expand=True, fill='both')
        self.root_node = FolderNode(self, root)
        self.root_node.is_root = True
        self.root_node.show()
