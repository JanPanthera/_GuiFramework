# GuiFramework/widgets/tree_view/file_tree_view/file_tree_view.py

import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .file_node import FileNode
from .folder_node import FolderNode
from GuiFramework.widgets.tree_view.base.base_tree_view import BaseTreeView


class DirectoryWatcher:
    def __init__(self, watch_directory, on_created, on_deleted, on_moved):
        self._watch_directory = watch_directory
        self._event_handler = FileSystemEventHandler()
        self._event_handler.on_created = on_created
        self._event_handler.on_deleted = on_deleted
        self._event_handler.on_moved = on_moved

        self._observer = Observer()
        self._observer.schedule(self._event_handler, self._watch_directory, recursive=True)

    def start(self):
        self._observer.start()

    def stop(self):
        self._observer.stop()
        self._observer.join()


class FileTreeView(BaseTreeView):
    def __init__(self, parent_container, root_path: str = "", single_selection=False, expand_root_node: bool = True, *args, **kwargs):
        super().__init__(parent_container, single_selection, *args, **kwargs)
        self.root_path = root_path
        self.directory_watcher = None
        if root_path:
            self.create_tree(expand_root_node)

    def create_tree(self, expand_root_node=False):

        if not os.path.isdir(self.root_path):
            raise ValueError("The specified root path must be a directory.")

        if self.root_node is not None:
            raise ValueError("The root node already exists. call destroy_tree() before creating a new tree.")

        self.root_node = FolderNode(self, parent_node=None, parent_container=self, node_text=os.path.basename(self.root_path), data=self.root_path)
        if expand_root_node:
            self.root_node.expand()
        self.start_watching()

    def start_watching(self):
        if self.directory_watcher:
            self.directory_watcher.stop()

        self.directory_watcher = DirectoryWatcher(self.root_path, self.on_created, self.on_deleted, self.on_moved)
        self.directory_watcher.start()

    def on_created(self, event):
        self.after(100, self.handle_creation, event)

    def on_deleted(self, event):
        self.after(100, self.handle_deletion, event)

    def on_moved(self, event):
        self.after(100, self.handle_move, event)

    def handle_creation(self, event):
        parent_path = os.path.dirname(event.src_path)
        parent_node = self.find_node_by_path(parent_path)
        if parent_node and os.path.exists(event.src_path):
            new_node = FolderNode(self, parent_node, parent_node.child_nodes_container, os.path.basename(event.src_path), data=event.src_path) if event.is_directory else FileNode(self, parent_node, parent_node.child_nodes_container, os.path.basename(event.src_path), data=event.src_path)
            new_node.show()

    def handle_deletion(self, event):
        node_to_delete = self.find_node_by_path(event.src_path)
        if node_to_delete:
            if isinstance(node_to_delete, FolderNode):
                # TODO: handle deletion of child nodes
                # TODO: move to node itself for easier cleanup
                pass
            self.deselect_node(node_to_delete)
            node_to_delete.cleanup()
            node_to_delete.parent_node.remove_child(node_to_delete)
            self.remove_node(node_to_delete)

    def handle_move(self, event):
        old_path = event.src_path
        new_path = event.dest_path
        node = self.find_node_by_path(old_path)
        if node:
            node.set_data(new_path)
            node.rename(os.path.basename(new_path))

    def find_node_by_path(self, path):
        return next((node for node in self.nodes if node.data == path), None)

    def recreate_tree(self, expand_root_node=False):
        if self.directory_watcher:
            self.directory_watcher.stop()
            self.directory_watcher = None
        self.destroy_tree()
        self.create_tree(expand_root_node)
