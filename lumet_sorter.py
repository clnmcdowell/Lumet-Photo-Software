import tkinter as tk
from tkinter import filedialog
import os
import shutil

# Function to select folder of photos to sort
def select_folder():
    root = tk.Tk()
    root.title('Lumet Sorter')
    root.withdraw()

    # Ask user to select folder of photos to sort
    folder_path = filedialog.askdirectory(title = "Select folder of photos to sort")
    print("Selected Folder: " + folder_path)

# Function to setup folders and move photos to Unsorted folder
def setup_folders(folder_path):
    subfolders = ["Unsorted", "Yes", "No", "Maybe"]
    for subfolder in subfolders:
        folder = os.path.join(folder_path, subfolder)
        os.makedirs(folder, exist_ok=True)
    
    # Define image extensions
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif")

    # Move images to Unsorted folder
    for file in os.listdir(folder_path):
        if file.endswith(image_extensions):
            source = os.path.join(folder_path, file)
            destination = os.path.join(folder_path, "Unsorted", file)
            shutil.move(source, destination)

