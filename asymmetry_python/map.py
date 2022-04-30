from utils import read_image, apply_mask, image_mask, mean_and_stdev
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from scipy import stats

wt_values_list = []
mt_values_list = []
ttest_list = []
y_axis_counter = 0
x_axis_count = 0
whole_process_counter = 0

#windows
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"
#mac
#folder_path = "/Users/henrycrosswell/Library/CloudStorage/OneDrive-UniversityCollegeLondon/Project Work/Image Analysis/Images/Cell shaver/test/"



# scans through the assigned folder, makes a count of how many images are in that folder and commits that to memory
# takes a single image and creates an array y=0, x= the x value (how many columns are in the image)
for number_of_images_in_folder, reference_file_path in enumerate(listdir(folder_path)):
    image_reference = read_image(folder_path+reference_file_path)
    number_of_images_in_folder +=1
    for row_list in image_reference:
        new_ttest_image = np.empty((0, len(image_reference[0])))
        break


# this while loop keeps a counter of how many processes have taken place and stops when the amount of pixels in every image has been scanned

while whole_process_counter!= (image_reference.size * number_of_images_in_folder):

    # this for loop counts and opens a single image in the folder path, repeating until each pixel in one row of each image has been indexed

    for file_number, file_path in enumerate(listdir(folder_path)): 

        input_image = read_image(folder_path+file_path) #commmits current image in for loop to variable

        current_row = input_image[y_axis_counter] #commits a list of values in the current row to a variable depending on its y value

        image_index_value = [index[x_axis_count] for index in current_row] #returns every [count] index of the image







        whole_process_counter += 1 # updates the while loop counter

        value_of_interest = current_row[x_axis_count] #x axis count indexes the current row sequentially

        if file_path[:2] == "WT":
            wt_values_list.append(value_of_interest) #if image is a WT the value of interest is added to a list 

        else: 
            mt_values_list.append(value_of_interest) #if image is a MT the value of interest is added to a list 

        if file_number == number_of_images_in_folder-1: #if the folder count of the for loop has reached the maximum amount of folders in the file (-1 for indexing reasons)

            p_value = stats.ttest_ind(wt_values_list, mt_values_list).pvalue #extracts a single p value for every MT pixel values at count and every WT value at count

            if np.isnan(p_value) == True: #if the value is nan (p values of zero values only) it is assigned 0 instead of nan
                p_value = 0

            ttest_list.append(p_value) # assigns a single p value of every pixel from every image to a list as index count.

            wt_values_list = [] #resets the list
            mt_values_list = []

            x_axis_count += 1 # moves the index along the a axis after all inxeded variables have been commited to the p value list

        if x_axis_count == len(current_row): #if the indexing reathes the full length of x axis
            y_axis_counter += 1 #the row being indexed moves one row down

            new_ttest_image = np.vstack([new_ttest_image, ttest_list]) #creates a new array with p values

            ttest_list = [] #resets the pvalue list

            x_axis_count = 0 #resets the row indexing to start at the begginning of the new row





plt.imshow(new_ttest_image)
plt.show()