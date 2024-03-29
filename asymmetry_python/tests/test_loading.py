import numpy as np
from ..loading import image_dimensions, read_and_sort_files, get_pixel_values_from_image_array
import pytest
from pathlib import Path

def test_image_dimensions():
    test_image_list = [np.ones(shape=(3, 4)), np.ones(shape=(3, 4))]
    width, height = image_dimensions(test_image_list)
    assert width == 4
    assert height == 3

def test_read_and_sort_files():
    test_folder_path = Path(__file__).parent / "data"
    wt_list, mt_list = read_and_sort_files(test_folder_path)
    wt_list, mt_list = read_and_sort_files(test_folder_path)
    assert len(mt_list) == 3
    assert len(wt_list) == 3

    # wt images are edited for the first two pixels to be 252
    for im_array in wt_list: 
        image_pixel_row = im_array[26][:]
        x = np.count_nonzero(image_pixel_row == 252)
        assert x == 2

    # mt images are edited for the first four pixels to be 252
    for im_array in mt_list:
        image_pixel_row = im_array[26][:]
        x = np.count_nonzero(image_pixel_row == 252)
        assert x == 4

def test_get_pixel_values_from_image_array():
    # Create sample image arrays for testing
    image1 = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])

    image2 = np.array([[11, 12, 13],
                       [14, 15, 16],
                       [17, 18, 19]])
    
    x = 0
    y = 0
    result = get_pixel_values_from_image_array(x, y, [image1, image2])
    assert result == [1, 11]

    x = 1
    y = 1
    result = get_pixel_values_from_image_array(x, y, [image1, image2])
    assert result == [5, 15]

    x = 2
    y = 2
    result = get_pixel_values_from_image_array(x, y, [image1, image2])
    assert result == [9,19]

    x = 4
    y = 50
    with pytest.raises(IndexError) as e:
        result = get_pixel_values_from_image_array(x, y, [image1, image2])
        assert str(e.value) == "index 50 is out of bounds for axis 0 with size 3"