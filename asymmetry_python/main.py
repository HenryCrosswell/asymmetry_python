from utils import read_image, apply_mask, image_mask, mean_and_stdev
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\pixel_distance_python\\"

fig, axs = plt.subplots(len(listdir(folder_path)), figsize= (10,20))
fig.suptitle('Histograms')
plt.ylabel("Quantity")
plt.xlabel("Pixel distance")
plt.rcParams['figure.constrained_layout.use'] = True
for file_number, file_path in enumerate(listdir(folder_path)):
    input_image = read_image(folder_path+file_path)
    mask = image_mask(input_image)
    values_of_interest = input_image[mask]
    axs[file_number].set_title(file_path)
    if file_path[:2] == "WT":
        axs[file_number].hist(values_of_interest, color= 'green')
        continue
    axs[file_number].hist(values_of_interest)

plt.show()
