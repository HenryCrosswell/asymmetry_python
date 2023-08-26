"""
Functions to facilitate the loading and sorting of images
"""

from skimage.io import imread
import os
from os import listdir
from tqdm import tqdm
import logging

def read_and_sort_files(folder_path):
    """
    Categorises the files from a folder into mutant or wild-type, ignoring heterozygous genotypes.
    
    Args:
        folder_path : The location of all images to be analysed, both WT and mutant genotypes.
    Returns as tuple:
        wt_list : Images with WT prefix are sorted into this list.
        mt_list : All other images except CF+ are sorted into this list.
    """       

    logging.info('Loading images...')  
    
    # Intialise lists 
    pbar = tqdm(total = len(listdir(folder_path)))
    mt_list = []
    wt_list = []

    try:
        for file_path in listdir(folder_path):
            if file_path == '.DS_Store':
                continue
            pbar.update(1)
            input_image = imread(os.path.join(folder_path, file_path)) 
            if file_path[:2] == "WT":
                wt_list.append(input_image) 
            elif file_path[:3] == "CF+":
                continue
            else:
                mt_list.append(input_image) 

    except ValueError as e:
        logging.error(f'Unexpected value encountered : {e}')

    except Exception as e:
        logging.error(f'An error has occured : {e}')

    return wt_list, mt_list

def image_dimensions(image_array):
    """
    Returns the number of rows and columns in the image array.

    Args:
        image_array : Array of images.
    Returns: 
        tuple : Image width and height.
    """

    first_image = image_array[0]   
    image_height = len(first_image)
    image_width = len(first_image[0])

    return image_width, image_height

def get_pixel_values_from_image_array(x_coord, y_coord, array_of_images):
    """
    Returns a list of pixel values at a specific XY coordinate in all image arrays.
    If all pixel values are 0, they are removed from the list.

    Args:
        x_coord : Current X-coordinate iteration.
        y_coord : Current Y-coordinate iteration.
        array_of_images : Array of images.
    Returns:
        result : List of pixel values at the specified coordinate.
    """
    try:
        result = [image[y_coord, x_coord] for image in array_of_images]
        if all(value == 0 for value in result):
            result = []
    except ValueError as e:
        logging.error(f'An error has occured : {e}')

    return result
