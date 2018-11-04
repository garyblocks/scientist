import tkinter as tk
import numpy as np
import decimal
BOLD = 'Helvetica 14 bold'
FONT = 'Helvetica 14'


class AutoScrollbar(tk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError

    def place(self, **kw):
        raise tk.TclError


class InnerTable(tk.Frame):

    def __init__(self, master, dataframe):
        tk.Frame.__init__(self, master)
        self.master = master
        self.dataframe = dataframe
        num_of_rows, self.num_of_cols = dataframe.shape
        self.start_idx = 0
        self.current_view_id = 0
        self.next_view_id = 1 if num_of_rows > 100 else 0
        self.num_of_rows = min(num_of_rows, 100)
        self.create_view()

    def create_view(self):
        # create body
        df = self.dataframe[self.start_idx: self.start_idx + 100]
        data = df.values
        header = df.columns.values
        indices = df.index.values

        # create header
        for j in range(1, self.num_of_cols + 1):
            cell = tk.Label(
                self,
                height=2,
                padx=3,
                text=header[j - 1],
                font=BOLD
            )
            cell.grid(row=0, column=j)

        # 0 for header
        for i in range(1, self.num_of_rows + 1):
            # show index
            bg_color = '#FFFFFF' if i % 2 else '#F5F5F5'
            cell = tk.Label(
                self,
                height=2,
                padx=3,
                text=str(indices[i - 1]),
                bg=bg_color,
                font=BOLD
            )
            cell.grid(row=i, column=0)
            for j in range(1, self.num_of_cols + 1):
                number = str(data[i-1, j-1])
                if number.replace('.', '').replace('-', '').isdecimal(
                ) and decimal.Decimal(number).as_tuple().exponent < -4:
                    # round number to 4 decimal places
                    number = str(round(float(number), 4))

                cell = tk.Label(
                    self,
                    height=2,
                    padx=3,
                    text=number,
                    bg=bg_color,
                    font=FONT
                )
                cell.grid(row=i, column=j)


class Table(tk.Frame):

    def __init__(self, master, dataframe, *args, **kw):
        tk.Frame.__init__(self, master, *args, **kw)

        # create scrollbars
        vscrollbar = AutoScrollbar(self)
        vscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        hscrollbar = AutoScrollbar(self, orient=tk.HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)

        # create a canvas to scroll on
        canvas = tk.Canvas(
            self, bd=0, highlightthickness=0,
            yscrollcommand=vscrollbar.set,
            xscrollcommand=hscrollbar.set
        )
        canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # reset the view
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        # make the canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.canvas = canvas

        # create content
        self.views = self.split_df(dataframe, 100)
        self.current_view_id = 0
        self.table = None
        self.create_table(self.views[self.current_view_id])

    def create_table(self, dataframe):
        if self.table:
            self.table.destroy()
        inner_table = InnerTable(self.canvas, dataframe)
        inner_table.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # put content on canvas
        self.canvas.create_window(0, 0, anchor=tk.NW, window=inner_table)
        inner_table.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.table = inner_table

    @staticmethod
    def split_df(df, chunk_size):
        nrows = df.shape[0]
        indices = range(1 * chunk_size, (nrows // chunk_size + 1) * chunk_size, chunk_size)  # noqa
        return np.split(df, indices)

    def next_view(self):
        if self.current_view_id < len(self.views) - 1:
            self.current_view_id += 1
            self.create_table(self.views[self.current_view_id])

    def prev_view(self):
        if self.current_view_id > 0:
            self.current_view_id -= 1
            self.create_table(self.views[self.current_view_id])
