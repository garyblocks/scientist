import tkinter as tk
from libs.font import TITLE
# from libs.button import Button


class TextViewPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.init_frame()

    def reload(self):
        self.s = self.controller.STR
        text = tk.Label(self.vertical, text=self.s)
        text.pack()
        self.text = text
        self.vertical.add(self.text)
        self.ctrl_pane.reload()

    def init_frame(self):
        # split out left panel
        vertical_split = tk.PanedWindow(self)
        vertical_split.pack(fill=tk.BOTH, expand=1)
        self.s = self.controller.STR
        text = tk.Label(vertical_split, text=self.s)
        text.pack()
        self.text = text
        vertical_split.add(self.text)
        ctrl_pane = ViewControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        self.vertical = vertical_split


class ViewControlPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.s = self.controller.s
        self.text = self.controller.text
        self.row = 0
        self.init_frame()

    def reload(self):
        self.s = self.controller.s
        self.row = 0
        self.init_frame()

    def init_frame(self):
        title_table = tk.Label(
            self, text="Text View", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_table.grid(row=self.row, column=0, columnspan=6)

        # display random rows
        # Button(self, "word cloud", 1, 0, 2, lambda: self.word_cloud())
