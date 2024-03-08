# GuiFramework/gui/gui_manager/widget_builder/abstract_builder.py

import abc


class AbstractBuilder(abc.ABC):
    @property
    @abc.abstractmethod
    def widget_type(self):
        pass

    @abc.abstractmethod
    def create_widget(self, master, widget_properties):
        pass

    @abc.abstractmethod
    def apply_packing(self, widget, packing_properties):
        pass

    @abc.abstractmethod
    def apply_grid_configuration(self, widget, grid_configuration):
        pass