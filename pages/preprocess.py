import tkinter as tk
import pandas as pd
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
from libs.table import Table
from libs.font import SECTION, LABEL
from libs.button import Button
from libs.select import Select


class DataPreprocessPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.table = None
        self.init_frame()

    def init_frame(self):
        # split out left panel
        vertical_split = tk.PanedWindow(self)
        vertical_split.pack(fill=tk.BOTH, expand=1)
        self.df = self.controller.DF
        # add control panel
        ctrl_pane = PrepControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        self.vertical = vertical_split
        # add table
        self.vertical = vertical_split
        table = Table(vertical_split, self.df)
        self.table = table
        vertical_split.add(self.table)

    def reload(self):
        self.df = self.controller.DF
        self.table.destroy()
        table = Table(self.vertical, self.df)
        self.table = table
        self.vertical.add(table)
        self.ctrl_pane.df = self.df
        self.ctrl_pane.reload()


class PrepControlPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.row = 0
        self.df = self.controller.df
        self.select = None
        self.init_frame()

    def reload(self):
        self.row = 0
        self.df = self.controller.df
        self.init_frame()

    def init_frame(self):
        # select feature
        select = Select(self, self.df.columns.values.tolist())
        select.grid(row=self.row, column=0, columnspan=6)
        self.select = select

        # normalization
        self.row += 1
        label_norm = tk.Label(
            self, text="scaler",
            font=SECTION, bg='#F3F3F3'
        )
        label_norm.grid(row=self.row, column=0, columnspan=6)
        # scale in to 0-1
        Button(self, "scale 01", 1, 1, 2, lambda: self.scale_01())
        # normalization
        Button(self, "scale norm", 0, 3, 2, lambda: self.norm())

        # encode
        self.row += 1
        label_enc = tk.Label(self, text="encoder", font=SECTION, bg='#F3F3F3')
        label_enc.grid(row=self.row, column=0, columnspan=6)
        # encode categorical feature to integers
        Button(self, "label encoder", 1, 0, 3, lambda: self.label_encoder())
        # one hot encoder
        Button(self, "k hot encoder", 0, 3, 3, lambda: self.one_hot())
        # encode by quantile
        self.row += 1
        label_index = tk.Label(
            self, text="num of quantiles:",
            font=LABEL, bg='#F3F3F3'
        )
        label_index.grid(row=self.row, column=0, columnspan=3)
        entry_nq = tk.Entry(self, highlightbackground='#F3F3F3')
        entry_nq.grid(row=self.row, column=3, columnspan=2)
        self.entry_nq = entry_nq
        Button(self, "quantile encoder", 1, 0, 6, lambda: self.q_encoder())

        # drop
        self.row += 1
        label_rm = tk.Label(
            self, text="removal",
            font=SECTION, bg='#F3F3F3'
        )
        label_rm.grid(row=self.row, column=0, columnspan=6)
        # remove by column
        Button(self, "drop features", 1, 0, 6, lambda: self.drop_feature())
        # remove by index
        self.row += 1
        label_index = tk.Label(
            self, text="index:",
            font=LABEL, bg='#F3F3F3'
        )
        label_index.grid(row=self.row, column=0, columnspan=3)
        entry_index = tk.Entry(self, highlightbackground='#F3F3F3')
        entry_index.grid(row=self.row, column=3, columnspan=2)
        self.entry_index = entry_index
        Button(self, "drop subjects", 1, 0, 6, lambda: self.drop_index())

        # sample rows
        self.row += 1
        label_sample = tk.Label(
            self, text="sample",
            font=SECTION, bg='#F3F3F3'
        )
        label_sample.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        label_nrow = tk.Label(self, text="num of rows:",
                              font=LABEL, bg='#F3F3F3')
        label_nrow.grid(row=self.row, column=0, columnspan=3)
        entry_nrow = tk.Entry(self, highlightbackground='#F3F3F3')
        entry_nrow.grid(row=self.row, column=3, columnspan=2)
        self.entry_nrow = entry_nrow
        Button(self, "sample", 1, 0, 6, lambda: self.sample())

        # deal with missing value
        self.row += 1
        label_sample = tk.Label(
            self, text="missing",
            font=SECTION, bg='#F3F3F3'
        )
        label_sample.grid(row=self.row, column=0, columnspan=6)
        Button(self, "drop NAN", 1, 0, 2, lambda: self.drop_na())
        Button(self, "fill mean", 0, 2, 2, lambda: self.fill_mean())
        Button(self, "fill median", 0, 4, 2, lambda: self.fill_median())

    def scale_01(self):
        df = self.df
        for f in self.select.tags:
            df[f] = (df[f] - df[f].min()) / (df[f].max() - df[f].min())
        self.controller.reload()

    def norm(self):
        df = self.df
        for f in self.select.tags:
            df[f] = (df[f] - df[f].mean()) / df[f].std()
        self.controller.reload()

    def label_encoder(self):
        encoder = LabelEncoder()
        df = self.df
        for f in self.select.tags:
            new_col_name = f + '_label'
            df[new_col_name] = encoder.fit_transform(df[f])
            df[new_col_name].astype('int32')
        self.controller.reload()

    def q_encoder(self):
        df = self.df
        n = int(self.entry_nq.get())
        for f in self.select.tags:
            new_col_name = f + '_quantile'
            df[new_col_name] = pd.qcut(df[f], n, labels=False)
            df[new_col_name].astype('int32')
        self.controller.reload()

    def one_hot(self):
        encoder = LabelBinarizer()
        df = self.df
        for f in self.select.tags:
            data = encoder.fit_transform(df[f].values)
            names = [f + '_' + c for c in encoder.classes_]
            for i, n in enumerate(names):
                df[n] = pd.DataFrame(data[:, i], columns=[n])
            df.drop(columns=f, inplace=True)
        self.controller.reload()

    def drop_feature(self):
        df = self.df
        df.drop(list(self.select.tags), inplace=True, axis=1)
        self.controller.reload()

    def drop_index(self):
        df = self.df
        index = int(self.entry_index.get())
        df.drop(index=index, inplace=True)
        self.controller.reload()

    def sample(self):
        df = self.df
        nrows = int(self.entry_nrow.get())
        new_df = df.sample(df.shape[0] - nrows)
        df.drop(new_df.index, inplace=True)  # remove old rows
        self.controller.reload()

    def drop_na(self):
        self.df.dropna(inplace=True)
        self.controller.reload()

    def fill_mean(self):
        self.df.fillna(self.df.mean(), inplace=True)
        self.controller.reload()

    def fill_median(self):
        self.df.fillna(self.df.median(), inplace=True)
        self.controller.reload()
