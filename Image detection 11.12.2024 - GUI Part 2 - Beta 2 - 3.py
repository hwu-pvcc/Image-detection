# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:51:58 2024

Last modified on Mon Nov 11 2024

@author: Hao Wu, Henry Volodin
"""
import os
from PIL import Image
import torch 
from IPython.display import display  
import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk
import tkinter
from pathlib import Path


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

root = tk.Tk() 
root.attributes("-topmost", True) 
root.geometry("750x250")  
root.title("FileSearch+")

w = tk.Label(root, text="Welcome to FileSearch+")
w.pack()
w = tk.Label(root, text="Begin by entering the object you\n wish to find in your images")
w.pack()
w = tk.Label(root, text="Currently, only a few objects are\n programed, such as person, car, or dog")
w.pack()


entry=tk.Entry(root, width= 40)
entry.focus_set()
entry.pack()


def display_text():     
    global object_name
    object_name = entry.get().strip()
    root.destroy()


ttk.Button(root, text= "Analyze Photos for Object",width= 40, command = display_text).pack(pady=20)

tk.mainloop()

directory_path = filedialog.askdirectory(title="Select a directory") 

image_paths = []  # List to store paths of images that match criteria
current_image_index = 0  # Track which image is currently displayed

# Directory path and criteria (assuming these variables are defined)

for filename in os.listdir(directory_path):         
    if filename.lower().endswith(('.png','.jpg','.jpeg','.bmp','.tiff')):
        file_path = os.path.join(directory_path,filename)
        img = Image.open(file_path)
        results = model(img)
        filtered_results = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == object_name] 
        if not filtered_results.empty:
            image_paths.append(file_path)
            print("image founded")
            try:
                display(img)
                if Path(file_path).exists():
                     Result = file_path
                else:
                    print("File does not exist:", file_path)
            except Exception as e:
                print(f"faild to show image: {e}")
        else:
            print("object not founded")
    else:
        print("data type error")

def update_image():
    global current_image_index, image_label, image_display
    if image_paths:
        # Open the current image and display it
        img_path = image_paths[current_image_index]
        image = Image.open(img_path)
        image = image.resize((750, 650), Image.LANCZOS)  # Resize to fit window
        photo = ImageTk.PhotoImage(image)
        
        # Update the label with the new image
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection

def show_next_image():
    global current_image_index
    if current_image_index < len(image_paths) - 1:
        current_image_index += 1
        update_image()

def show_previous_image():
    global current_image_index
    if current_image_index > 0:
        current_image_index -= 1
        update_image()

# Set up the tkinter window
image_display = tk.Tk()
image_display.attributes("-topmost", True)
image_display.geometry("750x750")
image_display.title("FileSearch+ Results")

# Label to display images
image_label = ttk.Label(image_display)
image_label.pack()

# Navigation buttons
prev_button = ttk.Button(image_display, text="Previous", command=show_previous_image)
prev_button.pack(side=tk.LEFT, padx=10, pady=10)

next_button = ttk.Button(image_display, text="Next", command=show_next_image)
next_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Display the first image if there are any matching images
if image_paths:
    update_image()
else:
    print("No images found that match the criteria.")

# Run the tkinter main loop
image_display.mainloop()



     
        
        
        
