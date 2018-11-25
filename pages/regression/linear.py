import tkinter as tk
import numpy as np
import pandas as pd
import statsmodels.api as sm
from libs.table import Table
from libs.font import TITLE, LABEL
from libs.button import Button
from libs.select import Select


class RegressionLinearPage(tk.Frame):

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
        ctrl_pane = RegressionControlPane(vertical_split, self)
        self.ctrl_pane = ctrl_pane
        vertical_split.add(ctrl_pane)
        # add result panel
        result_pane = RegressionResultPane(vertical_split, self)
        self.result_pane = result_pane
        vertical_split.add(result_pane)
        self.vertical = vertical_split


class RegressionControlPane(tk.Frame):

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
            self, text="Regression", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_lable.grid(row=self.row, column=0, columnspan=6)

        # select feature
        select = Select(self, self.df.columns.values.tolist())
        select.grid(row=self.row, column=0, columnspan=6)
        self.select = select

        # select features to regress
        self.row += 1
        label_class = tk.Label(self, text="choose dependent feature",
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

        Button(self, "regress", 1, 0, 6, lambda: self.run())

        # default sizes
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=20)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=20)

    def run(self):
        feat_list = list(self.select.tags)
        self.X = self.df[feat_list].values
        self.y = self.df[self.chose_cls.get()].values
        self.model = sm.OLS(self.y, sm.add_constant(self.X))
        results = self.model.fit()
        self.evaluate(results)

    def evaluate(self, results):
        coefs = results.params
        sde = results.bse
        t_values = results.tvalues
        p_values = results.pvalues
        conf_int = results.conf_int().T
        cfi_low = conf_int[0]
        cfi_high = conf_int[1]

        data = np.vstack((
            np.array(['Intercept'] + list(self.select.tags)),
            np.round(coefs, 4),
            np.round(sde, 4),
            np.round(t_values, 4),
            np.round(p_values, 4),
            np.round(cfi_low, 4),
            np.round(cfi_high, 4)
        ))
        print(data.T)
        columns = ['Features', 'Coefficients', 'Std Errors', 'T Values', 'P Values', '[0.025', '0.975]']
        result = pd.DataFrame(data=data.T, columns=columns)
        self.controller.result_pane.result = result
        self.controller.reload()


class RegressionResultPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.result = self.df  # for initialize
        self.table = None
        self.row = 0
        self.init_frame()

    def reload(self):
        self.row = 0
        self.df = self.controller.df
        self.table.destroy()
        self.init_frame()

    def init_frame(self):
        self.table = Table(self, self.result, width=500)
        self.table.pack(fill="both", expand=True)
