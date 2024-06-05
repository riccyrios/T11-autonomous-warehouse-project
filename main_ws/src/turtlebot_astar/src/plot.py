import matplotlib.pyplot as plt
 
# Define the points
points = [
[((0, 0), (0.528, 0.0), (0.924, 0.0), (0.522, -0.068), (0.648, 0.445), (0.774, 0.958), (0.669, 1.329), (0.949, 1.777), (0.864, 2.079))]
]
 
# Plot each set of points
for point_set in points:
    x = [point[0] for point in point_set]
    y = [point[1] for point in point_set]
    plt.plot(x, y)
 
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Graph of Points')
plt.grid(True)
plt.show()