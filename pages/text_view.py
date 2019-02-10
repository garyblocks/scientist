import tkinter as tk
from libs.font import TITLE
from libs.book import Book
# from libs.button import Button


class TextViewPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.book = None
        self.init_frame()

    def reload(self):
        self.s = self.controller.STR
        self.ctrl_pane.s = self.s
        book = Book(self.vertical, string=self.s)
        self.book = book
        self.vertical.add(self.book)
        self.ctrl_pane.reload()

    def init_frame(self):
        # split out left panel
        vertical_split = tk.PanedWindow(self)
        vertical_split.pack(fill=tk.BOTH, expand=1)
        self.s = self.controller.STR
        # add control pane
        ctrl_pane = ViewControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        book = Book(vertical_split, string=self.s)
        self.book = book
        vertical_split.add(book)
        self.vertical = vertical_split


class ViewControlPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.s = self.controller.s
        self.book = self.controller.book
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
