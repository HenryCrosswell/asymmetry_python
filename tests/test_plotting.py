from cmath import nan
import numpy as np
from asymmetry_python.plotting import gaussian_filter, plot3Dp_values

def test_gaussian_filter():
    image_array = np.array([[nan,1,nan,3,4,5],[nan,1,nan,3,4,5],[nan,1,nan,3,4,5],[nan,1,nan,3,4,5]])
    altered_image = gaussian_filter(image_array, 2, 4)
 
    assert image_array.shape == altered_image.shape
    assert np.all(altered_image) != nan


def test_plot3Dp_values():
    median_diff_array = np.ones(shape=(3, 3))*5
    p_value_mask = np.array([['blue' for x in range(3)] for y in range(3)], dtype = object)
    for i in range(3):
        if i%1  == 0:
            p_value_mask[i,i] = 'green'
    
    plot = plot3Dp_values(median_diff_array, p_value_mask, 10, 20)

def test_plot3Dmedians():
    pass
