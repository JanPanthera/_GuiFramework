import os
import customtkinter as ctk


class Node(ctk.CTkButton):
    def __init__(self, parent, path, icon=None, level=0, *args, **kwargs):
        self.node_base_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.node_base_container.pack(padx=0, pady=0, ipadx=0, ipady=0, anchor='nw')
        self.visible = False
        self.path = path
        self.name = os.path.basename(path)
        self.icon = None

        if not isinstance(icon, str):
            icon = self._get_default_icon(path)

        self.icon = ctk.CTkLabel(self.node_base_container, text=icon, fg_color="transparent", anchor='nw')
        self.icon.pack(side='left', padx=(0, 5), pady=0, ipadx=0, ipady=0)

        super().__init__(self.node_base_container, text=os.path.basename(path), anchor='nw', corner_radius=0, *args, **kwargs)
        self.pack(side='left', padx=0, pady=0, ipadx=0, ipady=0)
        if level == 0:
            self.show()
        self.level = level

    def show(self):
        self.node_base_container.pack(padx=0, pady=0, anchor='nw')
        self.visible = True

    def hide(self):
        self.node_base_container.pack_forget()
        self.visible = False

    def update_icon(self, icon):
        self.icon.configure(text=icon)

    def _get_default_icon(self, path):
        if path.endswith((".zip", ".7z", ".tar", ".gz", ".bz2", ".xz")):
            return "📦"
        elif path.endswith(".iso"):
            return "💿"
        elif os.path.isfile(path):
            return "📄"
        elif os.path.isdir(path):
            return "📁"
        elif os.path.islink(path):
            return "🔗"
        else:
            return "📝"


class FileNode(Node):
    def __init__(self, parent, file_path, level=1, *args, **kwargs):
        super().__init__(parent, file_path, level=level, hover=False, fg_color="transparent", *args, **kwargs)
        self.configure(command=self.toggle_selection)
        self.selected = False

    def toggle_selection(self):
        if self.selected:
            self.deselect()
        else:
            self.select()

    def select(self):
        if not self.selected and self.visible:
            self.selected = True
            self.configure(fg_color="#4d4d4d")

    def deselect(self):
        if self.selected and self.visible:
            self.selected = False
            self.configure(fg_color="transparent")


class FolderNode(Node):
    def __init__(self, parent, folder_path, level=1, *args, **kwargs):
        self.expanded_icon = "📂"
        self.collapsed_icon = "📁"

        self.folder_base_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.folder_base_container.pack(padx=0, pady=0, ipadx=0, ipady=0, anchor='nw')

        self.subnodes_container = ctk.CTkFrame(self.folder_base_container, fg_color="transparent")

        super().__init__(self.folder_base_container, folder_path, level=level, fg_color="transparent", *args, **kwargs)
        self.configure(command=self.toggle_subnodes)

        self.subnodes = []
        self.expanded = False
        self.populate_subnodes(self.subnodes_container)

    def populate_subnodes(self, container):
        entries = sorted((e for e in os.scandir(self.path) if e.is_dir() or e.is_file()), key=lambda e: e.name)
        root_depth = len(self.path.split(os.sep))
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
            self.update_icon(self.collapsed_icon)
        else:
            self.show_subnodes()
            self.update_icon(self.expanded_icon)

    def show_subnodes(self):
        self.subnodes_container.pack(padx=(15, 0), pady=0, ipadx=0, ipady=0, anchor='nw')
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
        self.root_node = FolderNode(self, root)

    # Public methods
    def expand_all(self):
        self._expand_all(self.root_node)

    def collapse_all(self):
        self._deselect_all(self.root_node)
        self._collapse_all(self.root_node)

    def select_all(self):
        self._select_all(self.root_node)

    def deselect_all(self):
        self._deselect_all(self.root_node)

    def get_selected_files(self):
        selected_files = {}
        self._get_selected_files(self.root_node, selected_files)
        return selected_files

    # Private methods
    def _expand_all(self, node):
        node.show_subnodes()
        for subnode in node.subnodes:
            if isinstance(subnode, FolderNode):
                self._expand_all(subnode)

    def _collapse_all(self, node):
        node.hide_subnodes()
        for subnode in node.subnodes:
            if isinstance(subnode, FolderNode):
                self._collapse_all(subnode)

    def _select_all(self, node):
        for subnode in node.subnodes:
            if isinstance(subnode, FolderNode):
                self._select_all(subnode)
            elif isinstance(subnode, FileNode):
                subnode.select()

    def _deselect_all(self, node):
        for subnode in node.subnodes:
            if isinstance(subnode, FolderNode):
                self._deselect_all(subnode)
            elif isinstance(subnode, FileNode):
                subnode.deselect()

    def _get_selected_files(self, node, selected_files):
        for subnode in node.subnodes:
            if isinstance(subnode, FolderNode):
                self._get_selected_files(subnode, selected_files)
            elif isinstance(subnode, FileNode) and subnode.selected:
                selected_files[subnode.name] = subnode.path
