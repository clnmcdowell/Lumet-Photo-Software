import tkinter as tk
from tkinter import filedialog
import os
import shutil
from PIL import Image, ImageTk

# Create a global window
root = tk.Tk()
root.title('Lumet Sorter')
root.config(bg="black") # Set background color to dark grey
root.attributes("-fullscreen", True) # Set window to full screen by default
root.withdraw()

# Supported image extensions
image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".ppm", ".pgm", ".pbm", ".pnm", ".sr", ".ras", ".jpe", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ico", ".cur", ".ani", ".tif", ".tiff", ".jfif", ".pjpeg", ".pjp")

# Global variables 
current_index = 0
images = []
selected_folder = ""
border_frame = None
counter_label = None

# Function to select folder of photos to sort
def select_folder():
    # Ask user to select folder of photos to sort
    folder_path = filedialog.askdirectory(title = "Select folder of photos to sort")
    if folder_path:
        print("Selected Folder: " + folder_path)
        return folder_path

# Function to setup folders and move photos to unsorted folder
def setup_folders(folder_path):
    subfolders = ["unsorted", "yes", "no", "maybe"]
    for subfolder in subfolders:
        folder = os.path.join(folder_path, subfolder)
        os.makedirs(folder, exist_ok=True)

    # Move images to unsorted folder
    for file in os.listdir(folder_path):
        if file.lower().endswith(image_extensions):
            source = os.path.join(folder_path, file)
            destination = os.path.join(folder_path, "unsorted", file)
            shutil.move(source, destination)

# Function to display image
def display_image(image_path):
    # Ensure image exists
    if not image_path or not os.path.exists(image_path):
        root.destroy()
        return
    
    image = Image.open(image_path)
    max_width, max_height = 1920, 1080
    image.thumbnail((max_width, max_height))  # Resize image while maintaining aspect ratio
    photo = ImageTk.PhotoImage(image)

    # Create a label to display image if not already created
    if not hasattr(root, "image_label"):
        root.image_label = tk.Label(border_frame, bg="black")
        root.image_label.pack(fill="both", expand="yes")

    # Display image
    root.image_label.config(image=photo)
    root.image_label.image = photo # Keep a reference to avoid garbage collection
    root.deiconify()

# Function to sort image
def sort_image(destination_folder):
    global current_index
    source = os.path.join(selected_folder, "unsorted", images[current_index])
    destination = os.path.join(selected_folder, destination_folder, images[current_index])
    shutil.move(source, destination)

    # Remove image from list and display next image
    if images:
        images.pop(current_index) 
        update_counter()
    if current_index < len(images):
        image_path = os.path.join(selected_folder, "unsorted", images[current_index])
        display_image(image_path)
    else:
        # No more images to sort: Delete unsorted folder if empty and exit
        unsorted_folder = os.path.join(selected_folder, "unsorted")
        if os.path.exists(unsorted_folder) and not os.listdir(unsorted_folder):
            os.rmdir(unsorted_folder)

        root.destroy()

# Function to blink border and sort image
def blink_border_and_sort(destination_folder, blink_color):
    blink_duration = 500 # milliseconds

    border_frame.config(bg=blink_color)
    root.after(blink_duration, lambda: border_frame.config(bg="black"))

    sort_image(destination_folder)

# Function to bind keys to sorting actions
def bind_keys():
    root.bind("<Left>", lambda event: blink_border_and_sort("no", "red"))      # Left arrow → no
    root.bind("<Right>", lambda event: blink_border_and_sort("yes", "green"))    # Right arrow → yes
    root.bind("<Up>", lambda event: blink_border_and_sort("maybe", "yellow"))     # Up arrow → maybe
    root.bind("<Down>", lambda event: blink_border_and_sort("maybe", "yellow"))   # Down arrow → maybe
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", not bool(root.attributes("-fullscreen")))) # Escape → toggle fullscreen

def update_counter():
    counter_label.config(text=f"Photos left: {len(images)}")

# Main execution
if __name__ == "__main__":
    # Select folder of photos to sort
    selected_folder = select_folder()

    if selected_folder:
        # Create list of unsorted images
        setup_folders(selected_folder)
        unsorted_folder = os.path.join(selected_folder, "unsorted")
        images = [f for f in os.listdir(unsorted_folder) if f.lower().endswith(image_extensions)]

        # Create border frame
        border_frame = tk.Frame(root, bg="black", bd=12)
        border_frame.pack(fill="both", expand="yes") 
        
        # Create remaining photo counter label
        counter_label = tk.Label(border_frame, text=f"Photos left: {len(images)}", bg="black", fg="white", font=("Helvetica", 16))
        counter_label.place(x=10, y=10)

        # Display first image and begin sort loop
        if images:
            display_image(os.path.join(unsorted_folder, images[current_index]))
            bind_keys()

    # Start the main event loop
    root.mainloop()