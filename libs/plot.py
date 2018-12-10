import tkinter as tk
import matplotlib
import numpy as np
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

    def plot_2d_scatter(self, X, y):
        # plot first two columns
        colors, labels = [], []
        C = set(y)
        for ci in C:
            label = "Class " + str(ci)
            if X.shape[1] > 1:
                col1, col2 = X[y == ci, 0], X[y == ci, 1]
            else:
                col1 = X[y == ci, 0]
                col2 = np.zeros(col1.shape)
            col = self.ax.scatter(
                col1, col2, label=label, alpha=0.5
            )
            colors.append(col)
            labels.append(label)
        self.ax.set_title('clusters')

        # make nice plotting
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()
        self.ax.spines['left'].set_position(('outward', 10))
        self.ax.spines['bottom'].set_position(('outward', 10))
        self.ax.legend(
            colors, labels, loc='best', labelspacing=0
        )
        self.canvas.draw()
