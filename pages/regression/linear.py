import tkinter as tk
import numpy as np
import pandas as pd
import statsmodels.api as sm
from libs.table import Table
from libs.font import TITLE, SECTION, LABEL
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
        stat_df = self.get_statistics(results)
        coef_df = self.get_coefficients(results)
        self.controller.result_pane.stat_df = stat_df
        self.controller.result_pane.coef_df = coef_df
        self.controller.reload()

    def get_coefficients(self, results):
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
            p_values,
            # np.round(p_values, 4),
            np.round(cfi_low, 4),
            np.round(cfi_high, 4)
        ))
        columns = ['Features', 'Coefficients', 'Std Errors', 'T Values', 'P Values', '[0.025', '0.975]']
        return pd.DataFrame(data=data.T, columns=columns)

    def get_statistics(self, results):
        stat_names = [
            'R-squared', 'Adj. R-squared', 'F-statistic', 'Prob (F-statistic)',
            'Log-Likelihood', 'AIC', 'BIC', 'Df Model'
        ]
        values = [
            np.round(results.rsquared, 4),
            np.round(results.rsquared_adj, 4),
            np.round(results.fvalue, 4),
            np.round(results.f_pvalue, 4),
            np.round(results.llf, 4),
            np.round(results.aic, 4),
            np.round(results.bic, 4),
            np.round(results.df_model, 4)
        ]
        data = np.vstack((np.array(stat_names), np.array(values)))
        columns = ['Stats', 'Values']
        return pd.DataFrame(data=data.T, columns=columns)


class RegressionResultPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.df = self.controller.df
        self.coef_df = self.df  # for initialize
        self.stat_df = self.df  # for initialize
        self.coef_label = None
        self.coef_table = None
        self.stat_label = None
        self.stat_table = None
        self.init_frame()

    def reload(self):
        self.df = self.controller.df
        self.coef_label.destroy()
        self.coef_table.destroy()
        self.stat_label.destroy()
        self.stat_table.destroy()
        self.init_frame()

    def init_frame(self):
        # model statistics
        self.stat_label = tk.Label(self, text="Model Statistics", font=SECTION, bg='#F3F3F3')
        self.stat_label.pack()
        self.stat_table = Table(self, self.stat_df, width=500)
        self.stat_table.pack()

        # coefficients
        self.coef_label = tk.Label(self, text="Model Coefficients", font=SECTION, bg='#F3F3F3')
        self.coef_label.pack()
        self.coef_table = Table(self, self.coef_df, width=500)
        self.coef_table.pack(fill=tk.BOTH, expand=tk.YES)
