from cmath import nan
from random import randint
import numpy as np
from processing import find_and_add_edge, scan_image_and_process, var_checked_p_value, threshold, total_significant_values

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

    image1 = np.array([[0, 0, 0],
                       [0, 1, 1],
                       [0, 1, 1],
                       [0, 5, 5]])

    image2 = np.array([[0, 0, 0],
                       [0, 3, 3],
                       [0, 5, 5],
                       [0, 15, 15]])
    
    expected = np.array([[nan, nan, nan],
                         [nan, 2, 2],
                         [nan, 3, 3],
                         [nan, 10, 10]])
    
    test_image_list = [image1, image2]
    median_diff_array, p_value_mask_array, test_median_image, wt_median_image = scan_image_and_process(test_image_list, test_image_list)
    test_median_image = np.array(test_median_image)
    assert np.allclose(test_median_image, expected, equal_nan=True)

def test_threshold():
    list_of_pixel_values = []
    thresholded_values = threshold(list_of_pixel_values)
    assert len(thresholded_values) == 0

    list_of_pixel_values = [nan, nan, nan]
    thresholded_values = threshold(list_of_pixel_values)
    assert len(thresholded_values) == 0

    list_of_pixel_values = [1,2,3,4,5]
    thresholded_values = threshold(list_of_pixel_values)
    assert thresholded_values == [1,2,3,4,5]

    list_of_pixel_values = [1,2,3,5,140,1,2,3,4,2]
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

    median_diff_array = np.array([[0, 0, 0, 0, 0],
                                  [0, 0, 1, 1, 1],
                                  [0, 0, 2, 2, 2],
                                  [0, 0, 3, 3, 3],
                                  [0, 0, 3, 3, 3],
                                  [0, 0, 3, 3, 3]])
    
    expected_diff_array = np.array([[0, 0, 0, 0, 0],
                                    [0, 0, 1, 1, 1],
                                    [0, 0, 2, 2, 2],
                                    [0, 0, 3, 3, 3],
                                    [0, 0, 3, 3, 3],
                                    [0, 0, 3, 3, 3]])

    p_value_mask = np.array([['None', 'None', 'None', 'None', 'None'],
                             ['None', 'None', 'pval', 'pval', 'pval'],
                             ['None', 'None', 'pval', 'pval', 'pval'],
                             ['None', 'None', 'pval', 'pval', 'pval'],
                             ['None', 'None', 'pval', 'pval', 'pval'],
                             ['None', 'None', 'pval', 'pval', 'pval']])
    
    expected_mask = np.array([['None', 'None', 'None', 'None', 'None'],
                              ['None', 'None', '#3CAEA3', '#3CAEA3', '#3CAEA3'],
                              ['None', 'None', '#3CAEA3', 'pval', 'pval'],
                              ['None', 'None', '#3CAEA3', 'pval', 'pval'],
                              ['None', 'None', '#3CAEA3', 'pval', 'pval'],
                              ['None', 'None', '#3CAEA3', 'pval', 'pval']])
    
    
    

    p_value_mask, median_diff_array = find_and_add_edge(median_diff_array,  p_value_mask, 1, '#3CAEA3')

    assert len(p_value_mask) == 6
    assert len(p_value_mask[0]) == 5
    assert len(median_diff_array) == 6
    assert len(median_diff_array[0]) == 5
    print(median_diff_array)
    print(expected_diff_array)
    print(p_value_mask)
    print(expected_mask)
    assert np.array_equal(median_diff_array, expected_diff_array)
    assert np.array_equal(p_value_mask, expected_mask)

def test_total_significant_values():
    image_height = 10
    image_width = 5

    median_diff_array = np.array([[nan for x in range(image_width)] for y in range(image_height)])
    p_value_mask = np.array([['None' for x in range(image_width)] for y in range(image_height)], dtype = object)

    median_diff_array[:,2:] = randint(1,15)


    p_value_mask[0,2:] = '#ED553B'
    p_value_mask[1,2:] = '#F6D55C'
    p_value_mask[2,2:] = '#ED553B'
    p_value_mask[3,2:] = '#ED553B'
    p_value_mask[4,2:] = '#ED553B'

    wt_sig, mt_sig = total_significant_values(p_value_mask, median_diff_array)
    
    assert wt_sig == 40
    assert mt_sig == 10