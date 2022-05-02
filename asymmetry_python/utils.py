import numpy as np
from skimage.io import show, imread, imshow
from pathlib import Path
import pandas as pd
from os import listdir

def read_image(file_path):
    input_image = imread(Path(file_path))
    return input_image

def image_mask(input_image):
    #returns an array of RGB values from the image in a 2D format
    tf_array = np.zeros(input_image.shape,dtype=bool)
    for i,row in enumerate(input_image):
        first_non_zero_index = (row!=0).argmax()
        #imagearray - specific row, column to the end of the array
        if first_non_zero_index != -1:
            tf_array[i,first_non_zero_index:] = True
    return tf_array

def mean_and_stdev(masked_image_values):
    mean = np.mean(masked_image_values)
    st_dev = np.std(masked_image_values)
    return mean, st_dev

def get_pixel_values_from_image_array(xAxis, yAxis, array_of_images):
    result = []
    for image in array_of_images:
        imagePixelValue = image[yAxis][xAxis]
        result.append(imagePixelValue)
    return result

def read_and_sort_files(folder_path, wt_list, mt_list):
    for file_path in listdir(folder_path): 
        input_image = read_image(folder_path+file_path) 

        if file_path[:2] == "WT":
            wt_list.append(input_image) 
        else: 
            mt_list.append(input_image) 