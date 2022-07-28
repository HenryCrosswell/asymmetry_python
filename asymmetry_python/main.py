"""
Main script in which you pick a folder containing pre-labelled, same size images. 
"""

from plotting import plot3Dp_values, plot3Dmedians
from tkinter import filedialog
from loading import read_and_sort_files
from processing import scan_image_and_process, downscale
import matplotlib.pyplot as plt
import numpy as np
import os

file_save_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image_Analysis\\Images\\Images_from_python_script\\"
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image_Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"
#folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\test\\"
#folder_path = filedialog.askdirectory()
#file_save_path = filedialog.askdirectory()

wt_files, mt_files = read_and_sort_files(folder_path)
median_diff_array, p_value_mask_array, mt_median_image, wt_median_image = scan_image_and_process(wt_files, mt_files)

number = 1

# numbers below are hardcorded angles that I want the plot to be saved at
while number != 4:
    if number == 1:
        variable_file_name = 'nonemy_plot_a60_e15.png'
        med_variable_file_name = 'nonemedian_diff_plot_a60_e15.png'
        azimuth = 60
        elevation = 15
    if number == 2:
        variable_file_name = 'nonemy_plot_a90_e90.png'
        med_variable_file_name = 'nonemedian_diff_plot_a90_e90.png'
        azimuth = 90
        elevation = 90
    if number == 3:
        variable_file_name = 'noneemy_plot_a0_e0.png'
        med_variable_file_name = 'nonemedian_diff_plot_a0_e0.png'
        azimuth = 0
        elevation = 0
    number += 1

    plot3Dp_values(median_diff_array, p_value_mask_array, elevation, azimuth)
    plt.savefig(os.path.join(file_save_path, variable_file_name), dpi = 300)

    plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth)
    plt.savefig(os.path.join(file_save_path, med_variable_file_name), dpi = 300)

    print(number,'- complete')
print('done')
