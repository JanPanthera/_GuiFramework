import os
import customtkinter as ctk

# TODO: icon optionally a image file
class Node(ctk.CTkButton):
    def __init__(self, parent, path, icon=None, level=1, *args, **kwargs):
        self.base_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.base_container.pack(padx=0, pady=0, anchor='nw')

        if icon:
            self.icon = ctk.CTkLabel(self.base_container, text=icon, fg_color="transparent", anchor='nw')
            self.icon.pack(side='left', padx=(0, 5), pady=0, anchor='nw')

        super().__init__(self.base_container, text=os.path.basename(path), anchor='nw', corner_radius=0, *args, **kwargs)
        self.pack(side='left', padx=0, pady=0, anchor='nw')
        if level == 0:
            self.show()
        self.level = level

    def show(self):
        self.base_container.pack(padx=2, pady=2, anchor='nw')

    def hide(self):
        self.base_container.pack_forget()


class FileNode(Node):
    def __init__(self, parent, file_path, level=1, *args, **kwargs):
        super().__init__(parent, file_path, icon="📄", level=level, hover=False, fg_color="transparent", *args, **kwargs)


class FolderNode(Node):
    def __init__(self, parent, folder_path, level=1, *args, **kwargs):
        self.base_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.base_container.pack(padx=0, pady=0, anchor='nw')

        self.subnodes_container = ctk.CTkFrame(self.base_container, fg_color="transparent")
        super().__init__(self.base_container, folder_path, icon="📁", level=level, fg_color="transparent", *args, **kwargs)
        self.configure(command=self.toggle_subnodes)
        self.subnodes = []
        self.expanded = False
        self.folder_path = str(folder_path)
        self.populate_subnodes(self.subnodes_container)

    def populate_subnodes(self, container):
        entries = sorted((e for e in os.scandir(self.folder_path) if e.is_dir() or e.is_file()), key=lambda e: e.name)
        root_depth = len(self.folder_path.split(os.sep))
        for entry in entries:
            entry_depth = len(entry.path.split(os.sep))
            if entry_depth > root_depth + 1:
                continue
            if entry.is_dir():
                self.subnodes.append(FolderNode(container, entry.path, self.level + 1))
            elif entry.is_file():
                self.subnodes.append(FileNode(container, entry.path, self.level + 1))

    def toggle_subnodes(self):
        if self.expanded:
            self.hide_subnodes()
        else:
            self.show_subnodes()

    def show_subnodes(self):
        self.subnodes_container.pack(padx=(15, 0), pady=0, anchor='nw')
        for subnode in self.subnodes:
            subnode.show()
        self.expanded = True

    def hide_subnodes(self):
        for subnode in self.subnodes:
            subnode.hide()
            if isinstance(subnode, FolderNode):
                subnode.hide_subnodes()
        self.subnodes_container.pack_forget()
        self.expanded = False


class TreeStructure(ctk.CTkFrame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root_node = FolderNode(self, root, level=0)
