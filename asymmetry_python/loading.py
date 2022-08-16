"""
Functions to facilitate the loading and sorting of images
"""
from cmath import nan
from skimage.io import imread
from pathlib import Path
from os import listdir
import numpy as np
from time import sleep
from tqdm import tqdm

def read_and_sort_files(folder_path):
    """Categorises the files from a folder into mutant or wild-type, ignoring heterozygous genotypes."""       
    print(' Loading images...')
    pbar = tqdm(total = len(listdir(folder_path)))
    mt_list = []
    wt_list = []
    for file_path in listdir(folder_path):
        sleep(0.02) 
        pbar.update(1)
        #input_image = imread(Path(folder_path + file_path)) 
        input_image = imread(folder_path + file_path)
        if file_path[:2] == "WT":
            wt_list.append(input_image) 
        elif file_path[:3] == "CF+":
            continue
        else: 
            mt_list.append(input_image) 
    return wt_list, mt_list

def image_dimensions(list_of_files):
    """ Recieves an image array and returns how many rows and columns it contains."""
    first_image = list_of_files[0]
    image_height = len(first_image)
    image_width = len(first_image[0])
    return image_width, image_height

def get_pixel_values_from_image_array(x_axis, y_axis, array_of_images):
    """At a specific XY coordinate in all image arrays, return a list of pixel values at the coordinate, if all values are 0, they are removed.

    Keyword arguments:
    x_axis -- the inputed x coordinate
    y_axis -- the inputed y coordinate
    array_of_images -- the array of images that will be indexed by the coordinates
    """
    result = []
    for image in array_of_images:
        result.append(image[y_axis][x_axis])
        if np.all(result) == 0:
            result = []
    return result


