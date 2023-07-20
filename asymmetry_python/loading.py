"""
Functions to facilitate the loading and sorting of images
"""

from skimage.io import imread
from pathlib import Path
from os import listdir
from tqdm import tqdm

def read_and_sort_files(folder_path):
    """Categorises the files from a folder into mutant or wild-type, ignoring heterozygous genotypes."""       
    print(' Loading images...')
    pbar = tqdm(total = len(listdir(folder_path)))
    mt_list = []
    wt_list = []
    for file_path in listdir(folder_path):
        pbar.update(1)
        input_image = imread(Path(folder_path, file_path)) 
        if file_path[:2] == "WT":
            wt_list.append(input_image) 
        elif file_path[:3] == "CF+":
            continue
        else: 
            mt_list.append(input_image) 
    return wt_list, mt_list

def image_dimensions(image_array):
    """Returns the number of rows and columns in the image array.

    Args:
        image_array (ndarray): Array of images.

    Returns:
        tuple: Image width and height.
    """
    first_image = image_array[0]
    image_height = len(first_image)
    image_width = len(first_image[0])
    return image_width, image_height

def get_pixel_values_from_image_array(x_coord, y_coord, array_of_images):
    """Returns a list of pixel values at a specific XY coordinate in all image arrays.

    If all pixel values are 0, they are removed from the list.

    Args:
        x_coord (int): X-coordinate.
        y_coord (int): Y-coordinate.
        array_of_images (list): Array of images.

    Returns:
        list: List of pixel values at the specified coordinate.
    """
    result = [image[y_coord, x_coord] for image in array_of_images]
    if all(value == 0 for value in result):
        result = []
    return result
