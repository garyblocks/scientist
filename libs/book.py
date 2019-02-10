import tkinter as tk
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


class InnerBook(tk.Frame):

    def __init__(self, master, string):
        tk.Frame.__init__(self, master)
        self.master = master
        self.string = string
        self.text = None
        self.create_view()

    def create_view(self):
        text = tk.Label(self, text=self.string)
        text.grid(row=0, column=0)
        self.text = text


class Book(tk.Frame):

    def __init__(self, master, string, *args, **kw):
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
        self.book = None
        self.create_book(string)

    def create_book(self, string):
        if self.book:
            self.book.destroy()
        inner_book = InnerBook(self.canvas, string)
        inner_book.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # put content on canvas
        self.canvas.create_window(0, 0, anchor=tk.NW, window=inner_book)
        inner_book.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.book = inner_book
