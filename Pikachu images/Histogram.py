import os
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def process_image_data(folder_path):
    """Collects image sizes from a folder and calculates area in megapixels"""
    image_sizes = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            filepath = os.path.join(folder_path, filename)
            with Image.open(filepath) as img:
                width, height = img.size
                image_sizes.append((width, height))
                filenames.append(filename)

    sizes_in_megapixels = [(w * h) / 1000000 for w, h in image_sizes]
    return sizes_in_megapixels, filenames

def find_outliers(sizes, threshold=2):
    mean_size = np.mean(sizes)
    std_dev = np.std(sizes)

    outlier_indices = []
    for i, size in enumerate(sizes):
        z_score = (size - mean_size) / std_dev
        if abs(z_score) > threshold:
            outlier_indices.append(i)

    return outlier_indices

data = {}
data_folder = "./HistogramData"
folder_label = data_folder.split('/')[-1:]
folder_label = '/'.join(folder_label) 
sizes, filenames = process_image_data(data_folder)
data[folder_label] = sizes

for label, sizes in data.items():
    plt.hist(sizes, bins=10, range=(0, max(sizes) * 1.1))  
    plt.xlabel("Image Size (megapixels)")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Image Sizes - {label}")
    plt.show()

outlier_indices = find_outliers(sizes)
filtered_sizes = [size for i, size in enumerate(sizes) if i not in outlier_indices]
filtered_folder = "./FilteredImages"

for label, sizes in data.items():
    plt.hist(filtered_sizes, bins=10, range=(0, max(sizes) * 1.1))  
    plt.xlabel("Image Size (megapixels)")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Image Sizes after big images removed - {label}")
    plt.show()

if os.path.exists(filtered_folder): 
    shutil.rmtree(filtered_folder)

os.makedirs(filtered_folder, exist_ok=True) 

for i, size in enumerate(sizes):
    if i not in outlier_indices: 
        filepath = os.path.join(data_folder, filenames[i])
        save_path = os.path.join(filtered_folder, filenames[i])

        with Image.open(filepath) as img:
            img.save(save_path)

