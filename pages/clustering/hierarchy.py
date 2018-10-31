import tkinter as tk
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from libs.plot import Plot
from libs.button import Button
from libs.select import Select
from libs.font import TITLE, LABEL


class ClusteringHierarchyPage(tk.Frame):

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
        ctrl_pane = HierarchyControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        # add plot canvas
        plot = Plot(vertical_split)
        self.plot = plot
        self.ctrl_pane.plot = self.plot
        vertical_split.add(plot)
        self.vertical = vertical_split


class HierarchyControlPane(tk.Frame):

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
            self, text="Hierarchy", font=TITLE, bg='#F3F3F3',
            width=25
        )
        text.grid(row=self.row, column=0, columnspan=6)

        # select features
        select = Select(self, self.df.columns.values.tolist())
        select.grid(row=self.row, column=0, columnspan=6)
        self.select = select

        # set linkage
        self.row += 1
        label_link = tk.Label(self, text="linkage",
                              font=LABEL, bg='#F3F3F3')
        label_link.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        link = tk.StringVar(self)
        links = [
            'ward', 'single', 'complete', 'average', 'weighted', 'centroid',
            'median'
        ]
        link.set('ward')
        link_menu = tk.OptionMenu(self, link, *links)
        link_menu.config(bg="#F3F3F3")
        link_menu.grid(row=self.row, column=0, columnspan=6)
        self.link = link

        # set distance
        self.row += 1
        label_dist = tk.Label(self, text="distance",
                              font=LABEL, bg='#F3F3F3')
        label_dist.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        dist = tk.StringVar(self)
        dists = [
            'euclidean', 'minkowski', 'cityblock', 'seuclidean', 'sqeuclidean',
            'cosine', 'correlation', 'hamming', 'jaccard', 'chebyshev'
        ]
        dist.set('euclidean')
        dist_menu = tk.OptionMenu(self, dist, *dists)
        dist_menu.config(bg="#F3F3F3")
        dist_menu.grid(row=self.row, column=0, columnspan=6)
        self.dist = dist

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
        Button(self, "cluster", 1, 0, 6, lambda: self.hierarchy())
        # clear plot
        Button(self, "clear", 1, 0, 6, lambda: self.clear())

    def hierarchy(self):
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        k = int(self.entry_k.get())
        method = self.link.get()
        metric = self.dist.get()
        # generate the linkage matrix
        Z = linkage(X, method=method, metric=metric)
        clusters = fcluster(Z, k, criterion='maxclust')
        self.df[self.entry_col_name.get()] = pd.Series(
            clusters, index=self.df.index
        )
        self.plot_dendro(Z)

    def plot_dendro(self, Z):
        # calculate full dendrogram# calcul
        # self.plot.ax.title('Hierarchical Clustering Dendrogram')
        # self.plot.ax.xlabel('sample index')
        # self.plot.ax.ylabel('distance')
        dendrogram(Z, leaf_rotation=90.,  # rotates the x axis labels
                   ax=self.plot.ax)
        self.plot.canvas.draw()

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

    def clear(self):
        self.features = set()
        self.label_feats['text'] = 'features: no feature'
        self.plot.clear()
