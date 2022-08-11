from cmath import nan
from random import randint
from statistics import median
import numpy as np
from asymmetry_python.processing import find_and_add_edge, scan_image_and_process, var_checked_p_value, threshold
from scipy import stats
import sys

def test_scan_image_and_process():

    mt_test_image_list = [np.ones(shape=(3, 3)), np.ones(shape=(3, 3))*5]
    wt_test_image_list = [np.ones(shape=(3, 3)), np.ones(shape=(3, 3))*3]

    median_diff_array, p_value_mask_array, mt_median_image, wt_median_image = scan_image_and_process(wt_test_image_list, mt_test_image_list)
    median_diff_array = np.array(median_diff_array)
    p_value_mask_array = np.array(p_value_mask_array)
    mt_median_image = np.array(mt_median_image)
    wt_median_image = np.array(wt_median_image)

    assert wt_median_image.shape == mt_test_image_list[0].shape
    assert mt_median_image.shape == mt_test_image_list[0].shape
    assert p_value_mask_array.shape == mt_test_image_list[0].shape
    assert median_diff_array.shape == mt_test_image_list[0].shape
    assert np.all(mt_median_image == 3)
    assert np.all(wt_median_image == 2)
    assert np.all(median_diff_array == 1)
    assert np.all(p_value_mask_array) == 'None'

def test_threshold():
    list_of_pixel_values = []
    thresholded_values = threshold(list_of_pixel_values)
    assert len(thresholded_values) == 0

    list_of_pixel_values = [1,2,3,4,5]
    thresholded_values = threshold(list_of_pixel_values)
    assert thresholded_values == [1,2,3,4,5]

    list_of_pixel_values = [1,2,3,5,56,1,2,3,4,2]
    thresholded_values = threshold(list_of_pixel_values)
    assert len(thresholded_values) == 0
 

def test_var_checked_p_value():
    wt_test = [0,1,2,3,4,4,2,1]
    mt_test = [5,23,2,12,13,2,9,30]

    p_value, name_of_higher_mean_embryos = var_checked_p_value(wt_test, mt_test)

    assert p_value < 0.05
    assert name_of_higher_mean_embryos == 'mt_mean'

    wt_test = [5,23,2,12,13,2,9,30]
    mt_test = [0,1,2,3,4,4,2,1]
    p_value, name_of_higher_mean_embryos = var_checked_p_value(wt_test, mt_test)

    assert p_value < 0.05
    assert name_of_higher_mean_embryos == 'wt_mean'


def test_find_and_add_edge():
    # path = open('C:\\Users\\henry\\Desktop\\median.csv')
    # median_diff_array = np.loadtxt(path, delimiter=",")
    # image_height = len(median_diff_array)
    # image_width = len(median_diff_array[0])

    image_height = 30
    image_width = 20
    median_diff_array = np.array([[nan for x in range(image_width)] for y in range(image_height)])
    
    p_value_mask = np.array([['None' for x in range(image_width)] for y in range(image_height)], dtype = object)

    for y_index in range(image_height):
        for index in range(10):
            index += 10
            p_value_mask[y_index,index:] = 'p_value'
            median_diff_array[y_index,index] = randint(1,15)

    p_value_mask, median_diff_array = find_and_add_edge(median_diff_array,  p_value_mask, 5, '#3CAEA3', 0)

    assert len(p_value_mask) == 30
    assert len(p_value_mask[0]) == 20
    assert p_value_mask[0][10] == '#3CAEA3'
    assert p_value_mask[2][10] == '#3CAEA3'
    assert p_value_mask[12][10] == '#3CAEA3'
    assert p_value_mask[0][0] == 'None'
    assert p_value_mask[13][0] == 'None'
    assert p_value_mask[0][-2] == 'p_value'
    assert p_value_mask[8][-1] == 'p_value'
    assert len(np.where(p_value_mask[8] == '#3CAEA3')[0]) == 5

    assert len(median_diff_array) == 30
    assert len(median_diff_array[0]) == 20
    assert median_diff_array[0][10] == 0
    assert median_diff_array[2][10] == 0
    assert median_diff_array[12][10] == 0
    assert np.isnan(median_diff_array[0][0])
    assert np.isnan(median_diff_array[13][0])
    assert type(median_diff_array[0][-2]) == np.float64 and median_diff_array[0][-2] != 0
    assert type(median_diff_array[8][-1]) == np.float64 and median_diff_array[8][-1] != 0
    assert len(np.where(median_diff_array[8] == 0)[0]) == 5

