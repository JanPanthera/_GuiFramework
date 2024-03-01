# tab_view.py

from customtkinter import CTkFrame, CTkButton


class TabView(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.window = master

        self.pack(fill='both', expand=True)

        # Vertical expansion weights
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        self.btn_frame = CTkFrame(self, fg_color="transparent", bg_color="transparent")
        self.btn_frame.grid(row=0, column=1, sticky="nsew")

        self.btn_to_frame = {}
        self.title_to_btn = {}

    def show(self):
        self.pack(fill='both', expand=True)

    def hide(self):
        self.pack_forget()

    def add_tab(self, frame, title):
        self._create_tab_button(frame, title)
        frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.hide_tab(frame)

    def remove_tab(self, frame):
        for btn, frm in self.btn_to_frame.items():
            if frm == frame:
                del self.title_to_btn[btn.cget('text')]
                btn.destroy()
                del self.btn_to_frame[btn]
                break

    def show_tab(self, frame):
        for frm in self.btn_to_frame.values():
            frm.grid_remove()
        frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

    def hide_tab(self, frame):
        frame.grid_remove()

    def rename_tab(self, old_title, new_title):
        if old_title in self.title_to_btn:
            btn = self.title_to_btn[old_title]
            btn.configure(text=new_title)
            del self.title_to_btn[old_title]
            self.title_to_btn[new_title] = btn

    def _create_tab_button(self, frame, title):
        btn = CTkButton(self.btn_frame, text=title, command=lambda: self.show_tab(frame))
        btn.pack(side='left', fill='none', expand=False)
        self.btn_to_frame[btn] = frame
        self.title_to_btn[title] = btn