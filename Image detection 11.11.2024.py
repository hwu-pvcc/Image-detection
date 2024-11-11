# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:23:28 2024

@author: Hao Wu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:51:58 2024

Last modified on Mon Nov 11 2024

@author: Hao Wu, Henry Volodin
"""
import os    # interact with operating system
from PIL import Image  #image procperessing library
import torch      #machine learning library
from IPython.display import display  
import tkinter as tk   #GUI library
from tkinter import ttk
from tkinter import filedialog

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')    #load yolov5 image detection model

root = tk.Tk()  #initialize the main tkinter window
root.attributes("-topmost", True) #make the window always on top
root.geometry("750x250")  #Set the geometry of Tkinter frame

#Create an Entry widget to accept User Input
entry=tk.Entry(root, width= 40)
entry.focus_set()
entry.pack()

#define a function to get directory path
def display_text():     
    global object_name
    object_name = entry.get().strip()
    root.destroy()

#Create a Button to validate Entry Widget
ttk.Button(root, text= "Okay",width= 20, command = display_text).pack(pady=20)

tk.mainloop()  #Start a tkinter event loop

directory_path = filedialog.askdirectory(title="Select a directory") #Select a dictory
  
#open contents in the designed file and detect these images
for filename in os.listdir(directory_path):         
    if filename.lower().endswith(('.png','.jpg','.jpeg','.bmp','.tiff')):
        file_path = os.path.join(directory_path,filename)
        img = Image.open(file_path)
        results = model(img)
        filtered_results = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == object_name]   #Put the images with detected objects into a variable 
#display image
        if not filtered_results.empty:
            print("image founded")
            try:
                display(img)
                print("image showed successful")
            except Exception as e:
                print(f"faild to show image: {e}")
        else:
            print("object not founded")
    else:
        print("data type error")





     
        
        
        
