
import math

# Circle parameters
center_x = 0.336
center_y = 0.589
radius = 0.16  # Radius in meters
num_points = 8

# List to store the coordinates of the points
circle_points = []

# Calculate the coordinates of each point
for i in range(num_points):
    angle_deg = 45 * i  # Each point is 45 degrees apart
    angle_rad = math.radians(angle_deg)
    x = center_x + radius * math.cos(angle_rad)
    y = center_y + radius * math.sin(angle_rad)
    # Round to 2 decimal places
    x_rounded = round(x, 2)
    y_rounded = round(y, 2)
    circle_points.append((x_rounded, y_rounded))

# Print the list of points
print(f"Cardinal direction points centred at ({center_x}, {center_y}) with radius {radius}:")
for i, point in enumerate(circle_points):
    print(f"{point},")

# Output as a list of tuples
circle_points

