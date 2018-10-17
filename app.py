import tkinter as tk
import pandas as pd
from tkinter import filedialog
# internal
from libs.font import LABEL
from pages.preprocess import DataPreprocessPage
from pages.view import DataViewPage
from pages.clustering.kmeans import ClusteringKmeansPage
from pages.clustering.hierarchy import ClusteringHierarchyPage
from pages.classification import AnalysisClassificationPage
from pages.coincidence import AnalysisCoincidencePage

DATAFRAMES = {}


class Scientist(tk.Tk):

    def __init__(self, *args, **kwargs):
        # data frame
        self.DF = pd.DataFrame()

        # load tkinter
        tk.Tk.__init__(self, *args, **kwargs)

        # set root properties
        self.title("Scientist")
        self.geometry("1300x800")

        # create menu bar
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        file_menu = tk.Menu(self.menu)
        file_menu.add_command(label='Import CSV', command=self.import_csv)
        file_menu.add_command(label='Save CSV', command=self.save_csv)
        file_menu.add_command(label='Exit', command=self.client_exit)
        self.menu.add_cascade(label='File', menu=file_menu)
        data_menu = tk.Menu(self.menu)
        data_menu.add_command(label="View", command=self.data_view)
        data_menu.add_command(label="Preprocess", command=self.data_preprocess)
        self.menu.add_cascade(label="Data", menu=data_menu)
        analysis_menu = tk.Menu(self.menu)
        analysis_clustering_menu = tk.Menu(analysis_menu)
        analysis_clustering_menu.add_command(
            label="Kmeans",
            command=self.clustering_kmeans
        )
        analysis_clustering_menu.add_command(
            label="Hierarchy",
            command=self.clustering_hierarchy
        )
        analysis_menu.add_cascade(
            label="Clustering",
            menu=analysis_clustering_menu
        )
        analysis_menu.add_command(
            label="Classification",
            command=self.analysis_classification
        )
        analysis_menu.add_command(
            label="Coincidence",
            command=self.analysis_coincidence
        )
        self.menu.add_cascade(label="Analysis", menu=analysis_menu)

        # create container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # load frames
        self.frames = {}
        pages = (StartPage, DataViewPage, DataPreprocessPage,
                 ClusteringKmeansPage, ClusteringHierarchyPage,
                 AnalysisClassificationPage,
                 AnalysisCoincidencePage)
        for F in pages:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # start with startPage
        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

    def import_csv(self):
        filename = self.select_file()
        if not filename:
            return
        self.DF = pd.read_csv(filename)
        DATAFRAMES[filename] = self.DF
        self.frames[DataViewPage].reload()
        self.show_frame(DataViewPage)

    def save_csv(self):
        filename = filedialog.asksaveasfile(
            mode='w',
            title="Save file",
            defaultextension=".csv"
        )
        self.DF.to_csv(filename)

    def select_file(self):
        filename = filedialog.askopenfilename(
            initialdir="~/",
            title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
        )
        return filename

    def client_exit(self):
        exit()

    def data_view(self):
        self.frames[DataViewPage].reload()
        self.show_frame(DataViewPage)

    def data_preprocess(self):
        self.frames[DataPreprocessPage].reload()
        self.show_frame(DataPreprocessPage)

    def clustering_kmeans(self):
        self.frames[ClusteringKmeansPage].reload()
        self.show_frame(ClusteringKmeansPage)

    def clustering_hierarchy(self):
        self.frames[ClusteringHierarchyPage].reload()
        self.show_frame(ClusteringHierarchyPage)

    def analysis_classification(self):
        self.frames[AnalysisClassificationPage].reload()
        self.show_frame(AnalysisClassificationPage)

    def analysis_coincidence(self):
        self.frames[AnalysisCoincidencePage].reload()
        self.show_frame(AnalysisCoincidencePage)


class StartPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.init_frame()

    def init_frame(self):
        label = tk.Label(
            self,
            text='There is no dataframe yet, please import one',
            font=LABEL
        )
        label.pack(pady=10, padx=10)
        import_csv_btn = tk.Button(
            self,
            text="Import CSV",
            command=self.controller.import_csv
        )
        import_csv_btn.pack()


app = Scientist()
app.mainloop()
