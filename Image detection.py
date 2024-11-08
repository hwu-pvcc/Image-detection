# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:51:58 2024

Last modified on Fri Nov 8 2024

@author: Hao Wu
"""

import os    # interact with operating system
from PIL import Image  #image processing library
import torch      #machine learning library
from IPython.display import display  
import tkinter as tk   #GUI library
from tkinter import filedialog

root = tk.Tk()  #initialize the main tkinter window
root.withdraw()  #hide root window
root.attributes("-topmost", True) #make the window always on top

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')    #load yolov5 image detection model
object_name=input("Enter object you want to find ").strip()     #input object you want to detect
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
            print("Image founded")
            try:
                display(img)
                print("Image showed successful")
            except Exception as e:
                print(f"Faild to show image: {e}")
        else:
            print("Object not founded")
    else:
        
        print("There is no image in your file") 

        

     
        
        
        