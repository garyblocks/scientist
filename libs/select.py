import tkinter as tk
from libs.button import Button
from libs.font import LABEL


class Select(tk.Frame):

    def __init__(self, master, options=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.options = options
        self.tags = set()
        self.label = None
        self.choice = None
        self.init_frame()

    def reload(self):
        self.init_frame()

    def init_frame(self):
        self.master.row += 1
        label = tk.Label(self, text="features: no feature",
                         font=LABEL, bg='#F3F3F3')
        label.grid(row=self.master.row, column=0, columnspan=6)
        self.label = label
        self.master.row += 1
        choice = tk.StringVar(self)
        if not self.options:
            self.options = ['']
        # set default
        choice.set(self.options[0] if self.options else '')
        # create selection menu
        menu = tk.OptionMenu(self, choice, *self.options)
        menu.config(bg="#F3F3F3")
        menu.grid(row=self.master.row, column=0, columnspan=4)
        self.choice = choice
        Button(self.master, "add", 0, 4, 2, lambda: self.add())

    def add(self):
        new = self.choice.get()
        self.tags.add(new)
        self.label['text'] = 'features: ' + ','.join(list(self.tags))

    def clear(self):
        self.label['text'] = 'features: no feature'
        self.tags = set()
