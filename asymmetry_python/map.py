
from utils import read_image, get_pixel_values_from_image_array, read_and_sort_files
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


#windows
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"

#creates lists that will be filled with an array of images, depending on whether they are wt or mt
wt_files = []
mt_files = []
    
#reads folder_path, assigns image arrays to either wt or mt
read_and_sort_files(folder_path, wt_files, mt_files)

#returns reference height and width
firstImage = wt_files[0]
imageHeight = len(firstImage)
imageWidth = len(firstImage[0])

#creates a 2D array that is the width and height of the reference image
result = [[0 for x in range(imageWidth)] for y in range(imageHeight)]

#outside loop is for y axis, inside is for x. Therefore, every time it loops through an x axis the y axis ticks down once
for currentYAxis in range(imageHeight):
    for currentXAxis in range(imageWidth):

        #returns a list of values at the current x and y coordinate for either the wt or mt images. 
        wt_image_pixels = get_pixel_values_from_image_array(currentXAxis, currentYAxis, wt_files)
        mt_image_pixels = get_pixel_values_from_image_array(currentXAxis, currentYAxis, mt_files)
        p_value = stats.ttest_ind(wt_image_pixels, mt_image_pixels).pvalue
        
        if np.isnan(p_value):
            p_value = 0

        #writes the p_value into the corresponding coordinate for the empty array, creating a new image
        result[currentYAxis][currentXAxis] = p_value
    
np.savetxt("map.csv", result, delimiter=",")
plt.imshow(result)
plt.show()
