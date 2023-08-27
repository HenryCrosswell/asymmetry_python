from cmath import nan
import numpy as np
from ..plotting import custom_gaussian_filter, create_plots, plot3Dmedians, plot3Dp_values
from pathlib import Path

def test_gaussian_filter():
    image_array = np.array([[nan,nan,nan,nan,nan,nan],
                            [nan,nan,nan,2,1,3],
                            [nan,nan,nan,nan,1,4],
                            [nan,nan,nan,1,nan,3],
                            [nan,nan,nan,4,2,nan]])
    altered_image = custom_gaussian_filter(image_array, 1, 1)
    assert image_array.shape == altered_image.shape
    assert np.isnan(image_array).any() == True


def test_create_plots():
    # Create some dummy data for the test
    median_diff_array = np.random.rand(10, 10)
    p_value_mask_array = np.random.choice(['#3CAEA3', '#ED553B'], (10, 10))
    mt_median_image = np.random.rand(10, 10)
    wt_median_image = np.random.rand(10, 10) 
    file_save_path = Path(__file__).parent / 'test_save'
    print(file_save_path)
    elevation = 30
    azimuth = 45
    dpi = 300
    
    # Call the create_plots function
    create_plots(median_diff_array, p_value_mask_array, mt_median_image, wt_median_image, file_save_path, elevation, azimuth, dpi, '#3CAEA3', edge_line_width= 5)

def test_plot3Dp_values():
    median_diff_array = np.random.rand(10, 10)
    p_value_mask_array = np.random.choice(['#3CAEA3', 'None'], (10, 10))
    elevation = 30
    azimuth = 45
    
    plot3Dp_values(median_diff_array, p_value_mask_array, elevation, azimuth, '#3CAEA3', edge_line_width= 5)
    # No assertions here as this function involves visual inspection.

    
def test_plot3Dmedians():
    wt_median_image = np.random.rand(10, 10)
    mt_median_image = np.random.rand(10, 10)
    elevation = 30
    azimuth = 45
    
    plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth)
    # No assertions here as this function involves visual inspection.