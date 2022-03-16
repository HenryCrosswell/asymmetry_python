from utils import read_image, apply_mask, image_mask, mean_and_stdev
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\pixel_distance_python\\"

fig, axs = plt.subplots(len(listdir(folder_path)))
fig.suptitle('Histograms')

for file_number, file_path in enumerate(listdir(folder_path)):
    input_image = read_image(folder_path+file_path)
    mask = image_mask(input_image)
    values_of_interest = apply_mask(input_image, mask)

    axs[file_number].hist(values_of_interest)
    # plt.scatter(np.ones_like(values_of_interest), values_of_interest)
    #plt.boxplot(values_of_interest)

    mean, st_dev = mean_and_stdev(values_of_interest)
    print(mean)
    print(st_dev)

plt.show()