import tkinter as tk
from libs.font import LABEL


class Alert():

    def warn(self, msg):
        pop_up_win = tk.Toplevel()
        pop_up_win.wm_title("WARNING")

        label = tk.Label(
            pop_up_win, text=msg,
            font=LABEL, bg='#F3F3F3'
        )
        label.grid(row=0)
