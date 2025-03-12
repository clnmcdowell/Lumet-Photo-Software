import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title('Lumet Sorter')

folderPath = filedialog.askdirectory(title = "Select Folder of Photos to Sort")
print("Selected Folder: " + folderPath)