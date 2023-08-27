"""
Main script in which you pick a folder containing pre-labelled, same size images. 
"""

from asymmetry_python.plotting import create_plots
from asymmetry_python.loading import read_and_sort_files
from asymmetry_python.processing import scan_image_and_process, total_significant_values
import time 
from tqdm import tqdm
from multiprocessing import freeze_support
import logging
from tkinter import filedialog
import os
import warnings
warnings.filterwarnings('error')

if __name__ == '__main__':
    # Logging and time taken initalising
    freeze_support()
    logging.basicConfig(filename='asymmetry_python/log_file.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    start_time = time.time()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # These values were chosen to give completly different views of the data - (azimuth, elevation), as well as a clear edge colour.
    azimuth_elevation_mapping = {
        1: (60, 15),
        2: (90, 89),
        3: (0, 0)
    }
    edge_colour = '#3CAEA3'

    # Interactive selection of a folder containing images to analyse and a folder to save the images.
    try:
        print('Select the folder containing your pre-processed images... ')
        # folder_path = filedialog.askdirectory(title="Select folder containing images")
        folder_path = os.path.join(script_dir, 'asymmetry_python/tests/data')
        print(f"Selected folder: {folder_path}")

        print('Select the folder where you would like to output the plots... ')
        # file_save_path = filedialog.askdirectory(title="Select folder for results")
        file_save_path = os.path.join(script_dir, 'asymmetry_python/tests/test_save')
        print(f"Selected folder to save results in : {file_save_path}")

    except FileNotFoundError as e:
        print(f'The path provided is not valid : {e}')

    except Exception as e:
        logging.error(f'An error has occured : {e}')

    wt_files_list, mt_files_list = read_and_sort_files(folder_path)
    median_diff_array, p_value_mask_array, mt_median_image, wt_median_image = scan_image_and_process(wt_files_list, mt_files_list)
    wt_sig_percentage, mt_sig_percentage = total_significant_values(p_value_mask_array, median_diff_array)

    # The total amount of graphs with 3 azimuth nad elevation maps is 6, since create plots creates two different plots.
    with tqdm(total=6) as pbar:
        for number, (azimuth, elevation) in azimuth_elevation_mapping.items():
            logging.info(f'Creating plots, viewed at azimuth : {azimuth} and elevation : {elevation}...')
            pbar.update(2)
            # 300 dpi was chosen as it is a standard for printed images, 5 is a good line thickness for this size image.
            create_plots(
                median_diff_array, 
                p_value_mask_array, 
                mt_median_image, 
                wt_median_image, 
                file_save_path, 
                elevation, 
                azimuth, 
                dpi = 300, 
                edge_colour = edge_colour, 
                edge_line_width = 5
                )

    logging.info(
    f'WT significance - {wt_sig_percentage:.2f}%\n'
    f'MT significance - {mt_sig_percentage:.2f}%\n'
    f'Figures successfully saved in - {file_save_path}\n'
    f'---- {time.time()-start_time:.2f} seconds ----'
    )