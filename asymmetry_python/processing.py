"""
Functions that scan the images and run different calculations on them
"""

from cmath import nan
from asymmetry_python.loading import image_dimensions, get_pixel_values_from_image_array
import numpy as np
from scipy import stats
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def threshold(list_of_pixel_values):
    """
    Checks the list and returns it if there are no outliers, otherwise, returns an empty list.

    Args:
        list_of_pixel_values (list): List of pixel values.
    Returns:
        list: List of pixel values if no outliers, otherwise an empty list.
    """
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
    """Checks the distribution of wt_pixels and mt_pixels and returns the P_value from a ttest 
    in which the mean of the wt distribution is less than the MT.

    Args:
        wt_pixels (list): A list of pixel values at a specific coordinate from the WT images.
        mt_pixels (list): A list of pixel values at a specific coordinate from the MT images.
    Returns:
        tuple: P_value and name_of_higher_mean_embryos.
    """
    wt_mean = np.mean(wt_pixels)
    mt_mean = np.mean(mt_pixels)

    name_of_higher_mean_embryos = 'wt_mean' if wt_mean >= mt_mean else 'mt_mean'

    # Check variance using Levene's test
    _, unchecked_p_value = stats.levene(wt_pixels, mt_pixels)
    variance = unchecked_p_value >= 0.05

    # Perform t-test with or without equal variance assumption
    ttest_args = {'equal_var': variance}
    p_value = stats.ttest_ind(wt_pixels, mt_pixels, **ttest_args).pvalue

    return p_value, name_of_higher_mean_embryos

def total_significant_values(p_value_mask, median_diff_array):
    """Calculates percentage of WT and MT significance as a percentage of area.

    Args:
        p_value_mask (ndarray): P-value mask array.
        median_diff_array (ndarray): Median difference array.
    Returns:
        tuple: Percentage of WT and MT significance.
    """

    wt_color = '#ED553B'
    mt_color = '#F6D55C'

    # Count occurrences of WT and MT significant values
    wt_sig_count = np.count_nonzero(p_value_mask == wt_color)
    mt_sig_count = np.count_nonzero(p_value_mask == mt_color)

    # Calculate total non-NaN elements in median_diff_array
    total_non_nans = np.count_nonzero(~np.isnan(median_diff_array))
    # Calculate percentages
    wt_sig_percentage = (wt_sig_count / total_non_nans) * 100
    mt_sig_percentage = (mt_sig_count / total_non_nans) * 100

    return round(wt_sig_percentage, 2), round(mt_sig_percentage, 2)

def process_chunk(chunk):
    """Processes a chunk of the image and returns the results.

    Args:
        chunk (tuple): A tuple containing y_start, y_end, image_width, wt_files_chunk, and mt_files_chunk.
    Returns:
        tuple: Results of the processing for the chunk.
    """

    y_start, y_end, image_width, wt_files_chunk, mt_files_chunk = chunk

    mt_median_image_chunk = [[nan for _ in range(image_width)] for _ in range(y_start, y_end)]
    wt_median_image_chunk = [[nan for _ in range(image_width)] for _ in range(y_start, y_end)]
    median_diff_array_chunk = [[nan for _ in range(image_width)] for _ in range(y_start, y_end)]
    p_value_mask_array_chunk = np.array([['None' for _ in range(image_width)] for _ in range(y_start, y_end)], dtype=object)
   

    for current_y_axis in range(y_start, y_end):
        for current_x_axis in range(image_width):
            #returns a list of values at the current x and y coordinate for either the wt or mt images. 
            wt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, wt_files_chunk)
            mt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, mt_files_chunk)

            wt_image_pixels = threshold(wt_image_pixels)
            mt_image_pixels = threshold(mt_image_pixels)

            if len(wt_image_pixels) >=2:
                median_wt = np.median(wt_image_pixels)
                wt_median_image_chunk[current_y_axis - y_start][current_x_axis] = median_wt
            else:
                wt_median_image_chunk[current_y_axis - y_start][current_x_axis] = nan

            if len(mt_image_pixels) >=2:
                median_mt = np.median(mt_image_pixels)
                mt_median_image_chunk[current_y_axis - y_start][current_x_axis] = median_mt
            else:
                mt_median_image_chunk[current_y_axis - y_start][current_x_axis] = nan

            if len(mt_image_pixels) >=2 and len(wt_image_pixels) >=2:

                median_diff_array_chunk[current_y_axis - y_start][current_x_axis] = median_mt - median_wt
                p_value, name_of_higher_mean_embryos = var_checked_p_value(wt_image_pixels, mt_image_pixels)
                if p_value <= 0.05:
                    if name_of_higher_mean_embryos == 'wt_mean':
                        p_value_mask_array_chunk[current_y_axis - y_start][current_x_axis] = '#ED553B'
                    else:
                        p_value_mask_array_chunk[current_y_axis - y_start][current_x_axis] = '#F6D55C'
            else:
                median_diff_array_chunk[current_y_axis - y_start][current_x_axis] = nan
    
    return median_diff_array_chunk, p_value_mask_array_chunk, mt_median_image_chunk, wt_median_image_chunk

