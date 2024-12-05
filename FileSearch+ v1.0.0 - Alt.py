# -*- coding: utf-8 -*-
"""
Created on Sat Nov 2  2024

Last modified on Thu Nov 21 2024

@author: Hao Wu, Henry Volodin, Jennie Cha
"""

### 1.import needed libraries
import sys
import subprocess
import pkg_resources

# Define the required packages
required = {'pillow', 'torch', 'ipython'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

# Install missing packages
if missing:
    try:
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing])
        print(f"Installed missing packages: {', '.join(missing)}")
    except subprocess.CalledProcessError as e:
        error = tk.Tk() 
        error.attributes("-topmost", True) 
        error.geometry("950x450")  
        error.title("Error")
        w = tk.Label(error, text="Unable to install packages, please try again.")
        w.pack()
        sys.exit(1)

# Import libraries
import os
from PIL import Image, ImageTk
import torch
from IPython.display import display
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

### 2.Predefined detection model that can detect 80 objects
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')    # Load yolov5 image detection model

# 80 objects that the image detection model can detect
suggestions = ["person", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear",
               "zebra", "giraffe", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
               "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", 
               "bench", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", 
               "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", 
               "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", 
               "donut", "cake", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", 
               "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", 
               "teddy bear", "hair drier", "toothbrush", "backpack", "umbrella", "handbag", "tie", 
               "suitcase", "frisbee", "skis", "snowboard", "sports ball", "frisbee", "bed", "toilet",
               "mirror", "chair", "sofa", "potted plant"
               ]




### 3.Main GUI window
root = tk.Tk() 
root.attributes("-topmost", True) 
root.geometry("950x450")  
root.title("FileSearch+")

# User instruction
w = tk.Label(root, text="Welcome to FileSearch+")
w.pack()
w = tk.Label(root, text="Begin by entering the object you\n wish to find in your images")
w.pack()
w = tk.Label(root, text="Currently, only a few objects are\n programed, such as person, car, or dog")
w.pack()




### 4.Show suggested objects when user types something
# Function that show the top 5 suggestion
def show_suggestions(*args):
    query = object_input.get().strip()
    if query:
        matches = [item for item in suggestions if query.lower() in item.lower()]
        suggestion_list.set(matches[:5])  # Show top 5 matches
    else:
        suggestion_list.set([])  # Clear suggestions if input is empty
        
# GUI entry that allows user to enter object name
object_input = tk.StringVar()
object_input.trace_add("write", show_suggestions)  # When user type something, show suggestions
entry = tk.Entry(root, textvariable=object_input, width=40)
entry.pack()

# GUI list show 5 suggestions
suggestion_list = tk.StringVar()
listbox = tk.Listbox(root, listvariable=suggestion_list, height=5, width=40)
listbox.pack()




### 5.Get selected object by clicking
# Function that get selected object into entry 
def get_suggestion(event):
    selected_object = listbox.get(listbox.curselection())  # Get the selected item
    object_input.set(selected_object)  # Set the selected item in the Entry field
    suggestion_list.set([])  # Clear the listbox

# Bind "click" operation to get_suggestion function
listbox.bind("<<ListboxSelect>>", get_suggestion)




### 5.Get object name and path for model
# Function that get object name that user wants to detect
def get_object_name():     
    global object_name
    object_name = entry.get().strip()
    root.destroy()

# GUI button that get object name
ttk.Button(root, text= "Analyze Photos for Object",width= 40, command = get_object_name).pack(pady=20)

# User instruction
w = tk.Label(root, text="Important Note: This image detection model\n is weaker than average to allow users to use\n this on less powerful computers. As such, this model\n may provide inacurate or partially correct answers\n due to this limitation.")
w.pack()

tk.mainloop()

# Select file path only after user type the object name
if object_name:
    directory_path = filedialog.askdirectory(title="Select a directory") 




### 6.Image detection
# Inilitize image path for image disply
image_paths = []

# Image detection 
for filename in os.listdir(directory_path):         
    if filename.lower().endswith(('.png','.jpg','.jpeg','.bmp','.tiff','.webp','.psd','.raw','.HEIC')):  # Check image extension
        file_path = os.path.join(directory_path,filename)   # Connect the image name and its path name
        img = Image.open(file_path)
        results = model(img)    # Detect objects in image using predefined model
        filtered_results = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == object_name]   #Put the images with detected objects into a variable
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



### 7.Display detected image in a gallery
# Initialize current image index
current_image_index = 0

# Function that display the image
def update_image():
    global current_image_index, image_label, image_display
    if image_paths:
        img_path = image_paths[current_image_index]
        image = Image.open(img_path)
        image = image.resize((1240, 660), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

# Function that show next image
def show_next_image():
    global current_image_index
    if current_image_index < len(image_paths) - 1:
        current_image_index += 1
        update_image()
        
# Function that show previous image
def show_previous_image():
    global current_image_index
    if current_image_index > 0:
        current_image_index -= 1
        update_image()


# Image disply GUI window
image_display = tk.Tk()
image_display.attributes("-topmost", True)
image_display.geometry("1620x900")
image_display.title("FileSearch+ Results")
image_label = ttk.Label(image_display)
image_label.pack()

# Previous image buttion
prev_button = ttk.Button(image_display, text="Previous", command=show_previous_image)
prev_button.pack(side=tk.LEFT, padx=10, pady=10)

# NeXT image button
next_button = ttk.Button(image_display, text="Next", command=show_next_image)
next_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Shoe image if images are found
if image_paths:
    update_image()
else:
    print("No images found that match the criteria.")

image_display.mainloop()
