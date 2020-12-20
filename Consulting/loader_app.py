import textwrap
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb
from coordinate_data_pull import CoordinateDemographicsDataLoader

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.create_title()
        self.filepath = None
        self.create_file_button()
        self.create_run_button()

    def create_file_button(self):
        self.file_label_var = tk.StringVar()
        self.file_label = tk.Label(self, textvariable=self.file_label_var)
        self.file_label.pack(padx=10, pady=25)
    
        self.file_btn = tk.Button(self, text='Select File', command=self.file_dialog)
        self.file_btn.pack(padx=10, pady=25)

    def file_dialog(self):
        self.filepath = filedialog.askopenfilename(
            parent=self,
            title='Choose a file',
            filetype = (("Excel file","*.xlsx"),("Excel file", "*.xls")),
        )
        self.file_label_var.set(textwrap.fill(self.filepath, 70))
    
    
    def create_title(self):
        title = tk.Label(text="Coordinate Data Downloader", font=("Arial", 14, "bold"))
        title.pack(padx=10, pady=10)
    
    def create_run_button(self):
        self.run_btn = tk.Button(self, text="Run", command=self.run)
        self.run_btn.pack(padx=10, pady=10)
    
    def run(self):
        if self.filepath is None:
           mb.showwarning('Error', "Please enter a filename")
        else:
            loader = CoordinateDemographicsDataLoader(self.filepath)
            loader.fetch_coodinate_data()