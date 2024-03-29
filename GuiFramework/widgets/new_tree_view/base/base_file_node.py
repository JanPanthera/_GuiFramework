from typing import Any

from .base_node import BaseNode


class BaseFileNode(BaseNode):

    def __init__(self, tree_view_instance, parent_node, parent_container, data: Any = None, **kwargs):
        super().__init__(tree_view_instance, parent_node, parent_container, data, **kwargs)

    def on_select(self):
        self.tree_view_instance.selected_nodes["file"].append(self)

    def on_deselect(self):
        self.tree_view_instance.selected_nodes["file"].remove(self)
