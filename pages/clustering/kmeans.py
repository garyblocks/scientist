import tkinter as tk
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from libs.button import Button
from libs.select import Select
from libs.plot import Plot
from libs.font import TITLE, SECTION, LABEL
from pages.clustering.base import BaseClusteringPage
from pages.clustering.base import BaseControlPane


class ClusteringKmeansPage(BaseClusteringPage):

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


class KmeansControlPane(BaseControlPane):

    def init_frame(self):
        # title
        text = tk.Label(
            self, text="Kmeans", font=TITLE, bg='#F3F3F3', width=30
        )
        text.grid(row=self.row, column=0, columnspan=6)

        # section setting
        self.row += 1
        label_setting = tk.Label(
            self, text="settings", font=SECTION, bg='#F3F3F3',
        )
        label_setting.grid(row=self.row, column=0, columnspan=6)

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
            self, text="name of the new column",
            font=LABEL, bg='#F3F3F3'
        )
        label_set_col_name.grid(row=self.row, column=0, columnspan=3)
        entry_col_name = tk.Entry(self, highlightbackground="#F3F3F3")
        entry_col_name.grid(row=self.row, column=3, columnspan=2)
        self.entry_col_name = entry_col_name

        # run the clustering algorithm
        Button(self, "cluster", 1, 0, 6, lambda: self.cluster())

        # visualization
        self.row += 1
        label_setting = tk.Label(
            self, text="visualization", font=SECTION, bg='#F3F3F3'
        )
        label_setting.grid(row=self.row, column=0, columnspan=6)

        # plot the clusters
        Button(self, "t-SNE", 1, 0, 2, lambda: self.plot_tsne())
        Button(self, "radviz", 0, 2, 2, lambda: self.plot_radvis())
        Button(self, "PCA", 0, 4, 2, lambda: self.plot_pca())
        Button(self, "profile", 1, 0, 2, lambda: self.plot_profile())

        # clear plot
        Button(self, "clear", 1, 0, 6, lambda: self.clear())

    def run(self):
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
        # default is plotting first features
        self.plot.plot_2d_scatter(X[:, :2], model.labels_)
