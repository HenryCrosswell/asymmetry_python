"""Script that sorts images and creates a 3D topographic representation visulising signficant tissue difference"""
from cmath import nan
from utils import read_image, get_pixel_values_from_image_array, read_and_sort_files, biggest_value, plot3Dp_values, plot3Dmedians, var_checked_p_value
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from skimage.transform import rescale
#real = adjusted_pixel_distance_python

folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"

#creates lists that will be filled with an array of images, depending on whether they are wt or mt
wt_files = []
mt_files = []
smallest_value = 0
largest_pixel_value = 0

#reads folder_path, assigns image arrays to either wt or mt
read_and_sort_files(folder_path, wt_files, mt_files)

#returns reference height and width
first_image = wt_files[0]
image_height = len(first_image)
image_width = len(first_image[0])

#creates a 2D array that is the width and height of the reference image
result = [[nan for x in range(image_width)] for y in range(image_height)]

#total_result = [[0 for x in range(image_width)] for y in range(image_height)]
p_value_mask = np.array([['#3CAEA300' for x in range(image_width)] for y in range(image_height)], dtype = object)

mt_median_image = [[nan for x in range(image_width)] for y in range(image_height)]
wt_median_image = [[nan for x in range(image_width)] for y in range(image_height)]

#outside loop is for y axis, inside is for x. Therefore, every time it loops through an x axis the y axis ticks down once
for current_y_axis in range(image_height):
    for current_x_axis in range(image_width):

        #returns a list of values at the current x and y coordinate for either the wt or mt images. 
        wt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, wt_files)
        mt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, mt_files)
        
        median_wt = np.median(wt_image_pixels)
        median_mt = np.median(mt_image_pixels)
        #at the specific pixel value, assesses distributions of both image pixels, if the mean of the WT is greater than the mutant = the P_value is more significant
        wt_p_value = var_checked_p_value(wt_image_pixels, mt_image_pixels, 'greater')
        mt_p_value = var_checked_p_value(wt_image_pixels, mt_image_pixels, 'less')

        mt_median_image[current_y_axis][current_x_axis] = median_mt
        wt_median_image[current_y_axis][current_x_axis] = median_wt
        
        total_median_values = median_mt-median_wt
        result[current_y_axis][current_x_axis] = total_median_values
        
        if mt_p_value <= 0.05:
            p_value_mask[current_y_axis][current_x_axis] = '#ED553B'#'#933D86' 
        if wt_p_value <= 0.05:
            p_value_mask[current_y_axis][current_x_axis] = '#F6D55C' #'#F178C3'

plot3Dp_values(result, p_value_mask)
#plot3Dmedians(mt_median_image, wt_median_image)

plt.show()