import tkinter as tk
import matplotlib
import pylab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # noqa
from matplotlib.figure import Figure
from matplotlib import style
from pandas.plotting import radviz
matplotlib.use("TkAgg")
style.use("ggplot")


class Plot(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.init_fig()
        self.tmp_axes = []

    def init_fig(self):
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
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.canvas.draw()
        self.toolbar.update()

    def add_color_bar(self, mappable=None):
        if not mappable:
            mappable = self.ax
        cax = self.fig.add_axes([0.91, 0.1, 0.02, 0.8])
        pylab.colorbar(ax=self.ax, cax=cax, mappable=mappable)

    def plot_radviz(self, df, cls):
        radviz(df, cls, ax=self.ax)
        self.canvas.draw()
