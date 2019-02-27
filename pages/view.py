import tkinter as tk
import numpy as np
import math
from pandas.plotting import scatter_matrix
from libs.table import Table
from libs.plot import Plot
from libs.font import TITLE
from libs.button import Button
from libs.select import Select


class DataViewPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.table = None
        self.init_frame()

    def reload(self):
        self.df = self.controller.DF
        self.table.destroy()
        table = Table(self.vertical, self.df)
        self.table = table
        self.vertical.add(table)
        self.ctrl_pane.reload()

    def init_frame(self):
        # split out left panel
        vertical_split = tk.PanedWindow(self)
        vertical_split.pack(fill=tk.BOTH, expand=1)
        self.df = self.controller.DF
        table = Table(vertical_split, self.df)
        self.table = table
        plot = Plot(vertical_split)
        self.plot = plot
        vertical_split.add(self.table)
        ctrl_pane = ViewControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        self.vertical = vertical_split


class ViewControlPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.table = self.controller.table
        self.plot = self.controller.plot
        self.select = None
        self.row = 0
        self.init_frame()

    def reload(self):
        self.show_table()
        self.df = self.controller.df
        self.row = 0
        self.init_frame()

    def init_frame(self):
        title_table = tk.Label(
            self, text="Table View", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_table.grid(row=self.row, column=0, columnspan=6)

        # display random rows
        Button(self, "shuffle", 1, 0, 2, lambda: self.shuffle())
        Button(self, "statistics", 0, 2, 2, lambda: self.statistic())
        Button(self, "correlation", 0, 4, 2, lambda: self.correlation())

        # previous page and next page button
        Button(self, "prev", 1, 0, 2, lambda: self.prev_view())
        Button(self, "refresh", 0, 2, 2, lambda: self.controller.reload())
        Button(self, "next", 0, 4, 2, lambda: self.next_view())

        # display in plot
        self.row += 7
        title_plot = tk.Label(
            self, text="Plot View", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_plot.grid(row=self.row, column=0, columnspan=6)

        # select feature
        select = Select(self, self.df.columns.values.tolist())
        select.grid(row=self.row, column=0, columnspan=6)
        self.select = select

        # different types of plots
        Button(self, "kde", 1, 0, 2, lambda: self.plot_kde())
        Button(self, "histogram", 0, 2, 2, lambda: self.plot_hist())
        Button(self, "line chart", 0, 4, 2, lambda: self.plot_line())
        Button(self, "box", 1, 0, 2, lambda: self.plot_box())
        Button(self, "bar", 0, 2, 2, lambda: self.plot_bar())
        Button(self, "area", 0, 4, 2, lambda: self.plot_area())
        Button(self, "scatter matrix", 1, 0, 2, lambda: self.plot_scatter_matrix())
        Button(self, "hexbin", 0, 2, 2, lambda: self.plot_hexbin())
        Button(self, "3d scatter", 0, 4, 2, lambda: self.plot_3d())

        # clear plot
        Button(self, "clear", 1, 0, 6, lambda: self.clear())

        # default sizes
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=20)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=20)

    def shuffle(self):
        self.show_table()
        df = self.controller.df
        df = df.sample(frac=1).reset_index(drop=True)
        self.controller.table.destroy()
        table = Table(self.controller.vertical, df)
        self.controller.table = table
        self.controller.vertical.add(table)

    def statistic(self):
        self.show_table()
        self.controller.table.destroy()
        dataframe = self.controller.df.describe().T
        dataframe['dtype'] = self.controller.df.dtypes
        table = Table(self.controller.vertical, dataframe)
        self.controller.table = table
        self.controller.vertical.add(table)

    def correlation(self):
        self.show_table()
        self.controller.table.destroy()
        table = Table(self.controller.vertical,
                      self.controller.df.corr())
        self.controller.table = table
        self.controller.vertical.add(table)

    def prev_view(self):
        self.controller.table.prev_view()

    def next_view(self):
        self.controller.table.next_view()

    def plot_hist(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        for i in range(len(feat_list)):
            values = X[:, i]
            bins = math.ceil(len(np.unique(values)) / 3)
            self.plot.ax.hist(values, bins=bins, edgecolor='black')
        self.plot.ax.legend(
            labels=feat_list, loc='best', labelspacing=0
        )
        self.plot.canvas.draw()

    def plot_kde(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        dist = self.df[feat_list]
        dist.plot.kde(ax=self.plot.ax, legend=False)
        dist.plot.hist(density=True, ax=self.plot.ax,
                       alpha=0.7, edgecolor='black')
        self.plot.ax.set_ylabel('Probability')
        self.plot.ax.grid(axis='x')

    def plot_line(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        for i in range(len(feat_list)):
            values = X[:, i]
            self.plot.ax.plot(values)
        self.plot.ax.legend(
            labels=feat_list, loc='best', labelspacing=0
        )
        self.plot.canvas.draw()

    def plot_box(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        dist = self.df[feat_list]
        dist.plot.box(ax=self.plot.ax, legend=False)
        self.plot.ax.grid(axis='x')

    def plot_bar(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        dist = self.df[feat_list]
        dist.plot.barh(ax=self.plot.ax, legend=False)
        self.plot.ax.grid(axis='x')

    def plot_area(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        dist = self.df[feat_list]
        dist.plot.area(ax=self.plot.ax)
        self.plot.ax.grid(axis='x')

    def plot_scatter_matrix(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        tmp = self.df[feat_list]
        scatter_matrix(tmp, ax=self.plot.ax, diagonal='kde')
        self.plot.canvas.draw()

    def plot_hexbin(self):
        self.show_plot()
        feat_list = list(self.select.tags)
        dist = self.df[feat_list]
        if len(feat_list) < 2:
            return False
        elif len(feat_list) == 2:
            dist.plot.hexbin(x=feat_list[0], y=feat_list[1], ax=self.plot.ax, gridsize=20)
        else:
            dist.plot.hexbin(
                x=feat_list[0], y=feat_list[1],
                C=feat_list[2], ax=self.plot.ax, gridsize=20
            )
        self.plot.ax.grid(axis='x')

    def plot_3d(self):
        self.show_plot()
        self.plot.switch_to_3d_ax()
        feat_list = list(self.select.tags)
        X = self.df[feat_list].values
        if len(feat_list) != 3:
            return False
        self.plot.ax.scatter(X[:, 0], X[:, 1], X[:, 2])
        self.plot.ax.set_xlabel(feat_list[0])
        self.plot.ax.set_ylabel(feat_list[1])
        self.plot.ax.set_zlabel(feat_list[2])
        self.plot.canvas.draw()

    def show_plot(self):
        self.plot.clear()
        self.controller.vertical.forget(self.controller.table)
        self.controller.vertical.add(self.plot)

    def show_table(self):
        self.controller.vertical.forget(self.plot)
        self.controller.vertical.add(self.controller.table)

    def clear(self):
        self.show_plot()
        self.select.clear()
        self.plot.clear()
