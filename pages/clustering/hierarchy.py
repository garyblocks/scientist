import tkinter as tk
import pandas as pd
import pylab
import matplotlib
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.manifold import TSNE
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
        self.axes = []
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
        # plot the clusters
        Button(self, "matrix", 1, 0, 2, lambda: self.plot_matrix())
        Button(self, "t-SNE", 0, 2, 2, lambda: self.plot_tsne())
        Button(self, "radviz", 0, 4, 2, lambda: self.plot_radvis())
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
        self.X = X
        self.Z = Z
        self.plot_dendro()

    def plot_dendro(self):
        self.plot.clear()
        # calculate full dendrogram# calcul
        self.plot.ax.set_title('Hierarchical Clustering Dendrogram')
        # plt.xlabel('sample index')
        # plt.ylabel('distance')
        matplotlib.rcParams['lines.linewidth'] = 0.5
        dendrogram(self.Z, leaf_rotation=90.,  # rotates the x axis labels
                   ax=self.plot.ax)
        matplotlib.rcParams['lines.linewidth'] = 1.5
        self.plot.canvas.draw()

    def plot_matrix(self):
        self.plot.clear()
        fig = self.plot.fig
        axdendro = fig.add_axes([0.1, 0.1, 0.2, 0.8])
        matplotlib.rcParams['lines.linewidth'] = 0.3
        dg = dendrogram(self.Z, orientation='left', ax=axdendro)
        matplotlib.rcParams['lines.linewidth'] = 1.5
        axdendro.set_xticks([])
        axdendro.set_yticks([])

        # Plot distance matrix.
        axmatrix = fig.add_axes([0.3, 0.1, 0.6, 0.8])
        index = dg['leaves']
        D = self.X[index, :]
        im = axmatrix.matshow(D, aspect='auto', origin='lower')
        axmatrix.set_xticks([])
        axmatrix.set_yticks([])

        # Plot colorbar.
        axcolor = fig.add_axes([0.91, 0.1, 0.02, 0.8])
        pylab.colorbar(im, cax=axcolor)
        self.axes = [axdendro, axmatrix, axcolor]
        self.plot.canvas.draw()

    def plot_radvis(self):
        cls = self.entry_col_name.get()
        feat_list = list(self.select.tags) + [cls]
        tmp = self.df[feat_list]
        self.plot.clear()
        self.plot.plot_radviz(tmp, cls)

    def plot_tsne(self):
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        cls = self.entry_col_name.get()
        y = self.df[cls].values
        X_embedded = TSNE().fit_transform(X)
        self.plot.clear()
        self.plot.plot_2d_scatter(X_embedded, y)

    def clear(self):
        self.select.clear()
        self.plot.clear()
        for ax in self.axes:
            ax.remove()
