from plotting import plot3Dp_values, plot3Dmedians
from tkinter import filedialog
from loading import read_and_sort_files
from processing import scan_image_and_process, downscale
import matplotlib.pyplot as plt
import numpy as np


folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"
#folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\test\\"
#folder_path = filedialog.askdirectory()

wt_files, mt_files = read_and_sort_files(folder_path)
median_diff_array, p_value_mask_array, mt_median_image, wt_median_image, high_median_mt, high_median_wt = scan_image_and_process(wt_files, mt_files)

number = 1
while number != 5:#2
    if number == 1:
        variable_file_name = 'testmy_plot_a113_e30.png'
        med_variable_file_name = 'testmedian_diff_plot_a113_e30.png'
        azimuth = 113
        elevation = 30
    if number == 2:
        variable_file_name = 'testmy_plot_a54_e40.png'
        med_variable_file_name = 'testmedian_diff_plot_a54_e40.png'
        azimuth = 54
        elevation = 40
    if number == 3:
        variable_file_name = 'testmy_plot_a60_e15.png'
        med_variable_file_name = 'testmedian_diff_plot_a60_e15.png'
        azimuth = 60
        elevation = 15
    if number == 4:
        variable_file_name = 'testmy_plot_a90_e90.png'
        med_variable_file_name = 'testmedian_diff_plot_a90_e90.png'
        azimuth = 90
        elevation = 90
    number += 1

    
    plot3Dp_values(median_diff_array, p_value_mask_array, elevation, azimuth)
    plt.savefig(variable_file_name, dpi = 300, bbox_inches='tight')

    plot3Dmedians(mt_median_image, wt_median_image, elevation, azimuth)
    plt.savefig(med_variable_file_name, dpi = 300, bbox_inches='tight')
    #plt.show()
    print(number,'- complete')
print('done')
