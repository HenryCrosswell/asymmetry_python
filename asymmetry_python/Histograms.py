from utils import read_image, image_mask, mean_and_stdev
from os import listdir
import matplotlib.pyplot as plt
import numpy as np

#windows
folder_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\adjusted_pixel_distance_python\\"

#mac
#folder_path = "/Users/henrycrosswell/Library/CloudStorage/OneDrive-UniversityCollegeLondon/Project Work/Image Analysis/Images/Cell shaver/pixel_distance_python/"



fig, axs = plt.subplots(12,2, sharex=True, sharey=True, figsize= (10,9))
fig.suptitle('Histograms')
fig.supxlabel('Pixel distance')
fig.supylabel('Quantity')

plt.rcParams['figure.constrained_layout.use'] = True
y_lim = [0,400000]
x_lim = [10,350]
equally_spaced_bins = range(x_lim[0], x_lim[1]+25, 25)
mt_medians = []
wt_medians = []


for file_number, file_path in enumerate(listdir(folder_path)):
    input_image = read_image(folder_path+file_path)
    mask = image_mask(input_image)
    all_nonzero_values = input_image[mask]
    values_of_interest = all_nonzero_values[all_nonzero_values>10]
    row_number = file_number%12
    if file_path[:2] == "WT":
        axs[row_number, 1].hist(values_of_interest, color= 'green', bins=equally_spaced_bins)
        axs[row_number, 1].set_ylim(y_lim)
        axs[row_number, 1].set_xlim(x_lim)
        axs[row_number, 1].set_title(file_path)
        axs[row_number, 1].set_xticks([10,50,100,150,200,250,300,350])
        wt_medians.append(np.median(values_of_interest))
        continue
    axs[row_number, 0].set_title(file_path)
    axs[row_number, 0].hist(values_of_interest, bins=equally_spaced_bins)
    axs[row_number, 0].set_ylim(y_lim)
    axs[row_number, 0].set_xlim(x_lim)
    axs[row_number, 0].set_xticks([10,50,100,150,200,250,300,350])
    mt_medians.append(np.median(values_of_interest))

    


plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.6)
plt.show()


fig2, axs2 = plt.subplots()

bp = axs2.boxplot([wt_medians, mt_medians], patch_artist= True)

colour_list = ["red", "purple"]
whisker_colours = ["green", "green", "blue", "blue"]
for patch, color in zip(bp['boxes'], colour_list):
    patch.set_facecolor(color)

for patch, color in zip(bp['whiskers'], whisker_colours):
    plt.setp(patch, color = color)
     

plt.ylabel("Median")
axs2.set_xticklabels(["WT medians", "MT medians"]),

plt.show()
