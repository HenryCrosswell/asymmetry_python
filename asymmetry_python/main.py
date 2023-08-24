"""
Main script in which you pick a folder containing pre-labelled, same size images. 
"""
from plotting import create_plots
from loading import read_and_sort_files
from processing import scan_image_and_process, total_significant_values
import time 
from tqdm import tqdm
from pathlib import Path
from multiprocessing import freeze_support
import warnings

if __name__ == '__main__':
    freeze_support()

    start_time = time.time()

    print('Select the folder containing your pre-prepared images... ')
    folder_path = Path('C:\\Users\\henry\\OneDrive - University College London\\Coding\\tissue_asymmetry_python\\asymmetry_python\\tests\\data\\')
    print('Select the folder where you would like to output the plots... ')
    file_save_path = Path('C:\\Users\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Python Test images\\')

    wt_files_list, mt_files_list = read_and_sort_files(folder_path)
    
    with warnings.catch_warnings():
        median_diff_array, p_value_mask_array, mt_median_image, wt_median_image = scan_image_and_process(wt_files_list, mt_files_list)
        
        wt_sig_percentage, mt_sig_percentage = total_significant_values(p_value_mask_array, median_diff_array)
        warnings.simplefilter("ignore")

    azimuth_elevation_mapping = {
        1: (60, 15),
        2: (90, 89),
        3: (0, 0)
    }

    print('Creating plots...')
    with tqdm(total=6) as pbar:
        for number, (azimuth, elevation) in azimuth_elevation_mapping.items():
            pbar.update(1)
            create_plots(median_diff_array, p_value_mask_array, mt_median_image, wt_median_image, file_save_path, elevation, azimuth)

    print(f'WT significance - {wt_sig_percentage:.2f}%, MT significance - {mt_sig_percentage:.2f}%')
    print('Figures saved in - ', file_save_path)
    print(f'---- {time.time()-start_time:.2f} seconds ----')
