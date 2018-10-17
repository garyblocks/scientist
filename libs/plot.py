import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # noqa
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib
matplotlib.use("TkAgg")
style.use("ggplot")


class Plot(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # create matplotlib plot
        self.fig = Figure(figsize=(5, 4), dpi=150)
        self.ax = self.fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = canvas
        self.toolbar = toolbar

    def clear(self):
        self.ax.clear()
        self.canvas.draw()
