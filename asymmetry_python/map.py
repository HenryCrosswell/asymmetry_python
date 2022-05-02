
from utils import read_image, get_pixel_values_from_image_array, read_and_sort_files
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


#windows
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"

wt_files = []
mt_files = []
    
read_and_sort_files(folder_path, wt_files, mt_files)

firstImage = wt_files[0]
imageHeight = len(firstImage)
imageWidth = len(firstImage[0])

result = [[0 for x in range(imageWidth)] for y in range(imageHeight)]

for currentYAxis in range(imageHeight):
    for currentXAxis in range(imageWidth):

        wt_image_pixels = get_pixel_values_from_image_array(currentXAxis, currentYAxis, wt_files)
        mt_image_pixels = get_pixel_values_from_image_array(currentXAxis, currentYAxis, mt_files)
        p_value = stats.ttest_ind(wt_image_pixels, mt_image_pixels).pvalue
        
        if np.isnan(p_value):
            p_value = 0

        result[currentYAxis][currentXAxis] = p_value
    
np.savetxt("map.csv", result, delimiter=",")
plt.imshow(result)
plt.show()
