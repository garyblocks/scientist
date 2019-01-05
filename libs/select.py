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
        self.cells = []
        self.init_frame()

    def reload(self):
        self.init_frame()

    def init_frame(self):
        self.master.row += 1
        Button(self.master, "select features", 0, 0, 6, lambda: self.pick())

    def pick(self):
        pop_up_win = tk.Toplevel()
        pop_up_win.wm_title("Features")

        label = tk.Label(
            pop_up_win, text="features",
            font=LABEL, bg='#F3F3F3'
        )
        label.grid(row=0)
        self.cells = []
        for i, op in enumerate(self.options):
            label = tk.Label(pop_up_win, text=op)
            label.grid(row=i+1)
            label.bind("<Button-1>", lambda e, i=i, op=op: self.add(i, op))
            self.cells.append(label)
            if op in self.tags:
                self.cells[i].config(bg="red")
        self.pop_up_win = pop_up_win

    def add(self, i, op):
        if op in self.tags:
            # unselect
            self.tags.remove(op)
            self.cells[i].config(bg="white")
        else:
            # select
            self.tags.add(op)
            self.cells[i].config(bg="red")

    def clear(self):
        self.tags = set()
