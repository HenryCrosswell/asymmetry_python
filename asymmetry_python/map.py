"""Script that sorts images and creates a 3D topographic representation visulising signficant tissue difference"""
from cmath import nan
from utils import read_image, get_pixel_values_from_image_array, read_and_sort_files, biggest_value, plot3D
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

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
result = [[0 for x in range(image_width)] for y in range(image_height)]

total_result = [[0 for x in range(image_width)] for y in range(image_height)]
mt_mask = [[nan for x in range(image_width)] for y in range(image_height)]
wt_mask = [[nan for x in range(image_width)] for y in range(image_height)]

#outside loop is for y axis, inside is for x. Therefore, every time it loops through an x axis the y axis ticks down once
for current_y_axis in range(image_height):
    for current_x_axis in range(image_width):

        #returns a list of values at the current x and y coordinate for either the wt or mt images. 
        wt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, wt_files)
        mt_image_pixels = get_pixel_values_from_image_array(current_x_axis, current_y_axis, mt_files)
        
        mean_wt = np.median(wt_image_pixels)
        mean_mt = np.median(mt_image_pixels)


        #at the specific pixel value, assesses distributions of both image pixels, if the mean of the WT is greater than the mutant = the P_value is more significant
        wt_p_value = stats.ttest_ind(wt_image_pixels, mt_image_pixels, alternative='greater').pvalue

        mt_p_value = stats.ttest_ind(wt_image_pixels, mt_image_pixels, alternative='less').pvalue

        if mean_wt == 0:
            mean_wt = nan
        if mean_mt == 0:
            mean_mt = nan
        total_result = mean_wt-mean_mt
        result[current_y_axis][current_x_axis] = total_result
        
        if mt_p_value <= 0.05:
            mt_mask[current_y_axis][current_x_axis] = mt_p_value
        if wt_p_value <= 0.05:   
            wt_mask[current_y_axis][current_x_axis] = wt_p_value
        #mt_result[currentYAxis][currentXAxis] = mean_mt
        #largest_pixel_value = biggest_value(largest_pixel_value, result)

plot3D(result, mt_mask, wt_mask)

plt.show()