"""
Functions to aid in the plotting of created 2D arrays
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import scipy as sp
import matplotlib as mpl
from asymmetry_python.processing import find_and_add_edge_colour

def gaussian_filter(image_array, sigma, truncate):
    """Filters a given array excluding nan values more effectively than the normal gaussian function.

    Keyword arguments:
    image_array -- the chosen image array that will undergo filtering
    sigma -- the range at which the filter averages the values
    truncate -- the decimal places in which the average is cut off at    
    """

    U = np.array(image_array)
    V=U.copy()
    V[np.isnan(U)]=0
    VV=sp.ndimage.gaussian_filter(V,sigma=sigma,truncate=truncate)
    W=0*U.copy()+1
    W[np.isnan(U)]=0
    WW=sp.ndimage.gaussian_filter(W,sigma=sigma,truncate=truncate)
    Z = VV/WW
    return Z

def plot3Dp_values(median_diff_array, P_value_mask, elevation, azimuth):
    """Surface plots the difference in median values onto an X,Y,Z axis, smooths the image and extends the Y axis to a representitive size. 
    Following this, applys either a Red mask if the P_value for the mutant is significant, or a Blue mask if the wild-type is significant.
    
    Keyword arguments:
    median_diff_array -- a 2D array, containing the difference in median values between indivual pixels for the mutant images and wild-type.
    p_value_mask -- a 2D array, containing colour-coordinated strings in which significant mutant and WT P_values are coloured differently to non-sig values.
    elevation -- an int determining the height at which the graph is viewed
    azimuth -- an int specifiying the rotation of the final graph
    """
    image_height = len(median_diff_array)
    image_width = len(median_diff_array[0])

    Z = gaussian_filter(median_diff_array, 4, 4)
    p_value_and_edge_mask = find_and_add_edge_colour(median_diff_array, P_value_mask, 5, '#3CAEA3')
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8,6))
    ax.set(xlim=(0, image_width), ylim=(0, image_height))
    X, Y = np.meshgrid(range(image_width), range(image_height))
    ax.set_aspect('auto')
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, facecolors=p_value_and_edge_mask) #alpha = 0.6)
    ax.view_init(elevation,azimuth)
    ax.dist = 7
    
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zlim(-40,40)
    median_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#3CAEA3', marker = 'o')
    wt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#F6D55C', marker = 'o')
    mt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#ED553B', marker = 'o')
    ax.legend([median_proxy, wt_proxy, mt_proxy], ['Median Difference', 'WT significance', 'MT signficance'], numpoints = 1, loc='upper left')

def plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth):
    """Surface plots both results onto an X,Y,Z axis, smooths the image and extends the Y axis to a representitive size.
    
    Keyword arguments:
    mt_median_image -- a 2D array, with median values of indivual pixels for the mutant images 
    wt_median_image -- a 2D array, with median values of indivual pixels for the wild-type images
    elevation -- an int determining the height at which the graph is viewed
    azimuth -- an int specifiying the rotation of the final graph
    """
    image_height = len(wt_median_image)
    image_width = len(wt_median_image[0])
    plt.rcParams.update({'font.family':'Calibri'})
    Z = gaussian_filter(wt_median_image, 4, 4)
    Z1 = gaussian_filter(mt_median_image, 4, 4)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8,6))
    ax.set(xlim=(0, image_width), ylim=(0, image_height))
    X, Y = np.meshgrid(range(image_width), range(image_height))
       
    ax.set_aspect('auto')

    ax.plot_surface(X, Y, Z, color='#EDC194', antialiased=True, alpha = 0.8, rcount=200, ccount=200)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))
    ax.dist=7

    ax.plot_surface(X, Y, Z1,  color='#6A76B7', linewidth=0, antialiased=True, alpha = 0.8, rcount=200, ccount=200)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.4, 1.0, 0.4, 1]))
    ax.view_init(elevation,azimuth)

    ax.set_zlim(0,70)
    wt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#6A76B7', marker = 'o')
    mt_proxy = mpl.lines.Line2D([0],[0], linestyle="none", c='#EDC194', marker = 'o')
    ax.legend([wt_proxy, mt_proxy], ['WT median distance', 'Cre;Fl/Fl median distance'], numpoints = 1, loc='upper left')

