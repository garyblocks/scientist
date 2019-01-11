import tkinter as tk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
from libs.font import TITLE, LABEL
from libs.button import Button
from libs.select import Select
from libs.table import Table
from libs.alert import Alert


class ClassificationBiclassPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.DF
        self.init_frame()

    def reload(self):
        self.df = self.controller.DF
        self.ctrl_pane.df = self.df
        self.ctrl_pane.reload()
        self.result_pane.reload()

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
        self.select = None
        self.row = 0
        self.init_frame()

    def reload(self):
        self.row = 0
        self.init_frame()

    def init_frame(self):
        title_lable = tk.Label(
            self, text="Biclass", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_lable.grid(row=self.row, column=0, columnspan=6)

        # select feature
        select = Select(self, self.df.columns.values.tolist())
        select.grid(row=self.row, column=0, columnspan=6)
        self.select = select

        # select features to classify
        self.row += 1
        label_class = tk.Label(self, text="choose target",
                               font=LABEL, bg='#F3F3F3')
        label_class.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        chosen_cls = tk.StringVar(self)
        choices = self.df.columns.values.tolist()
        if not choices:
            choices = ['']
        chosen_cls.set(choices[0] if choices else '')
        feature_menu = tk.OptionMenu(self, chosen_cls, *choices)
        feature_menu.config(bg="#F3F3F3")
        feature_menu.grid(row=self.row, column=0, columnspan=6)
        self.chose_cls = chosen_cls

        # select algorithm to use
        self.row += 1
        label_algo = tk.Label(self, text="choose classification algorithm",
                              font=LABEL, bg='#F3F3F3')
        label_algo.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        chosen_algo = tk.StringVar(self)
        algos = ['kNN', 'SGD', 'Logistic']
        chosen_algo.set(algos[0])
        algo_menu = tk.OptionMenu(self, chosen_algo, *algos)
        algo_menu.config(bg="#F3F3F3")
        algo_menu.grid(row=self.row, column=0, columnspan=6)
        self.chose_algo = chosen_algo

        # train test split
        self.row += 1
        label_sec_1 = tk.Label(self, text="train-test split ratio",
                               font=LABEL, bg='#F3F3F3')
        label_sec_1.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        entry_split_rate = tk.Entry(self)
        entry_split_rate.grid(row=self.row, column=0, columnspan=6)
        self.split_rate = entry_split_rate
        Button(self, "classify", 1, 0, 6, lambda: self.run())

        # default sizes
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=20)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=20)

    def run(self):
        feat_list = list(self.select.tags)
        algo = self.chose_algo.get()
        self.X = self.df[feat_list].values
        self.y = self.df[self.chose_cls.get()].values
        if len(set(self.y)) > 2:
            alert = Alert()
            alert.warn("target must be binary")
            return
        self.hold_out()
        if algo == 'kNN':
            self.model = KNeighborsClassifier()
        elif algo == 'SGD':
            self.model = SGDClassifier(random_state=101)
        elif algo == 'Logistic':
            self.model = LogisticRegression(C=1., solver='lbfgs')
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
        train_precision = precision_score(self.y_train, y_train_pred)
        test_precision = precision_score(self.y_test, y_test_pred)
        train_recall = recall_score(self.y_train, y_train_pred)
        test_recall = recall_score(self.y_test, y_test_pred)
        train_f1 = f1_score(self.y_train, y_train_pred)
        test_f1 = f1_score(self.y_test, y_test_pred)
        # create metric table
        data = [
            [train_accuracy, test_accuracy],
            [train_precision, test_precision],
            [train_recall, test_recall],
            [train_f1, test_f1]
        ]
        index = ['accuracy', 'precision', 'recall', 'f1']
        metrics = pd.DataFrame(data, index, ['train', 'test'])
        self.controller.result_pane.metric_df = metrics
        # create confusion matrix
        self.controller.result_pane.train_conf_df = pd.DataFrame(confusion_matrix(self.y_train, y_train_pred))
        self.controller.result_pane.test_conf_df = pd.DataFrame(confusion_matrix(self.y_test, y_test_pred))
        self.controller.reload()


class ClassificationResultPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.metric_df = self.df
        self.metric_table = None
        self.train_conf_df = self.df
        self.train_conf_mx = None
        self.test_conf_df = self.df
        self.test_conf_mx = None
        self.row = 0
        self.init_frame()

    def reload(self):
        self.row = 0
        self.df = self.controller.df
        self.metric_table.destroy()
        self.init_frame()

    def init_frame(self):
        self.metric_table = Table(self, self.metric_df, width=500)
        self.metric_table.grid(row=self.row, sticky=tk.N+tk.S+tk.E+tk.W)
        self.row += 1
        self.train_conf_mx = Table(self, self.train_conf_df, width=500)
        self.train_conf_mx.grid(row=self.row, sticky=tk.N+tk.S+tk.E+tk.W)
        self.row += 1
        self.test_conf_mx = Table(self, self.test_conf_df, width=500)
        self.test_conf_mx.grid(row=self.row, sticky=tk.N+tk.S+tk.E+tk.W)
