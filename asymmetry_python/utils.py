"""Functions for Asymmetry Project"""
import numpy as np
from skimage.io import show, imread, imshow
from pathlib import Path
from os import listdir
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy import stats
import scipy as sp
import matplotlib as mpl
import sys

def read_image(file_path):
    """Returns an image from the file path."""
    input_image = imread(Path(file_path))
    return input_image

def image_mask(input_image):
    """From the input image, returns a True/False array.
    
    True -- every value after the first non-zero
    False -- every zero value up until the first non-zero
    """
    tf_array = np.zeros(input_image.shape,dtype=bool)
    for i,row in enumerate(input_image):
        first_non_zero_index = (row!=0).argmax()
        if first_non_zero_index != -1:
            tf_array[i,first_non_zero_index:] = True
    return tf_array

def mean_and_stdev(masked_image_values):
    """Returns the mean and standard deviation of a 2D array."""
    mean = np.mean(masked_image_values)
    st_dev = np.std(masked_image_values)
    return mean, st_dev

def get_pixel_values_from_image_array(x_axis, y_axis, array_of_images):
    """At a specific XY coordinate in all image arrays, return a list of pixel values at the coordinate, removes 0 values.
    
    Keyword arguments:
    x_axis -- the inputed x coordinate
    y_axis -- the inputed y coordinate
    array_of_images -- the array of images that will be indexed by the coordinates
    """
    result = []
    for image in array_of_images:
        imagePixelValue = image[y_axis][x_axis]
        if imagePixelValue != 0:
            result.append(imagePixelValue)
    return result

def read_and_sort_files(folder_path, wt_list, mt_list):
    """Categorises the file into mutant or wild-type, ignoring heterozygous genotypes.

    Keyword arguments:
    folder_path -- the path from which the images will be obtained
    wt_list -- an empty list for all wild-type images
    mt_list -- an empty list for all mutant images
    """
    for file_path in listdir(folder_path): 
        input_image = read_image(folder_path+file_path) 
        if file_path[:2] == "WT":
            wt_list.append(input_image) 
        elif file_path[:3] == "CF+":
            continue
        else: 
            mt_list.append(input_image) 

def biggest_value(current_biggest_value, results):
    """Returns the value if it exceeds the current biggest value."""
    for value in results:
        result = np.argmax(value)
        if np.argmax(value) < current_biggest_value:
            return current_biggest_value
        else:
            return result


def plot3Dp_values(result, P_value_mask):
    """Surface plots the difference in median values onto an X,Y,Z axis, smooths the image and extends the Y axis to a representitive size. 
    Following this, applys either a Red mask if the P_value for the mutant is significant, or a Blue mask if the wild-type is significant.
    
    Keyword arguments:
    result -- a 2D array, with the diference in median values between indivual pixels for the mutant images and wild-type 
    mt_mask -- a 2D array, only containing values where the mutant P_value are below 0.05
    wt_mask -- a 2D array, only containing values where the wild-type P_value are below 0.05
    """
    image_height = len(result)
    image_width = len(result[0])
    
    sigma=2.0                  # standard deviation for Gaussian filter
    truncate=4.0               # truncate filter at this many sigmas
    
    U = np.array(result)

    V=U.copy()
    V[np.isnan(U)]=0
    VV=sp.ndimage.gaussian_filter(V,sigma=sigma,truncate=truncate)

    W=0*U.copy()+1
    W[np.isnan(U)]=0
    WW=sp.ndimage.gaussian_filter(W,sigma=sigma,truncate=truncate)

    Z = VV/WW

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8,6))
    ax.set(xlim=(0, image_width), ylim=(0, image_height))
    X, Y = np.meshgrid(range(image_width), range(image_height))
    ax.set_aspect('auto')
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, facecolors=P_value_mask, alpha = 0.6)
    ax.view_init(35, 110)
    ax.dist = 7
    median_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#3CAEA3', marker = 'o')
    wt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#F6D55C', marker = 'o')
    mt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#ED553B', marker = 'o')
    ax.legend([median_proxy, wt_proxy, mt_proxy], ['Median Difference', 'WT significance', 'MT signficance'], numpoints = 1, loc='upper left')

def plot3Dmedians(result, second_result):
    """Surface plots both results onto an X,Y,Z axis, smooths the image and extends the Y axis to a representitive size.
    
    Keyword arguments:
    mt_result -- a 2D array, with median values of indivual pixels for the mutant images 
    wt_result -- a 2D array, with median values of indivual pixels for the wild-type images
    """
    image_height = len(result)
    image_width = len(result[0])
    filtered_Z_value = {}

    sigma=10                  # standard deviation for Gaussian filter
    truncate=4.0               # truncate filter at this many sigmas

    function_list = [result, second_result]
    for i, which_image in enumerate(function_list):
        U = np.array(which_image)

        V=U.copy()
        V[np.isnan(U)]=0
        VV=sp.ndimage.gaussian_filter(V,sigma=sigma,truncate=truncate)

        W=0*U.copy()+1
        W[np.isnan(U)]=0
        WW=sp.ndimage.gaussian_filter(W,sigma=sigma,truncate=truncate)

        filtered_Z_value["image {0}".format(i+1)] = VV/WW

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8,8))
    ax.set(xlim=(0, image_width), ylim=(0, image_height))
    X, Y = np.meshgrid(range(image_width), range(image_height))
    ax.set_aspect('auto')
    ax.plot_surface(X, Y, filtered_Z_value["image 1"],  color='g', linewidth=0, antialiased=True, alpha = 0.4, rcount=200, ccount=200)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))

    ax.plot_surface(X, Y, filtered_Z_value["image 2"], color='r', antialiased=True, alpha = 0.4, rcount=200, ccount=200)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))
    ax.dist=5


def var_checked_p_value(wt_pixels, mt_pixels, alt_answer):
    _, unchecked_p_value = stats.levene(wt_pixels, mt_pixels)
    if unchecked_p_value < 0.05:
        variance = False
    else:
        variance = True
    p_value = stats.ttest_ind(wt_pixels, mt_pixels, equal_var = variance, alternative=alt_answer).pvalue
    return p_value
 
def image_dimensions(list_of_files):
    """ Recieves an image array and returns how many rows and columns it contains."""
    first_image = list_of_files[0]
    image_height = len(first_image)
    image_width = len(first_image[0])
    return image_width, image_height


