"""
Main script in which you pick a folder containing pre-labelled, same size images. 
"""

from plotting import plot3Dp_values, plot3Dmedians
from tkinter import filedialog
from loading import read_and_sort_files
from processing import scan_image_and_process, total_significant_values
from loading import read_and_sort_files
from processing import scan_image_and_process, total_significant_values
import matplotlib.pyplot as plt
import os
from time import sleep
import time 
from tqdm import tqdm
from pathlib import Path

start_time = time.time()

print('Select the folder containing your pre-prepared images... ')
#folder_path = filedialog.askdirectory()
print('Select the folder where you would like to output the plots... ')
#file_save_path = filedialog.askdirectory()

folder_path = Path('C:\\Users\\henry\\OneDrive - University College London\\Coding\\tissue_asymmetry_python\\tests\\data\\')
file_save_path= Path('C:\\Users\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Python Test images\\')



wt_files, mt_files = read_and_sort_files(folder_path)
median_diff_array, p_value_mask_array, mt_median_image, wt_median_image = scan_image_and_process(wt_files, mt_files)
wt_sig_percentage, mt_sig_percentage = total_significant_values(p_value_mask_array, median_diff_array)
number = 1

# numbers below are hardcorded angles that present the plots nicely.
print(' Creating plots..')
pbar = tqdm(total = 6)
        
while number != 4:
    
    if number == 1:
        variable_file_name = 'none_my_plot_a60_e15.png'
        med_variable_file_name = 'median_diff_plot_a60_e15.png'
        azimuth = 60
        elevation = 15
    if number == 2:
        variable_file_name = 'none_my_plot_a90_e89.png'
        med_variable_file_name = '_median_diff_plot_a90_e89.png'
        azimuth = 90
        elevation = 89  # cannot put 90 because colours are displayed incorrectly.
    if number == 3:
        variable_file_name = 'nonee_my_plot_a0_e0.png'
        med_variable_file_name = 'median_diff_plot_a0_e0.png'
        azimuth = 0
        elevation = 0    

    sleep(0.02) 
    pbar.update(1)
    plot3Dp_values(median_diff_array, p_value_mask_array, elevation, azimuth)
    plt.savefig(os.path.join(file_save_path, variable_file_name), dpi = 300)

    sleep(0.02) 
    pbar.update(1)  
    plot3Dmedians(wt_median_image, mt_median_image, elevation, azimuth)
    plt.savefig(os.path.join(file_save_path, med_variable_file_name), dpi = 300)

    number += 1
    
print(' WT significance -', wt_sig_percentage, '%, MT significance -', mt_sig_percentage, '%')
print('Figures saved in - ', file_save_path)

print(f'---- {time.time()-start_time} seconds ----')