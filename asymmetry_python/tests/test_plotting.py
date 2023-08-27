from cmath import nan
import numpy as np
from ..plotting import gaussian_filter, create_plots, plot3Dmedians, plot3Dp_values
import os

def test_gaussian_filter():
    image_array = np.array([[nan,1,nan,3,4,5],[nan,1,nan,3,4,5],[nan,1,nan,3,4,5],[nan,1,nan,3,4,5]])
    altered_image = gaussian_filter(image_array, 2, 4)
 
    assert image_array.shape == altered_image.shape
    assert np.all(altered_image) != nan

def test_create_plots():
    # Create some dummy data for the test
    median_diff_array = np.random.rand(10, 10)
    p_value_mask_array = np.random.choice(['#3CAEA3', '#ED553B'], (10, 10))
    mt_median_image = np.random.rand(10, 10)
    wt_median_image = np.random.rand(10, 10)
    file_save_path = "test_save/"
    elevation = 30
    azimuth = 45
    dpi = 300
    
    # Call the create_plots function
    create_plots(median_diff_array, p_value_mask_array, mt_median_image, wt_median_image, file_save_path, elevation, azimuth, dpi)
    
    # Assert that the output file has been created
    assert os.path.exists(os.path.join(file_save_path, f'p_value_plot_a{azimuth}_e{elevation}.png'))
    assert os.path.exists(os.path.join(file_save_path, f'median_plot_a{azimuth}_e{elevation}.png'))

def test_plot3Dp_values():
    median_diff_array = np.random.rand(10, 10)
    p_value_mask_array = np.random.choice(['#3CAEA3', 'None'], (10, 10))
    elevation = 30
    azimuth = 45
    
    plot3Dp_values(median_diff_array, p_value_mask_array, elevation, azimuth)
    # No assertions here as this function involves visual inspection.

    
def test_plot3Dmedians():
    wt_median_image = np.random.rand(10, 10)
    mt_median_image = np.random.rand(10, 10)
    elevation = 30
    azimuth = 45
    
    plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth)
    # No assertions here as this function involves visual inspection.