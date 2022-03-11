#VERSION FOR MAC

import numpy as np
from skimage.io import show, imread, imshow
from pathlib import Path
import pandas as pd

input_image = imread(Path("C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\Pixel distance\\MAX_Result NVAH5 vert.tif"))

def image_mask(input_image):
    #returns an array of RGB values from the image in a 2D format
    tf_array = np.zeros(input_image.shape,dtype=bool)
    for i,row in enumerate(input_image):
        first_non_zero_index = (row!=0).argmax()
        #imagearray - specific row, column to the end of the array
        if first_non_zero_index != -1:
            tf_array[i,first_non_zero_index:] = True
            
    return tf_array
mask = image_mask(input_image)

df = pd.DataFrame({'booleans': mask.flatten(), 'values': input_image.flatten()}, columns=['booleans', 'values'])
true_image = df.loc[df['booleans'] == True, 'values']
print(np.mean(true_image.values))
print(np.std(true_image.values))
