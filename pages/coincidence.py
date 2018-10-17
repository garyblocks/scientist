import tkinter as tk
import numpy as np
import math
from collections import Counter
from scipy.stats import hypergeom
from sklearn import preprocessing
from libs.plot import Plot
from libs.font import TITLE, SECTION, LABEL


class AnalysisCoincidencePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.DF
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
        ctrl_pane = CoincidenceControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        # add plot canvas
        plot = Plot(vertical_split)
        self.plot = plot
        self.ctrl_pane.plot = self.plot
        vertical_split.add(plot)
        self.vertical = vertical_split


class CoincidenceControlPane(tk.Frame):
    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.plot = self.controller.plot
        self.init_frame()

    def reload(self):
        self.init_frame()

    def init_frame(self):
        # title
        row = 0
        text = tk.Label(
            self, text="Coincidence", font=TITLE, bg='#F3F3F3', width=25)
        text.grid(row=row, column=0, columnspan=3)

        # settings
        row += 1
        label_set = tk.Label(self, text="Settings", font=SECTION, bg='#F3F3F3')
        label_set.grid(row=row, column=0, columnspan=3)

        # select two feature
        choices = self.df.columns.values.tolist()
        if not choices:
            choices = ['']
        row += 1
        label_feat_1 = tk.Label(
            self, text="select feature 1", font=LABEL, bg='#F3F3F3')
        label_feat_1.grid(row=row, column=0, columnspan=1)
        chosen_1 = tk.StringVar(self)
        chosen_1.set(choices[0] if choices else '')
        feat_1 = tk.OptionMenu(self, chosen_1, *choices)
        feat_1.grid(row=row, column=1, columnspan=2)
        self.feat_1 = chosen_1
        row += 1
        label_feat_2 = tk.Label(
            self, text="select feature 2", font=LABEL, bg='#F3F3F3')
        label_feat_2.grid(row=row, column=0, columnspan=1)
        chosen_2 = tk.StringVar(self)
        chosen_2.set(choices[0] if choices else '')
        feat_2 = tk.OptionMenu(self, chosen_2, *choices)
        feat_2.grid(row=row, column=1, columnspan=2)
        self.feat_2 = chosen_2

        # run the coincidence algorithm
        row += 1
        btn_coin = tk.Button(
            self,
            text="coincidence",
            bg='#F3F3F3',
            padx=15,
            pady=10,
            command=lambda: self.coincidence())
        btn_coin.grid(row=row, column=0, columnspan=3, padx=10, pady=10)

        # clear plot
        row += 1
        btn_clear = tk.Button(
            self,
            text="clear",
            bg='#F3F3F3',
            padx=15,
            pady=10,
            command=lambda: self.clear())
        btn_clear.grid(row=row, column=0, columnspan=3, padx=10, pady=10)

    def coincidence(self):
        feature1 = self.feat_1.get()
        feature2 = self.feat_2.get()
        y1 = self.df[feature1].values
        y2 = self.df[feature2].values
        self.plot_coincidence(y1, y2, feature1, feature2)

    def plot_coincidence(self, y1, y2, name1, name2):
        if len(y1) != len(y2):
            print('The two sets of labels are not of same length')

        # everything to string
        y1 = list(map(str, y1))
        y2 = list(map(str, y2))
        # count coincidence
        pairs = list(zip(y1, y2))
        freq = Counter(pairs)
        xyz = [tuple(list(key) + [value]) for key, value in freq.items()]
        x, y, z = (np.array(i[0]) for i in zip(zip(*xyz)))

        size = self.calc_size(z)
        # color is the hypergeometric p-value scaled
        color = self.calc_color(y1, y2, x, y, z)
        x, y, xticks, yticks, xticklabels, yticklabels = self.get_ticks(x, y)

        # use the scatter function to plot
        ax = self.plot.ax
        ax.set_title('coincidence')
        ax.scatter(
            x,
            y,
            s=size * 2000,
            c=color,
            cmap="autumn",
            alpha=0.9,
            edgecolors="black",
            linewidth=1)
        # reset ticks for extra space
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xlabel(name1)
        ax.set_ylabel(name2)
        self.plot.canvas.draw()

    @staticmethod
    def calc_size(size_count):
        size = size_count * size_count  # size is square of coincidence
        # rescale size
        scaler_size = preprocessing.MinMaxScaler()
        scaler_size.fit(size.reshape(-1, 1))
        size = scaler_size.transform(size.reshape(-1, 1)).ravel() + 1
        return size

    @staticmethod
    def calc_color(list1, list2, x, y, count):
        count = list(count)
        # count cluster size
        cnt1 = Counter(list1)
        cnt2 = Counter(list2)
        # calc hypergeometric
        color = np.array([
            -math.log(
                hypergeom.sf(count[i] - 1, len(list1), cnt1[x[i]], cnt2[y[i]]))
            for i in range(len(count))
        ])
        # scale to 0-1
        scaler_color = preprocessing.MinMaxScaler()
        scaler_color.fit(color.reshape(-1, 1))
        color = scaler_color.transform(color.reshape(-1, 1)).ravel() + 1
        return color

    @staticmethod
    def get_ticks(x, y):
        xlabels, ylabels = list(set(x)), list(set(y))
        x = [xlabels.index(i) + 1 for i in x]
        y = [ylabels.index(i) + 1 for i in y]
        xticks = [i for i in range(len(xlabels) + 2)]
        yticks = [i for i in range(len(ylabels) + 2)]
        xlabels = [''] + xlabels + ['']
        ylabels = [''] + ylabels + ['']
        return x, y, xticks, yticks, xlabels, ylabels

    def clear(self):
        self.plot.clear()
