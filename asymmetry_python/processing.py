"""
Functions that scan the images and run different calculations on them
"""
from cmath import isnan, nan
from asymmetry_python.loading import image_dimensions, get_pixel_values_from_image_array
import numpy as np
from scipy import stats


def find_and_add_edge(median_diff_array,  p_value_mask, line_width, colour, value):
    ''' Compares the median difference array against the p value mask, finds the first non-zero value
    and replaces the value added with "line_width" with either a colour or a value, depending on the array type.
    Returns the same arrays, but with a highlighted edge.

    Keyword arguments:
    median_diff_array -- filtered median difference array
    p_value_mask -- mask for median difference array, with p-values coloured depending on WT or MT
    line_width -- size of edge
    colour -- colour of edge
    value -- value for median diff edge replacement
    '''
    for y_axis in range(len(median_diff_array)): 
        nan_indices = np.where(np.isnan(median_diff_array[y_axis]))
        if len(nan_indices[0]) > 0:
            first_value_index = nan_indices[0][-1] + 1
            indexed_line_width = first_value_index + line_width
            p_value_mask[y_axis,first_value_index:indexed_line_width] = colour
            median_diff_array[y_axis,indexed_line_width-4:indexed_line_width+4] = nan
            median_diff_array[y_axis,first_value_index:indexed_line_width] = value
        else:
            p_value_mask[y_axis,0:5] = colour
            
    return p_value_mask, median_diff_array

def threshold(list_of_pixel_values):
    ''' checks the list and returns it if there are no outliers, otherwise, returns an empty list.'''
    if len(list_of_pixel_values) != 0 or not np.all(np.isnan(list_of_pixel_values)):
        sdev = np.std(list_of_pixel_values)
        mean = np.mean(list_of_pixel_values)
        co_of_var = sdev/mean
        if co_of_var < 1.4:
            return list_of_pixel_values
        else:
            return []
    else:
        return []

def var_checked_p_value(wt_pixels, mt_pixels):
    """ Checks the distribution of wt_pixels and mt_pixels, if equally distributed, it updates the variance variable
    for the P_value. Returns the P_value from a ttest in which the mean of the wt distribution is less than the MT.

    Keyword arguments:
    wt_pixels -- A list of pixel values at a specific coordinate from the WT images.
    mt_pixels -- A list of pixel values at a specific coordinate from the MT images.
    alt_answer -- Determined by a pilot study, defines the alternative hypothesis.
    """
    if np.mean(wt_pixels) >= np.mean(mt_pixels):
        name_of_higher_mean_embryos = 'wt_mean'
    else:
        name_of_higher_mean_embryos = 'mt_mean'
    
    _, unchecked_p_value = stats.levene(wt_pixels, mt_pixels)
    if unchecked_p_value < 0.05:
        variance = False
    else:
        variance = True
    p_value = stats.ttest_ind(wt_pixels, mt_pixels, equal_var = variance).pvalue
    return p_value, name_of_higher_mean_embryos

def scan_image_and_process(wt_files, mt_files):
    """ From the list of WT and MT files, scans through each image pixel and assigns the values to a seperate list, at a certain x and y coordinate.
    These lists have their medians calculated and commited to a new 2D array, at the same coordinate the values were retrieved.
    The list of pixel values from both WT and MT are compared via a t-test, depending on whether the mean is higher for either WT or MT, it is assigned a colour.
    Empty lists are removed to prevent runtime-errors

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

            if len(wt_image_pixels) >=2 and len(mt_image_pixels) >=2:

                median_wt = np.median(wt_image_pixels)
                median_mt = np.median(mt_image_pixels)

                wt_median_image[current_y_axis][current_x_axis] = median_wt
                mt_median_image[current_y_axis][current_x_axis] = median_mt

                median_diff_array[current_y_axis][current_x_axis] = median_mt-median_wt

                p_value, name_of_higher_mean_embryos = var_checked_p_value(wt_image_pixels, mt_image_pixels)
                if p_value <= 0.05:
                    if name_of_higher_mean_embryos == 'wt_mean':
                        p_value_mask_array[current_y_axis][current_x_axis] = '#F6D55C' 
                    else:
                        p_value_mask_array[current_y_axis][current_x_axis] = '#ED553B'
                            
            # empty lists are removed to avoid runtime errors.
            else:
                mt_median_image[current_y_axis][current_x_axis] = nan
                wt_median_image[current_y_axis][current_x_axis] = nan
                median_diff_array[current_y_axis][current_x_axis] = nan

    return median_diff_array, p_value_mask_array, mt_median_image, wt_median_image

