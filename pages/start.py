import tkinter as tk
from libs.font import LABEL
from libs.button import Button


class StartPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.row = 0
        self.init_frame()

    def init_frame(self):
        label = tk.Label(
            self,
            text='There is no dataframe yet, please import one',
            font=LABEL
        )
        label.grid(row=self.row, column=0)
        Button(self, "Import CSV", 1, 0, 2, lambda: self.controller.import_csv())
