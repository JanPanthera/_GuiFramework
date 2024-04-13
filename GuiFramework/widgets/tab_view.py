# GuiFramework/widgets/tab_view.py

import uuid
from typing import Optional, List, Tuple
from customtkinter import CTkFrame, CTkButton

class Tab:
    def __init__(self, frame: CTkFrame, title: str, id: Optional[str] = None) -> None:
        self.id: str = id if id else str(uuid.uuid4())
        self.title: str = title
        self.frame: CTkFrame = frame
        self.button: Optional[CTkButton] = None

class TabView(CTkFrame):
    def __init__(self, parent_container: CTkFrame, tabs: Optional[List[Tuple[CTkFrame, str]]] = None) -> None:
        super().__init__(parent_container)
        self.tabs: dict = {}

        self._setup_containers()
        self._configure_grid()

        if tabs:
            for frame, title in tabs:
                self.add_tab(frame, title)

    def _setup_containers(self) -> None:
        self.navigation_container = CTkFrame(self, fg_color="transparent", bg_color="transparent")
        self.navigation_container.grid(row=0, column=1, sticky="nsew")

        self.tab_container = CTkFrame(self, fg_color="transparent", bg_color="transparent")
        self.tab_container.grid(row=1, column=0, columnspan=3, sticky="nsew")

    def _configure_grid(self) -> None:
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

    def add_tab(self, frame: CTkFrame, title: str, id: Optional[str] = None) -> str:
        new_tab = Tab(frame, title, id)
        self.tabs[new_tab.id] = new_tab
        self._create_tab_button(new_tab)
        return new_tab.id

    def remove_tab(self, tab_id: str) -> None:
        tab = self.tabs.get(tab_id)
        if tab:
            if tab.button:
                tab.button.destroy()
            tab.frame.destroy()
            del self.tabs[tab_id]
        else:
            raise ValueError(f"No tab with ID {tab_id} found to remove.")

    def show_tab(self, tab_id: str) -> None:
        tab_to_show = self.tabs.get(tab_id)
        if tab_to_show:
            for tab in self.tabs.values():
                if tab.id != tab_id:
                    tab.frame.grid_remove()
            tab_to_show.frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        else:
            raise ValueError(f"No tab with ID {tab_id} found to show.")

    def hide_tab(self, tab_id: str) -> None:
        tab = self.tabs.get(tab_id)
        if tab:
            tab.frame.grid_remove()
        else:
            raise ValueError(f"No tab with ID {tab_id} found to hide.")

    def rename_tab(self, tab_id: str, new_title: str) -> None:
        tab = self.tabs.get(tab_id)
        if tab:
            if tab.button:
                tab.button.configure(text=new_title)
            tab.title = new_title
        else:
            raise ValueError(f"No tab with ID {tab_id} found to rename.")

    def get_tab_id(self, frame: CTkFrame) -> str:
        for tab in self.tabs.values():
            if tab.frame == frame:
                return tab.id
        raise ValueError("No tab found with the given frame.")

    def _create_tab_button(self, tab: Tab) -> None:
        btn = CTkButton(self.navigation_container, text=tab.title, command=lambda: self.show_tab(tab.id))
        btn.pack(side="left", fill="none", expand=False)
        tab.button = btn
