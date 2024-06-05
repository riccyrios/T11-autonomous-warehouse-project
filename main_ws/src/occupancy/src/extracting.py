import cv2
import numpy as np
import yaml
import matplotlib.pyplot as plt

# Read the PGM file
map_image = cv2.imread('/home/ubuntu/git/T11_multi_warehouse/main_ws/src/occupancy/src/cart3_map.pgm', cv2.IMREAD_GRAYSCALE)

# Read the YAML file
with open('/home/ubuntu/git/T11_multi_warehouse/main_ws/src/occupancy/src/cart3_map.yaml', 'r') as yaml_file:
    map_metadata = yaml.safe_load(yaml_file)

# Extract map metadata
resolution = map_metadata['resolution']
origin = map_metadata['origin']
origin_x = origin[0]
origin_y = origin[1]
width = map_image.shape[1]
height = map_image.shape[0]

# Convert occupancy grid to binary image
_, binary_map = cv2.threshold(map_image, int(map_metadata['occupied_thresh'] * 255), 255, cv2.THRESH_BINARY)

# Initialize set to store rounded XY coordinates
occupied_coordinates_set = set()

# Extract coordinates of occupied areas
for y in range(height):
    for x in range(width):
        if binary_map[y, x] == 0:
            # Convert grid coordinates to real-world XY coordinates
            map_x = round(x * resolution + origin_x, 2)
            map_y = round((height - y) * resolution + origin_y, 2)  # Flip y-axis
            occupied_coordinates_set.add((map_x, map_y))

# Convert set to list and sort
occupied_coordinates = sorted(list(occupied_coordinates_set))

# Write coordinates to a text file
output_file = "occupied_coordinates_cart.txt"
with open(output_file, 'w') as f:
    for coord in occupied_coordinates:
        f.write(f"X: {coord[0]}, Y: {coord[1]}\n")

print(f"Occupied coordinates have been saved to '{output_file}'")

# Plot the map and occupied coordinates
plt.figure(figsize=(10, 10))
# plt.imshow(map_image, cmap='gray')
plt.scatter([coord[0] for coord in occupied_coordinates], [coord[1] for coord in occupied_coordinates], color='red', s=5)
plt.title('Occupied Areas')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.gca().invert_yaxis()  # Invert y-axis to match image coordinates

# Save the plot as an image file
plot_file = "occupied_coord_plot.png"
plt.savefig(plot_file)

plt.show()
