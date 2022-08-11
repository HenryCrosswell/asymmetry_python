"""
Functions that scan the images and run different calculations on them
"""
from cmath import nan
from statistics import median, stdev
from asymmetry_python.loading import image_dimensions, get_pixel_values_from_image_array
import numpy as np
from scipy import stats

def find_and_add_edge_colour(median_diff_array,  p_value_mask, line_width, colour, value):
    for y_axis in range(len(median_diff_array)): 
        nan_indices = np.where(np.isnan(median_diff_array[y_axis]))
        if len(nan_indices[0]) > 0:
            first_value_index = nan_indices[0][-1] + 1
            indexed_line_width = first_value_index + line_width
            p_value_mask[y_axis,first_value_index:indexed_line_width] = colour
            median_diff_array[y_axis,first_value_index:indexed_line_width] = value
    return p_value_mask, median_diff_array

def threshold(list_of_pixel_values):
    sdev = np.std(list_of_pixel_values)
    mean = np.mean(list_of_pixel_values)
    co_of_var = sdev/mean
    if co_of_var < 1.4:
        return list_of_pixel_values
    else:
        return []

def downscale(image_array):
    from skimage.transform import downscale_local_mean
    x = np.array(image_array)
    image_downscaled = downscale_local_mean(x, (20, 20))
    return image_downscaled


def var_checked_p_value(wt_pixels, mt_pixels, alt_answer):
    """ Checks the distribution of wt_pixels and mt_pixels, if equally distributed, it updates the variance variable
    for the P_value. Returns the P_value from a ttest in which the mean of the wt distribution is less than the MT.

    Keyword arguments:
    wt_pixels -- A list of pixel values at a specific coordinate from the WT images.
    mt_pixels -- A list of pixel values at a specific coordinate from the MT images.
    alt_answer -- Determined by a pilot study, defines the alternative hypothesis.
    """
    _, unchecked_p_value = stats.levene(wt_pixels, mt_pixels)
    if unchecked_p_value < 0.05:
        variance = False
    else:
        variance = True
    p_value = stats.ttest_ind(wt_pixels, mt_pixels, equal_var = variance, alternative=alt_answer).pvalue
    return p_value

def scan_image_and_process(wt_files, mt_files):
    """ From the list of WT and MT files, scans through each image pixel and assigns the values to a seperate list, at a certain x and y coordinate.
    These lists have their medians calculated and commiited to a new 2D array, at the same coordinate the values were retrieved.
    The list of pixel values from both WT and MT are compared via a ttest, depending on whether the pixel is significant for either WT or MT, it is assigned a colour.

    Keyword arguments:
    wt_files -- A list of 2D arrays for each WT image
    mt_files -- A list of 2D arrays for each MT image
    """

    image_width, image_height = image_dimensions(wt_files)
    mt_median_image = [[nan for x in range(image_width)] for y in range(image_height)]
    wt_median_image = [[nan for x in range(image_width)] for y in range(image_height)]
    median_diff_array = [[nan for x in range(image_width)] for y in range(image_height)]
    p_value_mask_array = np.array([['None' for x in range(image_width)] for y in range(image_height)], dtype = object)
    for current_y_axis in range(image_height):
        for current_x_axis in range(image_width):

            #returns a list of values at the current x and y coordinate for either the wt or mt images. 
            wt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, wt_files)
            mt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, mt_files)
            
            wt_image_pixels = threshold(wt_image_pixels)
            mt_image_pixels = threshold(mt_image_pixels)

            #calculates the medians for a list of pixels
            median_wt = np.median(wt_image_pixels)
            median_mt = np.median(mt_image_pixels)
            median_diff = median_mt-median_wt

            #saves these medians in a 2D array the same coordinate they were retrieved
            if median_mt >= median_wt:
                mt_median_image[current_y_axis][current_x_axis] = median_mt
            elif median_mt < median_wt:
                wt_median_image[current_y_axis][current_x_axis] = median_wt

            median_diff_array[current_y_axis][current_x_axis] = median_diff
            
            #at the specific pixel value, assesses distributions of both image pixels, if the mean of the WT is greater than the mutant = the P_value is more significant
            wt_p_value = var_checked_p_value(wt_image_pixels, mt_image_pixels, 'greater')
            mt_p_value = var_checked_p_value(wt_image_pixels, mt_image_pixels, 'less')
            if mt_p_value <= 0.05:
                p_value_mask_array[current_y_axis][current_x_axis] = '#ED553B'
            if wt_p_value <= 0.05:
                p_value_mask_array[current_y_axis][current_x_axis] = '#F6D55C'
    
    return median_diff_array, p_value_mask_array, mt_median_image, wt_median_image

