import tkinter as tk
from abc import ABC, abstractmethod
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from libs.plot import Plot
from libs.button import Button
from libs.select import Select
from libs.font import TITLE, SECTION, LABEL


class BaseClusteringPage(tk.Frame, ABC):

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
        ctrl_pane = BaseControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        # add plot canvas
        plot = Plot(vertical_split)
        self.plot = plot
        self.ctrl_pane.plot = self.plot
        vertical_split.add(plot)
        self.vertical = vertical_split


class BaseControlPane(tk.Frame):

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
        # clear plot
        Button(self, "clear", 1, 0, 6, lambda: self.clear())

    def cluster(self):
        try:
            self.run()
        except ValueError as e:
            self.alert_pop_up(str(e))

    def alert_pop_up(self, msg):
        pop_up_win = tk.Toplevel()
        pop_up_win.wm_title("Alert")

        label = tk.Label(
            pop_up_win, text=msg,
            font=SECTION, bg='#EEDFDE',
            fg='#A93E2F', padx=20, pady=20
        )
        label.grid(row=0, column=0)
    
    @abstractmethod
    def run(self):
        pass

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

    def plot_profile(self):
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        cls = self.entry_col_name.get()
        y = self.df[cls].values
        self.plot.clear()
        self.plot.plot_profile(X, y, feat_list)

    def clear(self):
        self.select.clear()
        self.plot.clear()
