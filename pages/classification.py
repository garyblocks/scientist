import tkinter as tk
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score  # , precision_score, recall_score
from libs.font import TITLE, LABEL
from libs.button import Button


class AnalysisClassificationPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.DF
        self.init_frame()

    def reload(self):
        self.df = self.controller.DF
        self.ctrl_pane.reload()

    def init_frame(self):
        # split out left panel
        vertical_split = tk.PanedWindow(self)
        vertical_split.pack(fill=tk.BOTH, expand=1)
        self.df = self.controller.DF
        # add control panel
        ctrl_pane = ClassificationControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        # add result panel
        result_pane = ClassificationResultPane(vertical_split, self)
        self.result_pane = result_pane
        vertical_split.add(result_pane)
        self.vertical = vertical_split


class ClassificationControlPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.features = set()
        self.row = 0
        self.init_frame()

    def reload(self):
        self.row = 0
        self.df = self.controller.df
        self.init_frame()

    def init_frame(self):
        title_lable = tk.Label(
            self, text="Classification", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_lable.grid(row=self.row, column=0, columnspan=3)

        # select features to classify
        self.row += 1
        label_feats = tk.Label(self, text="features: no feature",
                               font=LABEL, bg='#F3F3F3')
        label_feats.grid(row=self.row, column=0, columnspan=3)
        self.label_feats = label_feats
        self.row += 1
        chosen = tk.StringVar(self)
        choices = self.df.columns.values.tolist()
        if not choices:
            choices = ['']
        chosen.set(choices[0] if choices else '')
        add_feat = tk.OptionMenu(self, chosen, *choices)
        add_feat.grid(row=self.row, column=0, columnspan=2)
        self.add_feat = chosen
        btn_add_feat = tk.Button(self, text="add", bg='#F3F3F3',
                                 padx=15, pady=10,
                                 command=lambda: self.add_feature())
        btn_add_feat.grid(row=self.row, column=2, columnspan=1, padx=5, pady=5)

        # select features to classify
        self.row += 1
        label_class = tk.Label(self, text="choose class feature",
                               font=LABEL, bg='#F3F3F3')
        label_class.grid(row=self.row, column=0, columnspan=3)
        self.row += 1
        chosen_cls = tk.StringVar(self)
        choices = self.df.columns.values.tolist()
        if not choices:
            choices = ['']
        chosen_cls.set(choices[0] if choices else '')
        chose_cls = tk.OptionMenu(self, chosen_cls, *choices)
        chose_cls.grid(row=self.row, column=0, columnspan=2)
        self.chose_cls = chosen_cls

        # train test split
        self.row += 1
        label_sec_1 = tk.Label(self, text="train-test split ratio",
                               font=LABEL, bg='#F3F3F3')
        label_sec_1.grid(row=self.row, column=0, columnspan=3)
        self.row += 1
        entry_split_rate = tk.Entry(self)
        entry_split_rate.grid(row=self.row, column=0, columnspan=3)
        self.split_rate = entry_split_rate
        Button(self, "classify", 1, 0, 3, lambda: self.run())

        # default sizes
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=20)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=20)

    def add_feature(self):
        new_feature = self.add_feat.get()
        self.features.add(new_feature)
        self.label_feats['text'] = 'features: ' + ','.join(list(self.features))

    def run(self):
        feat_list = list(self.features)
        self.X = self.df[feat_list].values
        self.y = self.df[self.chose_cls.get()].values
        self.hold_out()
        self.model = KNeighborsClassifier()
        self.model.fit(self.X_train, self.y_train)
        self.evaluate()

    def hold_out(self):
        r = float(self.split_rate.get())
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=r, random_state=101)  # noqa

    def evaluate(self):
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        train_accuracy = accuracy_score(self.y_train, y_train_pred)
        test_accuracy = accuracy_score(self.y_test, y_test_pred)
        # train_precision = precision_score(self.y_train, y_train_pred)
        # test_precision = precision_score(self.y_test, y_test_pred)
        # train_recall = recall_score(self.y_train, y_train_pred)
        # test_recall = recall_score(self.y_test, y_test_pred)
        self.controller.result_pane.label_train_accuracy['text'] += str(train_accuracy)  # noqa
        self.controller.result_pane.label_test_accuracy['text'] += str(test_accuracy)  # noqa
        # self.controller.result_pane.label_train_precision['text'] += str(train_precision)  # noqa
        # self.controller.result_pane.label_test_precision['text'] += str(test_precision)  # noqa
        # self.controller.result_pane.label_train_recall['text'] += str(train_recall)  # noqa
        # self.controller.result_pane.label_test_recall['text'] += str(test_recall)  # noqa


class ClassificationResultPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.row = 0
        self.init_frame()

    def reload(self):
        self.row = 0
        self.df = self.controller.df
        self.init_frame()

    def init_frame(self):
        # train
        self.row += 1
        label_train_accuracy = tk.Label(self, text="train accuracy: ",
                                        font=LABEL, bg='#F3F3F3')
        label_train_accuracy.grid(row=self.row, column=0, columnspan=3)
        self.label_train_accuracy = label_train_accuracy
        # self.row += 1
        # label_train_precision = tk.Label(self, text="train precision: ",
        #                                  font=LABEL, bg='#F3F3F3')
        # label_train_precision.grid(row=self.row, column=0, columnspan=3)
        # self.label_train_precision = label_train_precision
        # self.row += 1
        # label_train_recall = tk.Label(self, text="train recall: ",
        #                               font=LABEL, bg='#F3F3F3')
        # label_train_recall.grid(row=self.row, column=0, columnspan=3)
        # self.label_train_recall = label_train_recall
        # test
        self.row += 1
        label_test_accuracy = tk.Label(self, text="test accuracy: ",
                                       font=LABEL, bg='#F3F3F3')
        label_test_accuracy.grid(row=self.row, column=0, columnspan=3)
        self.label_test_accuracy = label_test_accuracy
        # self.row += 1
        # label_test_precision = tk.Label(self, text="test precision: ",
        #                                 font=LABEL, bg='#F3F3F3')
        # label_test_precision.grid(row=self.row, column=0, columnspan=3)
        # self.label_test_precision = label_test_precision
        # self.row += 1
        # label_test_recall = tk.Label(self, text="test recall: ",
        #                              font=LABEL, bg='#F3F3F3')
        # label_test_recall.grid(row=self.row, column=0, columnspan=3)
        # self.label_test_recall = label_test_recall
