"""
Functions that scan the images and run different calculations on them
"""

from cmath import nan
from loading import image_dimensions, get_pixel_values_from_image_array
import numpy as np
from scipy import stats
from time import sleep
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def find_and_add_edge(median_diff_array,  p_value_mask, line_width, colour):
    ''' Compares the median difference array against the p value mask, finds the first non-zero value
    and replaces the value added with "line_width" with either a colour or a value, depending on the array type.
    Returns the same arrays, but with a highlighted edge.

    Variable names follow the convention that left and right pertain to the image view, not the order in the array.

    Keyword arguments:
    median_diff_array -- filtered median difference array
    p_value_mask -- mask for median difference array, with p-values coloured depending on WT or MT
    line_width -- size of edge
    colour -- colour of edge
    '''
    first_y_axis_line = True
    previous_first_right_value_index = -1
    previous_first_left_value_index = -1
    for y_axis in range(len(median_diff_array)): 

        non_nan_indices = np.where(~np.isnan(median_diff_array[y_axis])) 
        if len(non_nan_indices[0]) != 0:
            first_left_value_index = non_nan_indices[0][-1]
            first_right_value_index = non_nan_indices[0][0]
            left_edge = first_left_value_index + line_width

            right_edge = first_right_value_index - line_width 

            #paints first line
            if first_y_axis_line == True:
                left_index_of_first_line = first_left_value_index
                p_value_mask[y_axis,right_edge:left_edge] = colour
                first_y_axis_line = False
                previous_first_right_value_index = first_right_value_index
                previous_first_left_value_index = first_left_value_index
                continue

            #right edge
            if first_y_axis_line == False:
                p_value_mask[y_axis,right_edge:max(previous_first_right_value_index, first_right_value_index)] = colour
                
            # left edge
            if first_left_value_index >= left_index_of_first_line and y_axis < 1000:
                p_value_mask[y_axis,min(previous_first_left_value_index, first_left_value_index):left_edge] = colour
            
            # embryo close to right border of image
            if first_right_value_index <= line_width:
                p_value_mask[y_axis,0:line_width] = colour

            previous_first_right_value_index = first_right_value_index
            previous_first_left_value_index = first_left_value_index

    # hack to deal with weird green values inside embryo:
    # replace the p value mask where it is green with nan for the problematic region
    p_value_mask[300:600, 300:500] = np.where(p_value_mask[300:600, 300:500]==colour, "None", p_value_mask[300:600, 300:500])
    
    # draw bottom line
    bottom_line = 1796
    bottom_offset = 3
    p_value_mask[bottom_line:bottom_line+bottom_offset,previous_first_right_value_index:499] = colour

    return p_value_mask, median_diff_array

def threshold(list_of_pixel_values):
    ''' checks the list and returns it if there are no outliers, otherwise, returns an empty list.'''
    if len(list_of_pixel_values) != 0 or not np.all(np.isnan(list_of_pixel_values)):
        sdev = np.std(list_of_pixel_values)
        mean = np.mean(list_of_pixel_values)
        co_of_var = sdev/mean
        if co_of_var < 2.5:
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
    wt_mean = np.mean(wt_pixels)
    mt_mean = np.mean(mt_pixels)
    
    if wt_mean >= mt_mean:
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

def total_significant_values(p_value_mask, median_diff_array):
    ''' calculates percentage of WT and MT significance as a percentage of area.'''

    wt_sig_values = len(np.where(p_value_mask == '#ED553B')[0])
    mt_sig_values = len(np.where(p_value_mask == '#F6D55C')[0])
    total_non_nans = np.count_nonzero(~np.isnan(median_diff_array))

    wt_sig_percentage = (wt_sig_values/total_non_nans)*100
    mt_sig_percentage = (mt_sig_values/total_non_nans)*100

    return round(wt_sig_percentage, 2), round(mt_sig_percentage,2)


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
    print(' Processing files...')
    pbar = tqdm(total = (image_height))

    wt_image_pixels_stack = np.stack(wt_files)
    mt_image_pixels_stack = np.stack(mt_files)

    for current_y_axis in range(image_height):
        sleep(0.02) 
        pbar.update(1)
        for current_x_axis in range(image_width):
            
            wt_image_pixels = wt_image_pixels_stack[:, current_y_axis, current_x_axis].tolist()
            mt_image_pixels = mt_image_pixels_stack[:, current_y_axis, current_x_axis].tolist()

            wt_image_pixels = threshold(wt_image_pixels)
            mt_image_pixels = threshold(mt_image_pixels)

            if len(wt_image_pixels) >=2:
                median_wt = np.median(wt_image_pixels)
                wt_median_image[current_y_axis][current_x_axis] = median_wt
            else:
                wt_median_image[current_y_axis][current_x_axis] = nan

            if len(mt_image_pixels) >=2:
                median_mt = np.median(mt_image_pixels)
                mt_median_image[current_y_axis][current_x_axis] = median_mt
            else:
                mt_median_image[current_y_axis][current_x_axis] = nan

            if len(mt_image_pixels) >=2 and len(wt_image_pixels) >=2:

                median_diff_array[current_y_axis][current_x_axis] = median_mt-median_wt
                p_value, name_of_higher_mean_embryos = var_checked_p_value(wt_image_pixels, mt_image_pixels)
                if p_value <= 0.05:
                    if name_of_higher_mean_embryos == 'wt_mean':
                        p_value_mask_array[current_y_axis][current_x_axis] = '#ED553B'
                    else:
                        p_value_mask_array[current_y_axis][current_x_axis] = '#F6D55C'
            else:
                median_diff_array[current_y_axis][current_x_axis] = nan
    
    return median_diff_array, p_value_mask_array, mt_median_image, wt_median_image

def worker(args):
    a, b = args
    res1 = a + b
    res2 = a * b

    return res1, res2

def image_scan_worker(args):
    a,b = args
    

def main():
    args1 = [1, 2, 3, 4]
    args2 = [5, 6, 7, 8]

    with ProcessPoolExecutor() as executor:
        result = executor.map(worker, zip(args1, args2))

    a, b = map(list, zip(*result))

    print(a, b)


if __name__ == "__main__":
    main()