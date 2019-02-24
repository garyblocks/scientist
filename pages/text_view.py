import tkinter as tk
from PIL import Image
import numpy as np
import os
from wordcloud import WordCloud, STOPWORDS
from libs.font import TITLE
from libs.book import Book
from libs.plot import Plot
from libs.button import Button
# from libs.button import Button


class TextViewPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.book = None
        self.plot = None
        self.init_frame()

    def reload(self):
        self.s = self.controller.STR
        self.ctrl_pane.s = self.s
        book = Book(self.vertical, string=self.s)
        self.book = book
        self.vertical.add(self.book)
        self.ctrl_pane.reload()

    def init_frame(self):
        # split out left panel
        self.vertical = tk.PanedWindow(self)
        self.vertical.pack(fill=tk.BOTH, expand=1)
        self.s = self.controller.STR
        # add control pane
        ctrl_pane = ViewControlPane(self.vertical, self)
        self.ctrl_pane = ctrl_pane
        self.vertical.add(ctrl_pane)
        book = Book(self.vertical, string=self.s)
        self.book = book
        self.vertical.add(book)
        plot = Plot(self.vertical)
        self.plot = plot


class ViewControlPane(tk.Frame):

    def __init__(self, master, controller=None):
        tk.Frame.__init__(self, master, bg='#F3F3F3')
        self.master = master
        self.controller = controller
        self.s = self.controller.s
        self.book = self.controller.book
        self.plot = self.controller.plot
        self.row = 0
        self.init_frame()

    def reload(self):
        self.s = self.controller.s
        self.row = 0
        self.book = self.controller.book
        self.plot = self.controller.plot
        self.init_frame()

    def init_frame(self):
        title_table = tk.Label(
            self, text="Text View", font=TITLE, bg='#F3F3F3',
            width=25
        )
        title_table.grid(row=self.row, column=0, columnspan=6)

        # display random rows
        Button(self, "word cloud", 1, 2, 2, lambda: self.word_cloud())

    def word_cloud(self):
        self.show_plot()
        # set up the word cloud
        path_to_pic = os.getcwd() + '/static/default_pic.png'
        mask = np.array(Image.open(path_to_pic))
        stopwords = set(STOPWORDS)
        wc = WordCloud(
            background_color="white",
            max_words=200,
            mask=mask,
            stopwords=stopwords
        )
        # generate word cloud
        wc.generate(self.s)
        # show
        self.plot.ax.imshow(wc, interpolation='bilinear')
        self.plot.ax.axis("off")
        self.plot.canvas.draw()

    def show_plot(self):
        self.controller.vertical.forget(self.book)
        self.controller.vertical.add(self.plot)

    def show_book(self):
        self.controller.vertical.forget(self.plot)
        self.controller.vertical.add(self.book)
