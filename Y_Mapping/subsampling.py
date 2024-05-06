import cv2
import numpy as np
import yaml
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Read the PGM file
map_image = cv2.imread('cart3_map.pgm', cv2.IMREAD_GRAYSCALE)

# Read the YAML file
with open('cart3_map.yaml', 'r') as yaml_file:
    map_metadata = yaml.safe_load(yaml_file)

# Extract map metadata
resolution = map_metadata['resolution']
origin = map_metadata['origin']
origin_x = origin[0]
origin_y = origin[1]
width = map_image.shape[1]
height = map_image.shape[0]


# Perform clustering-based subsampling
def cluster_subsampling(map_image, resolution, origin_x, origin_y, num_clusters):
    occupied_pixels = np.argwhere(map_image == 0)  # Find coordinates of occupied pixels

    # Convert pixel coordinates to real-world XY coordinates
    occupied_coordinates = []
    for pixel in occupied_pixels:
        map_x = round(pixel[1] * resolution + origin_x, 2)
        map_y = round((height - pixel[0]) * resolution + origin_y, 2)  # Flip y-axis
        occupied_coordinates.append([map_x, map_y])

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(occupied_coordinates)
    cluster_centers = kmeans.cluster_centers_

    return cluster_centers.tolist()

# Define the number of clusters for subsampling
num_clusters = 100  # Adjust as needed

# Perform clustering-based subsampling
subsampled_coordinates = cluster_subsampling(map_image, resolution, origin_x, origin_y, num_clusters)

# Write subsampled coordinates to a new file
output_file_subsampled = "subsampled_coordinates_cart.txt"
with open(output_file_subsampled, "w") as f:
    for coord in subsampled_coordinates:
        x_rounded = round(coord[0], 2)
        y_rounded = round(coord[1], 2)
        f.write(f"X: {x_rounded}, Y: {y_rounded}\n")

print(f"Subsampled coordinates have been saved to '{output_file_subsampled}'")

# Optionally, visualize the subsampled points
plt.figure(figsize=(10, 10))
plt.scatter([coord[0] for coord in subsampled_coordinates], [coord[1] for coord in subsampled_coordinates], color='purple', s=5)
plt.title('Subsampled Occupied Areas')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.gca().invert_yaxis()

# Save the plot as an image file
plot_file = "subsampled_plot.png"
plt.savefig(plot_file)

# Show the plot
plt.show()

print(f"Plot saved as '{plot_file}'")
