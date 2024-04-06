from typing import Any

from .base_node import BaseNode


class BaseFileNode(BaseNode):

    def __init__(self, tree_view_instance, parent_node, parent_container, data: Any = None, **kwargs):
        file_selectable = tree_view_instance.file_selectable
        super().__init__(tree_view_instance, parent_node, parent_container, data, selectable=file_selectable, **kwargs)
