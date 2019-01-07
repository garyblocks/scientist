import tkinter as tk
import pandas as pd
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
from libs.table import Table
from libs.font import SECTION, LABEL, TITLE
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
        self.row += 1
        label_title = tk.Label(
            self, text="Preprocess",
            font=TITLE, bg='#F3F3F3'
        )
        label_title.grid(row=self.row, column=0, columnspan=6)
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
        Button(self, "label", 1, 0, 2, lambda: self.label_encoder())
        # one hot encoder
        Button(self, "k hot", 0, 2, 2, lambda: self.one_hot())
        # encode by quantile
        Button(self, "quantile", 0, 4, 2, lambda: self.q_encode_pop_up())

        # drop
        self.row += 1
        label_rm = tk.Label(
            self, text="drop data",
            font=SECTION, bg='#F3F3F3'
        )
        label_rm.grid(row=self.row, column=0, columnspan=6)
        # remove by column
        Button(self, "drop features", 1, 0, 6, lambda: self.drop_feature())
        # remove by index
        Button(self, "drop subjects", 1, 0, 6, lambda: self.drop_index_pop_up())

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
        label_nrow.grid(row=self.row, column=0, columnspan=2)
        entry_nrow = tk.Entry(self, highlightbackground='#F3F3F3', width=5)
        entry_nrow.grid(row=self.row, column=2, columnspan=2)
        self.entry_nrow = entry_nrow
        Button(self, "sample", 0, 4, 2, lambda: self.sample())

        # deal with missing value
        self.row += 1
        label_miss = tk.Label(
            self, text="missing",
            font=SECTION, bg='#F3F3F3'
        )
        label_miss.grid(row=self.row, column=0, columnspan=6)
        Button(self, "drop NAN", 1, 0, 2, lambda: self.drop_na())
        Button(self, "fill mean", 0, 2, 2, lambda: self.fill_mean())
        Button(self, "fill median", 0, 4, 2, lambda: self.fill_median())
        Button(self, "fill forward", 1, 0, 2, lambda: self.fill_forward())

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
        self.pop_up_win.destroy()
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
        self.pop_up_win.destroy()
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

    def fill_forward(self):
        self.df.fillna(self.df.ffill(), inplace=True)
        self.controller.reload()

    def q_encode_pop_up(self):
        pop_up_win = tk.Toplevel()
        pop_up_win.wm_title("Quantile encode")

        label = tk.Label(
            pop_up_win, text="number of quantiles:",
            font=LABEL, bg='#F3F3F3'
        )
        label.grid(row=0, column=0)
        entry_nq = tk.Entry(pop_up_win, highlightbackground='#F3F3F3', width=10)
        entry_nq.grid(row=1, column=0)
        self.entry_nq = entry_nq

        btn = tk.Button(pop_up_win, text="Encode", command=self.q_encoder)
        btn.grid(row=2, column=0)

        self.pop_up_win = pop_up_win

    def drop_index_pop_up(self):
        pop_up_win = tk.Toplevel()
        pop_up_win.wm_title("drop by index")

        label = tk.Label(
            pop_up_win, text="index: ",
            font=LABEL, bg='#F3F3F3'
        )
        label.grid(row=0, column=0)
        entry_index = tk.Entry(pop_up_win, highlightbackground='#F3F3F3', width=10)
        entry_index.grid(row=1, column=0)
        self.entry_index = entry_index

        btn = tk.Button(pop_up_win, text="drop", command=self.drop_index)
        btn.grid(row=2, column=0)

        self.pop_up_win = pop_up_win
