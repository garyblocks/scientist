import tkinter as tk
import matplotlib
import numpy as np
import matplotlib.patches as mpatches
import itertools as it
import pylab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # noqa
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
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

    def switch_to_3d_ax(self):
        self.ax = Axes3D(self.fig, rect=[0, 0, .95, 1], elev=48, azim=134)

    def add_color_bar(self, mappable=None, label=""):
        if not mappable:
            mappable = self.ax
        cax = self.fig.add_axes([0.91, 0.11, 0.02, 0.77])
        cbar = pylab.colorbar(ax=self.ax, cax=cax, mappable=mappable)
        cbar.ax.tick_params(labelsize=5, pad=-2)
        cbar.set_label(label, rotation=270, labelpad=4, size=8)

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

    def plot_profile(self, X, y, names):
        # spilt the data into clusters by class label
        clusters = {i: [] for i in set(y)}
        for i in range(len(y)):
            clusters[y[i]].append(i)
        # choose subplot
        # custom x ticks
        x = [i for i in range(len(names))]
        self.ax.set_xticks(x, names)
        # rotate xticks
        for label in self.ax.get_xmajorticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment("right")
            # Plot first center
            # ax.plot(x,centers.tolist()[j],color='red')
            # plot data points in a cluster
            patches = []
            colors = it.cycle(plt.cm.rainbow(np.linspace(0, 1, len(clusters))))
            for cls, clr in zip(clusters, colors):
                patches.append(mpatches.Patch(color=clr, label=cls))
                for i in clusters[cls]:
                    self.ax.plot(x, X[i], color=clr, alpha=0.02, linewidth=2.0)
            # set ylabel and title
            self.ax.set_title('profile for each individual')
        self.ax.legend(handles=patches)
        self.canvas.draw()
