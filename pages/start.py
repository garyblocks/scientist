import tkinter as tk
from libs.font import LABEL


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
            font=LABEL,
            bg='#F3F3F3',
            pady=15
        )
        label.pack()

        import_csv_btn = tk.Button(
            self,
            text="Import CSV",
            command=lambda: self.controller.import_csv(),
            highlightbackground='#F3F3F3',
            pady=15
        )
        import_csv_btn.pack()

        import_txt_btn = tk.Button(
            self,
            text="Import TXT",
            command=lambda: self.controller.import_txt(),
            highlightbackground='#F3F3F3',
            pady=15
        )
        import_txt_btn.pack()
