from scipy import stats
from skimage.io import imread
from pathlib import Path
from os import listdir
import numpy as np

def read_and_sort_files_with_names(folder_path):
    mt_list = []
    wt_list = []
    mt_names = []
    wt_names = []
    for file_path in listdir(folder_path): 
        input_image = imread(Path(folder_path + file_path)) 
        if file_path[:2] == "WT":
            wt_names.append(file_path)
            wt_list.append(input_image) 
        elif file_path[:3] == "CF+":
            continue
        else: 
            mt_list.append(input_image) 
            mt_names.append(file_path)
    return mt_list, wt_list, mt_names, wt_names

def get_all_non_zero_values(image):
    flat_im = image.flatten()
    sorted_image_list = [i for i in flat_im if i != 0]
    return sorted_image_list

wt_dict = {}
mt_dict = {}
wt_median_list = []
mt_median_list = []

folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"

mt_list, wt_list, mt_names, wt_names = read_and_sort_files_with_names(folder_path)

for image in wt_list:
    wt_image_non_zero_list = get_all_non_zero_values(image)
    wt_median = np.mean(wt_image_non_zero_list)
    wt_median_list.append(wt_median)

for image in mt_list:
    mt_image_non_zero_list = get_all_non_zero_values(image)
    mt_median = np.mean(mt_image_non_zero_list)
    mt_median_list.append(mt_median)

for key in wt_names:
    for value in wt_median_list:
        wt_dict[key] = value
        wt_median_list.remove(value)
        break  
for key in mt_names:
    for value in mt_median_list:
        mt_dict[key] = value
        mt_median_list.remove(value)
        break  

print(str(wt_dict))
print(str(mt_dict))