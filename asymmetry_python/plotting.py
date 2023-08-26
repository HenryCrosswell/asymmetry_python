"""
Functions to aid in the plotting of created 2D arrays
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import scipy as sp
import matplotlib as mpl
from processing import find_and_add_edge
import os

def custom_gaussian_filter(image_array, sigma, truncate):
    """Filters a given array excluding nan values more effectively than the normal gaussian function.

    Args:
        image_array (ndarray): The chosen image array that will undergo filtering.
        sigma (float): The range at which the filter averages the values.
        truncate (float): The decimal places at which the average is cut off.

    Returns:
        ndarray: The filtered array.
    """
    # Create a mask of non-nan values
    valid_mask = ~np.isnan(image_array)
    
    # Create a copy of the input array and set nan values to zero
    image_copy = np.array(image_array)
    image_copy[np.isnan(image_array)] = 0
    
    # Apply Gaussian filter on the masked copy of the array
    gaussian_filter_of_original_array = gaussian_filter(image_copy, sigma=sigma, truncate=truncate)
    
    # Apply Gaussian filter on the mask to get the count of non-nan values at each location
    gaussian_filter_of_non_zero_array = gaussian_filter(valid_mask.astype(np.float32), sigma=sigma, truncate=truncate)
    
    # Avoid division by zero and apply the filter
    combination_of_arrays = np.divide(gaussian_filter_of_original_array, gaussian_filter_of_non_zero_array, out=np.zeros_like(image_array), where=gaussian_filter_of_non_zero_array != 0)
    
    return combination_of_arrays

def create_plots(median_diff_array, p_value_mask_array, mt_median_image, wt_median_image, file_save_path, elevation, azimuth):
    plot3Dp_values(median_diff_array, p_value_mask_array, elevation, azimuth)
    plt.savefig(os.path.join(file_save_path, f'none_my_plot_a{azimuth}_e{elevation}.png'), dpi=300)

    plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth)
    plt.savefig(os.path.join(file_save_path, f'bigmedian_diff_plot_a{azimuth}_e{elevation}.png'), dpi=300)


def plot3Dp_values(median_diff_array, p_value_mask, elevation, azimuth):
    """Surface plots the difference in median values onto an X,Y,Z axis, smooths the image and extends the Y axis to a representitive size. 
    Following this, applys either a Red mask if the P_value for the mutant is significant, or a Blue mask if the wild-type is significant.
    
    Keyword arguments:
    median_diff_array -- a 2D array, containing the difference in median values between indivual pixels for the mutant images and wild-type.
    p_value_mask -- a 2D array, containing colour-coordinated strings in which significant mutant and WT P_values are coloured differently to non-sig values.
    elevation -- an int determining the height at which the graph is viewed
    azimuth -- an int specifiying the rotation of the final graph
    """

    # Applys a gaussian filter to the inputed 2D arrays - also finds the edge and applys that to the image.
    image_height = len(median_diff_array)
    image_width = len(median_diff_array[0])
    median_diff_array = custom_gaussian_filter(median_diff_array, 4,4)
    p_value_mask, median_diff_edge_array = find_and_add_edge(median_diff_array,  p_value_mask, 5, '#3CAEA3')

    # Creates the skeleton of figure, in which we will add plots.
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8,6))
    ax.set(xlim=(0, image_width), ylim=(0, image_height))
    X, Y = np.meshgrid(range(image_width), range(image_height))
    ax.set_aspect('auto')
    plt.rcParams.update({'font.family':'Calibri'})

    # Stretches plot along the Y axis - makes it more representative.
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))

    # Fills the skeleton with a surface plot, with the Z axis being the med. diff. and a mask of the coloured p_values are applied.
    green_entries = np.where(p_value_mask=='#3CAEA3', p_value_mask, "None")
    ax.plot_surface(X,Y,np.zeros_like(median_diff_edge_array), rstride=1, cstride=1, facecolors=green_entries)
    
    all_not_green_entries = np.where(p_value_mask=='#3CAEA3', "None", p_value_mask)
    ax.plot_surface(X,Y,median_diff_edge_array, rstride=1, cstride=1, facecolors=all_not_green_entries)
    
    # Removes x, y and z ticks and sets z limit.
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.set_zlim(-40,40)
    
    # Sets the distance and rotation of the viewing angle for the plot.
    ax.view_init(elevation,azimuth)
    ax.dist = 7
    
    # Creates a figure legend
    median_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#3CAEA3', marker = 'o')
    wt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#ED553B', marker = 'o')
    mt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#F6D55C', marker = 'o')
    ax.legend([median_proxy, wt_proxy, mt_proxy], ['Median Difference', 'WT significance', 'MT signficance'], numpoints = 1, loc='upper left')


def plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth):
    """Surface plots both results onto an X,Y,Z axis, smooths the image and extends the Y axis to a representitive size.
    
    Keyword arguments:
    mt_median_image -- a 2D array, with median values of indivual pixels for the mutant images 
    wt_median_image -- a 2D array, with median values of indivual pixels for the wild-type images
    elevation -- an int determining the height at which the graph is viewed
    azimuth -- an int specifiying the rotation of the final graph
    """
    # Applys a gaussian filter to the inputed 2D arrays.
    image_height = len(wt_median_image)
    image_width = len(wt_median_image[0])
    wt_filtered_image = custom_gaussian_filter(wt_median_image, 1, 4)
    mt_filtered_image = custom_gaussian_filter(mt_median_image, 1, 4)

    # Creates the skeleton of figure, in which we will add plots.
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8,6))
    ax.set(xlim=(0, image_width), ylim=(0, image_height))
    X, Y = np.meshgrid(range(image_width), range(image_height))
    ax.set_aspect('auto')
    plt.rcParams.update({'font.family':'Calibri'})

    # Fills the skeleton with a surface plot of the wt median, stretches plot along the Y-axis to make it more representative.
    ax.plot_surface(X, Y, wt_filtered_image, color='#EDC194', antialiased=True, alpha = 0.8, rcount=200, ccount=200)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))
    

    # Fills the skeleton with a surface plot of the mt median, stretches plot along the Y-axis to make it more representative.
    ax.plot_surface(X, Y, mt_filtered_image,  color='#6A76B7', linewidth=0, antialiased=True, alpha = 0.8, rcount=200, ccount=200)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))
    
    # Sets the distance and rotation of the viewing angle for the plot.
    ax.dist=7
    ax.view_init(elevation,azimuth)

    # Removes x, y and z ticks and sets z limit.
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.set_zlim(0,70)

    # Creates a figure legend
    wt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#6A76B7', marker = 'o')
    mt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#EDC194', marker = 'o')
    ax.legend([wt_proxy, mt_proxy], ['WT median distance', 'Cre;Fl/Fl median distance'], numpoints = 1, loc='upper left')

