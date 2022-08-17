from cgi import test
from cmath import nan
from random import randint
from statistics import median
import numpy as np
from asymmetry_python.loading import image_dimensions, read_and_sort_files, get_pixel_values_from_image_array
from os import listdir
from pathlib import Path

def test_image_dimensions():
    test_image_list = [np.ones(shape=(3, 4)), np.ones(shape=(3, 4))]
    width, height = image_dimensions(test_image_list)
    assert width == 4
    assert height == 3

def test_read_and_sort_files():
    test_folder_path = Path("./tests/data/")
    #point to test data path instead of th
    wt_list, mt_list = read_and_sort_files(test_folder_path)
    assert len(mt_list) == 2
    assert len(wt_list) == 2
    for im_array in wt_list: 
        image_pixel_row = im_array[26][:]
        x = np.count_nonzero(image_pixel_row == 252)
        assert x == 2
    for im_array in mt_list: 
        image_pixel_row = im_array[26][:]
        x = np.count_nonzero(image_pixel_row == 252)
        assert x == 4

def test_get_pixel_values_from_image_array():
    test_image_list = [np.ones(shape=(2, 2)), np.ones(shape=(2, 2)), np.ones(shape=(2, 2)), np.ones(shape=(2, 2)), np.zeros(shape=(2, 2))]
    for i, array in enumerate(test_image_list):
        array[:, 0] = i+1
    image_width, image_height = image_dimensions(test_image_list)

    for current_y_axis in range(image_height):
        for current_x_axis in range(image_width):
            result = get_pixel_values_from_image_array(current_x_axis, current_y_axis, test_image_list)
            result = np.array(result)
            if current_x_axis == 0:    
                assert result[0] == 1
                assert result[1] == 2
                assert result[2] == 3
                assert result[3] == 4
                assert result[4] == 5
                assert len(result) == 5
            if current_x_axis == 1:
                assert all(result) == 1
            assert all(result) != 0

