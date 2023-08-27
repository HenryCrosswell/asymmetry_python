"""
Functions to aid in the plotting of created 2D arrays
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import matplotlib as mpl
from asymmetry_python.processing import find_and_add_edge
import os

def custom_gaussian_filter(image_array, sigma = 4, truncate = 4):
    """
    Filters a given array excluding nan values more effectively than the normal gaussian function.

    Args:
        image_array : The chosen image array that will undergo filtering.
        sigma : The range at which the filter averages the values, default to 4.
        truncate : The decimal places at which the average is cut off, default to 4.

    Returns:
        image_array with guassian filter applied.
    """

    # Create a copy of the input array and replace NaN values with zeros
    image_np_array = np.array(image_array)
    copy_of_np_array = image_np_array.copy()
    copy_of_np_array[np.isnan(image_np_array)] = 0
    
    # Apply Gaussian filter to the copy of the array
    gaussian_filter_of_original_array = gaussian_filter(copy_of_np_array, sigma=sigma, truncate=truncate)

    # Create a mask of non-NaN values (1 for non-NaN, 0 for NaN)
    non_zero_np_array = 0 * image_np_array.copy() + 1
    non_zero_np_array[np.isnan(image_np_array)] = 0
    
    # Apply Gaussian filter to the mask to count non-NaN values
    gaussian_filter_of_non_zero_array = gaussian_filter(non_zero_np_array, sigma=sigma, truncate=truncate)

    # Divide the filtered array by the Gaussian-filtered non-zero count array
    combination_of_arrays = gaussian_filter_of_original_array / gaussian_filter_of_non_zero_array

    print(combination_of_arrays)
    
    return combination_of_arrays



def create_plots(
        median_diff_array, p_value_mask_array, mt_median_image, wt_median_image, 
        file_save_path, elevation, azimuth, dpi, edge_colour, edge_line_width):
    """
    From four different 2D arrays this function creates two 3D plots, edited by some parameters.
    One of the significant P_values masking the the median_diff_array, showing signficance where WT is compared with MT, 
    with an edge drawn around the neuropore for visualisation.
    For the median plots, the WT and MT images are plotted on top of each other to show differences in symmetry.

    Args:
        median_diff_array : 2D array of the MT values subtracted from WT values.
        p_value_mask_array : 2D string array containing different colours for where WT or MT values were significantly different.
        mt_median_image : 2D array of the MT values.
        wt_median_image : 2D array of the WT values.
        file_save_path : Location for resulting graphs to be saved.
        elevation : This value represents the vertical rotation of the viewed and saved image.
        azimuth : This value represents the horizontal rotation of the viewed and saved image.
        dpi : dots per inch - a measure of the images' quality.

    Returns:
        p_value_plot : 3D plot of the median diff array with areas highlighted to display genotypes significant tissue asymmetry.
        median_plot : 3D plot of MT and WT surface plots, displaying the difference in shape of the average PNP, between WT and MT.
    """

    plot3Dp_values(median_diff_array, p_value_mask_array, elevation, azimuth, edge_colour, edge_line_width)
    plt.savefig(os.path.join(file_save_path, f'p_value_plot_a{azimuth}_e{elevation}.png'), dpi=dpi)

    plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth)
    plt.savefig(os.path.join(file_save_path, f'median_plot_a{azimuth}_e{elevation}.png'), dpi=dpi)


def plot3Dp_values(median_diff_array, p_value_mask, elevation, azimuth, edge_colour, edge_line_width = 5):
    """
    Surface plots the difference in median values onto an X,Y,Z axis, smooths the image and extends the Y axis to a representitive size. 
    Following this, applys either a Red mask if the P_value for the mutant is significant, or a Blue mask if the wild-type is significant.
    
    Keyword arguments:
    median_diff_array : A 2D array, containing the difference in median values between indivual pixels for the mutant images and wild-type.
    p_value_mask : A 2D array, containing colour-coordinated strings in which significant mutant and WT P_values are coloured differently to non-sig values.
    elevation : This value represents the vertical rotation of the viewed image.
    azimuth : This value represents the horizontal rotation of the viewed image.
    edge_colour : Chosen colour for the line drawn around the edge of the average PNPs.
    edge_line_width: Thickness of line drawn, defualt 5px.
    """

    # Applys a gaussian filter to the inputed 2D arrays - also finds the edge and applys that to the image.
    image_height = len(median_diff_array)
    image_width = len(median_diff_array[0])

    # Using default settings as it helps smooth without creating new data when using large images.
    median_diff_array = custom_gaussian_filter(median_diff_array)
    p_value_mask, median_diff_edge_array = find_and_add_edge(median_diff_array,  p_value_mask, edge_line_width, edge_colour)

    # Creates the skeleton of figure, in which we will add plots.
    # figsize was chosen to be a large window, allowing easy viewing.
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8,6))
    ax.set(xlim=(0, image_width), ylim=(0, image_height))
    X, Y = np.meshgrid(range(image_width), range(image_height))
    ax.set_aspect('auto')
    plt.rcParams.update({'font.family':'Calibri'})

    # Stretches plot along the Y axis by a determined scale factor - makes it more representative.
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

