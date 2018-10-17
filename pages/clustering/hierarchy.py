import tkinter as tk
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from libs.plot import Plot
from libs.font import TITLE, SECTION, LABEL


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
        self.ctrl_pane.init_frame()

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
        self.features = set()
        self.init_frame()

    def reload(self):
        self.init_frame()

    def init_frame(self):
        # title
        row = 0
        text = tk.Label(
            self, text="Clustering", font=TITLE, bg='#F3F3F3',
            width=25
        )
        text.grid(row=row, column=0, columnspan=3)

        # settings
        row += 1
        label_sec_cluster = tk.Label(self, text="Settings",
                                     font=SECTION, bg='#F3F3F3')
        label_sec_cluster.grid(row=row, column=0, columnspan=3)

        # select features to cluster on
        row += 1
        label_feats = tk.Label(self, text="features: no feature",
                               font=LABEL, bg='#F3F3F3')
        label_feats.grid(row=row, column=0, columnspan=3)
        self.label_feats = label_feats
        row += 1
        chosen = tk.StringVar(self)
        choices = self.df.columns.values.tolist()
        if not choices:
            choices = ['']
        chosen.set(choices[0] if choices else '')
        add_feat = tk.OptionMenu(self, chosen, *choices)
        add_feat.grid(row=row, column=0, columnspan=2)
        self.add_feat = chosen
        btn_add_feat = tk.Button(self, text="add", bg='#F3F3F3',
                                 padx=15, pady=10,
                                 command=lambda: self.add_feature())
        btn_add_feat.grid(row=row, column=2, columnspan=1, padx=5, pady=5)

        # set linkage
        row += 1
        label_link = tk.Label(self, text="linkage",
                              font=LABEL, bg='#F3F3F3')
        label_link.grid(row=row, column=0, columnspan=3)
        row += 1
        link = tk.StringVar(self)
        links = [
            'ward', 'single', 'complete', 'average', 'weighted', 'centroid',
            'median'
        ]
        link.set('ward')
        chose_link = tk.OptionMenu(self, link, *links)
        chose_link.grid(row=row, column=0, columnspan=3)
        self.link = link

        # set distance
        row += 1
        label_dist = tk.Label(self, text="distance",
                              font=LABEL, bg='#F3F3F3')
        label_dist.grid(row=row, column=0, columnspan=3)
        row += 1
        dist = tk.StringVar(self)
        dists = [
            'euclidean', 'minkowski', 'cityblock', 'seuclidean', 'sqeuclidean',
            'cosine', 'correlation', 'hamming', 'jaccard', 'chebyshev'
        ]
        dist.set('euclidean')
        chose_dist = tk.OptionMenu(self, dist, *dists)
        chose_dist.grid(row=row, column=0, columnspan=3)
        self.dist = dist

        # set number of clusters
        row += 1
        label_set_k = tk.Label(self, text="number of clusters",
                               font=LABEL, bg='#F3F3F3')
        label_set_k.grid(row=row, column=0, columnspan=3)
        row += 1
        entry_k = tk.Entry(self)
        entry_k.grid(row=row, column=0, columnspan=3)
        self.entry_k = entry_k

        # set name of columns
        row += 1
        label_set_col_name = tk.Label(
            self, text="name of column",
            font=LABEL, bg='#F3F3F3'
        )
        label_set_col_name.grid(row=row, column=0, columnspan=3)
        row += 1
        entry_col_name = tk.Entry(self)
        entry_col_name.grid(row=row, column=0, columnspan=3)
        self.entry_col_name = entry_col_name

        # run the clustering algorithm
        row += 1
        btn_cluster = tk.Button(self, text="cluster", bg='#F3F3F3',
                                padx=15, pady=10,
                                command=lambda: self.cluster())
        btn_cluster.grid(row=row, column=0, columnspan=3, padx=10, pady=10)

        # clear plot
        row += 1
        btn_clear = tk.Button(self, text="clear", bg='#F3F3F3',
                              padx=15, pady=10,
                              command=lambda: self.clear())
        btn_clear.grid(row=row, column=0, columnspan=3, padx=10, pady=10)

    def cluster(self):
        self.hierarchy()

    def hierarchy(self):
        feat_list = list(self.features)
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

    def add_feature(self):
        new_feature = self.add_feat.get()
        self.features.add(new_feature)
        self.label_feats['text'] = 'features: ' + ','.join(list(self.features))

    def clear(self):
        self.features = set()
        self.label_feats['text'] = 'features: no feature'
        self.plot.clear()