def scan_image_and_process(wt_files, mt_files):
    """
    Scans the images and runs different calculations on them.

    Args:
        wt_files : List of WT image file paths.
        mt_files : List of MT image file paths.
    Returns:
        tuple: Median difference array, p-value mask array, MT median image, and WT median image.
    """

    # Get image dimensions
    image_width, image_height = image_dimensions(wt_files)

    # Create chunks
    chunk_size = 41
    chunks = [(y, min(y + chunk_size, image_height), image_width, wt_files, mt_files) for y in range(0, image_height, chunk_size)]

    # Process chunks in parallel
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_chunk, chunks), total=len(chunks)))

    # Merge results from chunks
    median_diff_array_list, p_value_mask_array_list, mt_median_image_list, wt_median_image_list = zip(*results)
    median_diff_array = np.vstack(median_diff_array_list)
    p_value_mask_array = np.vstack(p_value_mask_array_list)
    mt_median_image = np.vstack(mt_median_image_list)
    wt_median_image = np.vstack(wt_median_image_list)

    return median_diff_array, p_value_mask_array, mt_median_image, wt_median_image


def find_and_add_edge(median_diff_array, p_value_mask, line_width, colour):
    """
    Compares the median difference array against the p value mask, finds the first non-zero value
    and replaces the value added with "line_width" with either a colour or a value, depending on the array type.
    Returns the same arrays, but with a highlighted edge.

    Args:
        median_diff_array : Filtered median difference array.
        p_value_mask : Coloured mask for median difference array, with p-values coloured depending on WT or MT.
        line_width : Size of edge.
        colour : Colour of edge.
    Returns:
        tuple: Updated p_value_mask and median_diff_array.
    """

    first_y_axis_line = True
    image_height = len(median_diff_array) 
    previous_first_right_value_index = -1
    previous_first_left_value_index = -1

    for y_axis in range(image_height): 

        # Returns all non_nan_indices in the current y_axis and continues if all are nan.
        non_nan_indices = np.where(~np.isnan(median_diff_array[y_axis]))
        if non_nan_indices[0].size == 0:
            continue

        first_left_value_index = non_nan_indices[0][-1]
        first_right_value_index = non_nan_indices[0][0]
        left_edge = first_left_value_index + line_width
        right_edge = first_right_value_index - line_width 

        # If this y-axis is the first to contain a non_nan_index, it paints the first line.
        if first_y_axis_line == True:
            first_y_axis_line = False

            left_index_of_first_line = first_left_value_index
            p_value_mask[y_axis,right_edge:left_edge] = colour

            previous_first_right_value_index = first_right_value_index
            previous_first_left_value_index = first_left_value_index

            continue

        # Right edge
        if first_y_axis_line == False:
            p_value_mask[y_axis,right_edge:max(previous_first_right_value_index, first_right_value_index)] = colour

        # Left edge
        if first_left_value_index >= left_index_of_first_line and y_axis < 1000:
            p_value_mask[y_axis,min(previous_first_left_value_index, first_left_value_index):left_edge] = colour

        # Embryo close to right border of image
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