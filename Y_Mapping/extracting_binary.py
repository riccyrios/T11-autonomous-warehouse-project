import cv2
import numpy as np
import yaml
import matplotlib.pyplot as plt

# Read the PGM file
map_image = cv2.imread('/home/ubuntu/git/T11_multi_warehouse/Y_Mapping/cart3_map.pgm', cv2.IMREAD_GRAYSCALE)

# Read the YAML file
with open('/home/ubuntu/git/T11_multi_warehouse/Y_Mapping/cart3_map.yaml', 'r') as yaml_file:
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


output_file = "occupied_binary_cart.csv"


# Extract coordinates of occupied areas
with open(output_file, 'w') as f:
    for y in range(height):
        for x in range(width):
            if binary_map[y, x] == 0:
                f.write(f"1")
            else:
                f.write(f"0")
        f.write("\n")

print(f"Occupied coordinates have been saved to '{output_file}'")

