import tkinter as tk
from tkinter import filedialog
import os
import shutil
from PIL import Image, ImageTk

# Create a global window
root = tk.Tk()
root.title('Lumet Sorter')
root.withdraw()
image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif")

# Function to select folder of photos to sort
def select_folder():
    # Ask user to select folder of photos to sort
    folder_path = filedialog.askdirectory(title = "Select folder of photos to sort")
    if folder_path:
        print("Selected Folder: " + folder_path)
        return folder_path

# Function to setup folders and move photos to Unsorted folder
def setup_folders(folder_path):
    subfolders = ["Unsorted", "Yes", "No", "Maybe"]
    for subfolder in subfolders:
        folder = os.path.join(folder_path, subfolder)
        os.makedirs(folder, exist_ok=True)

    # Move images to Unsorted folder
    for file in os.listdir(folder_path):
        if file.endswith(image_extensions):
            source = os.path.join(folder_path, file)
            destination = os.path.join(folder_path, "Unsorted", file)
            shutil.move(source, destination)

# Function to display image
def display_image(image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Create a label to display image if not already created
    if not hasattr(root, "image_label"):
        root.image_label = tk.Label(root)
        root.image_label.pack(fill="both", expand="yes")

    # Display image
    root.image_label.config(image=photo)
    root.image_label.image = photo # Keep a reference to avoid garbage collection

# Main execution
if __name__ == "__main__":
    # Select folder of photos to sort
    selected_folder = select_folder()

    if selected_folder:
        # Create list of unsorted images
        setup_folders(selected_folder)
        unsorted_folder = os.path.join(selected_folder, "Unsorted")
        images = [f for f in os.listdir(unsorted_folder) if f.lower().endswith(image_extensions)]

        # Display images one by one for sorting
        if images:
            image_path = os.path.join(unsorted_folder, images[0])
            display_image(image_path)

    # Start the main event loop
    root.mainloop()