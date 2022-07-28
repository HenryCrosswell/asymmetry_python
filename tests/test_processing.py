from statistics import median
import numpy as np
from asymmetry_python.processing import scan_image_and_process, var_checked_p_value
from scipy import stats

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
    assert np.all(p_value_mask_array) == '#3CAEA300'


def test_var_checked_p_value():
    """ Checks the distribution of wt_pixels and mt_pixels, if equally distributed, it updates the variance variable
    for the P_value. Returns the P_value from a ttest in which the mean of the wt distribution is less than the MT.

    Keyword arguments:
    wt_pixels -- A list of pixel values at a specific coordinate from the WT images.
    mt_pixels -- A list of pixel values at a specific coordinate from the MT images.
    alt_answer -- Determined by a pilot study, defines the alternative hypothesis.
    """
    'greater'
    wt_test = [0,1,2,3,4,4,2,1]
    mt_test = [5,1,2,12,13,2,9,30]

    wt_p_value = var_checked_p_value(wt_test, mt_test, 'greater')
    mt_p_value = var_checked_p_value(wt_test, mt_test, 'less')
    
    assert mt_p_value < 0.05
    assert wt_p_value > 0.05

    