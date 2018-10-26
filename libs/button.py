import tkinter as tk


class Button(tk.Button):

    def __init__(self, master, text, row, col, span, command):
        self.master = master
        self.master.row += row
        super().__init__(
            self.master,
            text=text,
            highlightbackground='#F3F3F3',
            padx=15,
            pady=10,
            command=command)
        self.grid(
            row=self.master.row, column=col, columnspan=span, padx=10, pady=10)
