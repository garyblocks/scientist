import tkinter as tk
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, confusion_matrix
from libs.font import TITLE, LABEL
from libs.button import Button
from libs.select import Select
from libs.table import Table


class ClassificationMulticlassPage(tk.Frame):

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
            self, text="Classification", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_lable.grid(row=self.row, column=0, columnspan=6)

        # select feature
        select = Select(self, self.df.columns.values.tolist())
        select.grid(row=self.row, column=0, columnspan=6)
        self.select = select

        # select features to classify
        self.row += 1
        label_class = tk.Label(self, text="choose class feature",
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
        algos = ['kNN', 'Naive Bayes', 'Decision Tree', 'LDA']
        chosen_algo.set(algos[0])
        algo_menu = tk.OptionMenu(self, chosen_algo, *algos)
        algo_menu.config(bg="#F3F3F3")
        algo_menu.grid(row=self.row, column=0, columnspan=6)
        self.chose_algo = chosen_algo

        # train test split
        self.row += 1
        label_sec_1 = tk.Label(self, text="hold out ratio",
                               font=LABEL, bg='#F3F3F3')
        label_sec_1.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        entry_split_rate = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, bg='#F3F3F3', length=200)
        entry_split_rate.grid(row=self.row, column=0, columnspan=6)
        self.split_rate = entry_split_rate

        # cross validation
        self.row += 1
        label_sec_2 = tk.Label(self, text="CV folds",
                               font=LABEL, bg='#F3F3F3')
        label_sec_2.grid(row=self.row, column=0, columnspan=6)
        self.row += 1
        entry_cv_k = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL, resolution=1, bg='#F3F3F3', length=200)
        entry_cv_k.grid(row=self.row, column=0, columnspan=6)
        self.cv_k = entry_cv_k

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
        self.hold_out()
        if algo == 'kNN':
            self.model = KNeighborsClassifier()
        elif algo == 'Naive Bayes':
            self.model = BernoulliNB()
        elif algo == 'Decision Tree':
            self.model = DecisionTreeClassifier()
        elif algo == 'LDA':
            self.model = LinearDiscriminantAnalysis()
        self.evaluate()

    def hold_out(self):
        r = float(self.split_rate.get())
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=r, random_state=101, stratify=self.y)  # noqa

    def evaluate(self):
        # apply cross validation for training
        k = int(self.cv_k.get())
        y_train_pred = cross_val_predict(self.model, self.X_train, self.y_train, cv=k)
        self.model.fit(self.X_train, self.y_train)
        y_test_pred = self.model.predict(self.X_test)
        train_accuracy = accuracy_score(self.y_train, y_train_pred)
        test_accuracy = accuracy_score(self.y_test, y_test_pred)
        # create confusion matrix
        self.controller.result_pane.train_conf_df = pd.DataFrame(confusion_matrix(self.y_train, y_train_pred))
        self.controller.result_pane.test_conf_df = pd.DataFrame(confusion_matrix(self.y_test, y_test_pred))
        self.controller.reload()
        # update accuracy score
        self.controller.result_pane.label_train_accuracy['text'] += str(train_accuracy)  # noqa
        self.controller.result_pane.label_test_accuracy['text'] += str(test_accuracy)  # noqa


class ClassificationResultPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.train_conf_df = self.df
        self.train_conf_mx = None
        self.test_conf_df = self.df
        self.test_conf_mx = None
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
        self.row += 1
        label_train_conf_mx = tk.Label(self, text="train confusion matrix: ",
                                       font=LABEL, bg='#F3F3F3')
        label_train_conf_mx.grid(row=self.row, column=0, columnspan=3)
        self.row += 1
        self.train_conf_mx = Table(self, self.train_conf_df, width=500)
        self.train_conf_mx.grid(row=self.row, sticky=tk.N+tk.S+tk.E+tk.W)

        # test
        self.row += 1
        label_test_accuracy = tk.Label(self, text="test accuracy: ",
                                       font=LABEL, bg='#F3F3F3')
        label_test_accuracy.grid(row=self.row, column=0, columnspan=3)
        self.label_test_accuracy = label_test_accuracy
        self.row += 1
        label_test_conf_mx = tk.Label(self, text="test confusion matrix: ",
                                      font=LABEL, bg='#F3F3F3')
        label_test_conf_mx.grid(row=self.row, column=0, columnspan=3)
        self.row += 1
        self.test_conf_mx = Table(self, self.test_conf_df, width=500)
        self.test_conf_mx.grid(row=self.row, sticky=tk.N+tk.S+tk.E+tk.W)
