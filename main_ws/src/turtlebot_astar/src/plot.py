import matplotlib.pyplot as plt
 
# Define the points
points = [
[(0, 0), (0.396, 0.0), (0.524, 0.363), (0.804, 0.81), (1.297, 0.605), (1.631, 0.858), (2.038, 1.194), (2.344, 1.446), (2.076, 1.747), (1.846, 2.222), (1.617, 2.698), (1.388, 3.173), (1.159, 3.649), (0.929, 4.125), (0.7, 4.6), (0.471, 5.076), (0.057, 5.007), (-0.459, 4.898), (-0.976, 4.788)]
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