from turtle import color
from utils import read_image, apply_mask, image_mask, mean_and_stdev
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\pixel_distance_python\\"

fig, axs = plt.subplots(len(listdir(folder_path)))
fig.suptitle('Histograms')
plt.ylabel("quantity")
plt.ylabel("Pixel distance")

for file_number, file_path in enumerate(listdir(folder_path)):
    input_image = read_image(folder_path+file_path)
    mask = image_mask(input_image)
    values_of_interest = apply_mask(input_image, mask)

    axs[file_number].hist(values_of_interest)
    # plt.scatter(np.ones_like(values_of_interest), values_of_interest)
    #plt.boxplot(values_of_interest)
    axs[file_number].set_title(file_path)
    mean, st_dev = mean_and_stdev(values_of_interest)
    print(mean)
    print(st_dev)
    if file_path[:2] == "WT":
        plt.hist(values_of_interest, color= 'green')
        print('hi')
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=3)

plt.show()