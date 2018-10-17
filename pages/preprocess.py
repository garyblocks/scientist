import tkinter as tk
import pandas as pd
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
from libs.table import Table
from libs.font import TITLE, SECTION, LABEL
from libs.button import Button


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
        self.features = set()
        self.row = 0
        self.df = self.controller.df
        self.init_frame()

    def reload(self):
        self.row = 0
        self.df = self.controller.df
        self.init_frame()

    def init_frame(self):
        # title
        text = tk.Label(
            self, text="Preprocess", font=TITLE,
            bg='#F3F3F3', width=25
        )
        text.grid(row=self.row, column=0, columnspan=6)

        # select features to cluster on
        self.row += 1
        label_feats = tk.Label(self, text="features: no feature",
                               font=LABEL, bg='#F3F3F3')
        label_feats.grid(row=self.row, column=0, columnspan=6)
        self.label_feats = label_feats
        self.row += 1
        chosen = tk.StringVar(self)
        choices = self.df.columns.values.tolist()
        if not choices:
            choices = ['']
        chosen.set(choices[0] if choices else '')
        add_feat = tk.OptionMenu(self, chosen, *choices)
        add_feat.grid(row=self.row, column=0, columnspan=4)
        self.add_feat = chosen
        btn_add_feat = tk.Button(self, text="add", bg='#F3F3F3',
                                 padx=15, pady=10,
                                 command=lambda: self.add_feature())
        btn_add_feat.grid(row=self.row, column=4, columnspan=2, padx=5, pady=5)

        # normalization
        self.row += 1
        label_norm = tk.Label(
            self, text="normalization",
            font=SECTION, bg='#F3F3F3'
        )
        label_norm.grid(row=self.row, column=0, columnspan=6)
        # scale in to 0-1
        Button(self, "scale 01", 1, 0, 3, lambda: self.scale_01())
        # normalization
        Button(self, "normalization", 0, 3, 3, lambda: self.norm())

        # encode
        self.row += 1
        label_enc = tk.Label(
            self, text="encoding",
            font=SECTION, bg='#F3F3F3'
        )
        label_enc.grid(row=self.row, column=0, columnspan=6)
        # encode categorical feature to integers
        Button(self, "label encoder", 1, 0, 3, lambda: self.label_encoder())
        # one hot encoder
        Button(self, "one hot encoder", 0, 3, 3, lambda: self.one_hot())

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
            self, text="index",
            font=LABEL, bg='#F3F3F3'
        )
        label_index.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        entry_index = tk.Entry(self)
        entry_index.grid(row=self.row, column=0, columnspan=6)
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
        label_nrow = tk.Label(self, text="num of rows",
                              font=LABEL, bg='#F3F3F3')
        label_nrow.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        entry_nrow = tk.Entry(self)
        entry_nrow.grid(row=self.row, column=0, columnspan=6)
        self.entry_nrow = entry_nrow
        Button(self, "sample", 1, 0, 6, lambda: self.sample())

        # deal with missing value
        self.row += 1
        label_sample = tk.Label(
            self, text="missing",
            font=SECTION, bg='#F3F3F3'
        )
        label_sample.grid(row=self.row, column=0, columnspan=6)
        Button(self, "drop NAN", 1, 0, 6, lambda: self.drop_na())

    def scale_01(self):
        df = self.df
        for f in self.features:
            df[f] = (df[f] - df[f].min()) / (df[f].max() - df[f].min())
        self.controller.reload()

    def norm(self):
        df = self.df
        for f in self.features:
            df[f] = (df[f] - df[f].mean()) / df[f].std()
        self.controller.reload()

    def label_encoder(self):
        encoder = LabelEncoder()
        df = self.df
        for f in self.features:
            new_col_name = f + '_label'
            df[new_col_name] = encoder.fit_transform(df[f])
            df[new_col_name].astype('int32')
        self.controller.reload()

    def one_hot(self):
        encoder = LabelBinarizer()
        df = self.df
        for f in self.features:
            data = encoder.fit_transform(df[f].values)
            names = [f + '_' + c for c in encoder.classes_]
            for i, n in enumerate(names):
                df[n] = pd.DataFrame(data[:, i], columns=[n])
            df.drop(columns=f, inplace=True)
        self.controller.reload()

    def add_feature(self):
        new_feature = self.add_feat.get()
        self.features.add(new_feature)
        self.label_feats['text'] = 'features: ' + ','.join(list(self.features))

    def drop_feature(self):
        df = self.df
        df.drop(list(self.features), inplace=True, axis=1)
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
        df = self.df
        df.dropna(inplace=True)
        self.controller.reload()
