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

# Define the specified coordinates
specified_coordinates = [
    (-2.913, 4.222), (-2.532, 4.162), (-0.890, 4.022), (-0.460, 3.972),
    (1.081, 3.892), (1.461, 3.852), (1.431, 3.342), (1.051, 3.392),
    (-0.440, 3.532), (-0.910, 3.572), (-2.532, 3.722), (-2.913, 3.762),
    (-3.093, 2.181), (-2.662, 2.161), (-1.061, 1.981), (-0.660, 1.951),
    (0.890, 1.821), (1.251, 1.841), (1.231, 1.290), (0.840, 1.340)
]

# Optionally, visualize the subsampled points and specified coordinates
plt.figure(figsize=(10, 10))
plt.scatter([coord[0] for coord in subsampled_coordinates], [coord[1] for coord in subsampled_coordinates], color='purple', s=5)
plt.scatter([coord[0] for coord in specified_coordinates], [coord[1] for coord in specified_coordinates], color='blue', s=50, marker='x')
plt.title('Subsampled Occupied Areas with Specified Coordinates')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.gca().invert_yaxis()
plt.gca().invert_xaxis()

# Add specified coordinates to the image
for coord in specified_coordinates:
    x, y = coord
    plt.text(x, y, f'({x}, {y})', color='blue', fontsize=8)

# Save the plot as an image file
plot_file = "subsampled_plot.png"
plt.savefig(plot_file)

# Show the plot
plt.show()

print(f"Plot saved as '{plot_file}'")
