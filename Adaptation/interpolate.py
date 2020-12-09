import cv2
import numpy as np
from PIL import Image
import os

"""
Dilates sparse ground truth data from a Velodyne HDL-32E lidar scanner to provide a denser representation.

Arguments:
- Folder name of target 16-bit sparse ground truth.
- Dilation kernel size


Returns:
- Dilated 16-bit ground truth and percentage of valid ground truth pixels.
"""

folder = 'lidar_16_bit' #folder name containing sparse ground truth
kernel_size = 7 #set kernel size

for filename in sorted(os.listdir(folder)): #sorts filenames by number
    print(filename)
    if(filename == ".DS_Store"): #skip
        continue

    gt_png = np.array(Image.open(os.path.join(folder, filename)), dtype=int) #open each image as numpy array

    #get initial percentage of valid ground truth pixels
    total_pixels = gt_png.size
    print(total_pixels)
    valid_pixels = gt_png[gt_png!=0].size
    print(valid_pixels)
    print((valid_pixels/total_pixels)*100) 


    gt_png = gt_png/256 #recover original depth values
    gt_png = gt_png.astype('uint8') #convert to 8 bit int


    kernel = np.ones((kernel_size,kernel_size),np.uint8) #create kernel
    dilation = cv2.dilate(gt_png,kernel,iterations = 1) #perform dilation
    dilation = dilation *256 #convert back to 16-bit int
    dilation = dilation.astype('uint16')

    #get new percentage of valid ground truth pixels after dilation
    total_pixels = dilation.size
    print(total_pixels)
    valid_pixels = dilation[dilation!=0].size
    print(valid_pixels)
    print((valid_pixels/total_pixels)*100) 

    final_filename = filename 
    cv2.imwrite(final_filename, dilation) #write dilated ground truth to new file