import tkinter as tk
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import AffinityPropagation
from libs.plot import Plot
from libs.button import Button
from libs.select import Select
from libs.font import TITLE, SECTION, LABEL


class ClusteringApPage(tk.Frame):

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
        ctrl_pane = ApControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        # add plot canvas
        plot = Plot(vertical_split)
        self.plot = plot
        self.ctrl_pane.plot = self.plot
        vertical_split.add(plot)
        self.vertical = vertical_split


class ApControlPane(tk.Frame):

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
            self, text="Affinity Propagation", font=TITLE, bg='#F3F3F3',
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
        Button(self, "cluster", 1, 0, 6, lambda: self.ap())

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
        # clear plot
        Button(self, "clear", 1, 0, 6, lambda: self.clear())

    def ap(self):
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        model = AffinityPropagation(preference=-50)
        model.fit(X)
        self.df[self.entry_col_name.get()] = pd.Series(
            model.labels_, index=self.df.index
        )
        # default is plotting first features
        self.plot.plot_2d_scatter(X[:, :2], model.labels_)

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

    def plot_pca(self):
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        cls = self.entry_col_name.get()
        y = self.df[cls].values
        X_embedded = PCA(n_components=2).fit_transform(X)
        self.plot.clear()
        self.plot.plot_2d_scatter(X_embedded, y)

    def clear(self):
        self.select.clear()
        self.plot.clear()
