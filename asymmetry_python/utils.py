import numpy as np
from skimage.io import show, imread, imshow
from pathlib import Path
import pandas as pd

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

def apply_mask(input_image, mask):
    df = pd.DataFrame({'booleans': mask.flatten(), 'values': input_image.flatten()}, columns=['booleans', 'values'])
    masked_image_df = df.loc[df['booleans'] == True, 'values']
    return masked_image_df.values

def mean_and_stdev(masked_image_values):
    mean = np.mean(masked_image_values)
    st_dev = np.std(masked_image_values)
    return mean, st_dev