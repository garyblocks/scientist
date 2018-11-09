import tkinter as tk
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from libs.plot import Plot
from libs.button import Button
from libs.select import Select
from libs.font import TITLE, LABEL


class ClusteringKmeansPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.plot = None
        self.init_frame()

    def reload(self):
        self.df = self.controller.DF
        self.ctrl_pane.df = self.df
        self.ctrl_pane.reload()

    def init_frame(self):
        # split out left panel
        vertical_split = tk.PanedWindow(self)
        vertical_split.pack(fill=tk.BOTH, expand=1)
        self.df = self.controller.DF
        # add control pane
        ctrl_pane = KmeansControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        # add plot canvas
        plot = Plot(vertical_split)
        self.plot = plot
        self.ctrl_pane.plot = self.plot
        vertical_split.add(plot)
        self.vertical = vertical_split


class KmeansControlPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.plot = self.controller.plot
        self.select = None
        self.row = 0
        self.init_frame()

    def reload(self):
        self.row = 0
        self.init_frame()

    def init_frame(self):
        # title
        text = tk.Label(
            self, text="Kmeans", font=TITLE, bg='#F3F3F3',
            width=25
        )
        text.grid(row=self.row, column=0, columnspan=6)

        # select feature
        select = Select(self, self.df.columns.values.tolist())
        select.grid(row=self.row, column=0, columnspan=6)
        self.select = select

        # set number of clusters
        self.row += 1
        label_set_k = tk.Label(self, text="number of clusters",
                               font=LABEL, bg='#F3F3F3')
        label_set_k.grid(row=self.row, column=0, columnspan=3)
        entry_k = tk.Entry(self, highlightbackground='#F3F3F3')
        entry_k.grid(row=self.row, column=3, columnspan=2)
        self.entry_k = entry_k

        # set name of columns
        self.row += 1
        label_set_col_name = tk.Label(
            self, text="name of column",
            font=LABEL, bg='#F3F3F3'
        )
        label_set_col_name.grid(row=self.row, column=0, columnspan=3)
        entry_col_name = tk.Entry(self, highlightbackground="#F3F3F3")
        entry_col_name.grid(row=self.row, column=3, columnspan=2)
        self.entry_col_name = entry_col_name

        # run the clustering algorithm
        Button(self, "cluster", 1, 0, 6, lambda: self.kmeans())
        # run the clustering algorithm
        Button(self, "radviz", 1, 0, 6, lambda: self.plot_radvis())
        # clear plot
        Button(self, "clear", 1, 0, 6, lambda: self.clear())

    def kmeans(self):
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        k = int(self.entry_k.get())
        model = MiniBatchKMeans(
            init='k-means++', n_clusters=k, batch_size=45,
            n_init=10, max_no_improvement=10, verbose=0
        )
        model.fit(X)
        self.df[self.entry_col_name.get()] = pd.Series(
            model.labels_, index=self.df.index
        )
        self.plot_2d_scatter(X[:, :2], model.labels_)

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
            col = self.plot.ax.scatter(
                col1, col2, label=label, alpha=0.5
            )
            colors.append(col)
            labels.append(label)
        self.plot.ax.set_title('clusters')

        # make nice plotting
        self.plot.ax.spines['top'].set_visible(False)
        self.plot.ax.spines['right'].set_visible(False)
        self.plot.ax.get_xaxis().tick_bottom()
        self.plot.ax.get_yaxis().tick_left()
        self.plot.ax.spines['left'].set_position(('outward', 10))
        self.plot.ax.spines['bottom'].set_position(('outward', 10))
        self.plot.ax.legend(
            colors, labels, loc='best', labelspacing=0
        )
        self.plot.canvas.draw()

    def plot_radvis(self):
        cls = self.entry_col_name.get()
        feat_list = list(self.select.tags) + [cls]
        tmp = self.df[feat_list]
        self.plot.clear()
        self.plot.plot_radviz(tmp, cls)

    def clear(self):
        self.select.clear()
        self.plot.clear()
