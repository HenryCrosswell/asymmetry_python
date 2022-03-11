from utils import read_image, apply_mask, image_mask, mean_and_stdev

file_path = "C:\\Users\\henry\\OneDrive - University College London\\Project Work\\Image Analysis\\Images\\Cell shaver\\Pixel distance\\MAX_Result NVAH5 vert.tif"

input_image = read_image(file_path)
mask = image_mask(input_image)
values_of_interest = apply_mask(input_image, mask)
mean_and_stdev(values_of_interest)