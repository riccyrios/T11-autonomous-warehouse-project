"""
Map Definition for A* Algorithm

Authors:
-Nidhi Bhojak
-Nalin Das (nalindas9@gmail.com)
Graduate Student pursuing Masters in Robotics,
University of Maryland, College Park
"""
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Plotting the final map

widthofmap = 9
heightofmap = 6
blc_x =  4
blc_y = -1
offset = 0.2

fig = plt.figure()
plt.axes()
plt.xlim(-5, 4.2)
plt.ylim(-1, 7)
plt.gca().invert_xaxis()  
plt.gca().invert_yaxis()  

walls = [
    (-0.13, 1.88),
    (-1.45, 4.12),
    (3.38, 2.82),
    (-3.89, 3.9),
    (1.16, -0.69),
    (1.71, 5.53),
    (-3.99, 2.33),
    (-2.12, 5.8),
    (2.9, 0.5),
    (-0.1, 5.66),
    (0.6, 3.57),
    (-2.12, 1.8),
    (-0.42, 0.08),
    (3.21, 5.33),
    (-3.8, 5.91),
    (-0.94, 1.48),
    (2.99, 1.54),
    (-4.58, 4.29),
    (-3.59, 2.27),
    (-1.12, 5.75),
    (0.16, -0.66),
    (3.66, 4.5),
    (2.29, 0.07),
    (-4.63, 3.22),
    (-4.59, 1.88),
    (0.59, 5.61),
    (0.08, 3.96),
    (-0.4, 0.41),
    (-3.03, 5.88),
    (1.6, 1.87),
    (-4.46, 4.77),
    (0.44, 1.53),
    (-3.08, 1.71),
    (-0.47, -0.61),
    (3.5, 3.57),
    (2.08, 5.45),
    (1.71, -0.39),
    (-0.78, 5.69),
    (1.76, 3.89),
    (-1.63, 2.07),
    (-4.3, 5.61),
    (-3.71, 4.36),
    (0.88, -0.69),
    (3.7, 4.97),
    (-2.42, 5.79),
    (2.98, 0.82),
    (-4.64, 2.79),
    (-0.34, 1.04),
    (-1.56, 1.71),
    (-1.89, 4.11),
    (3.25, 2.16),
    (-0.22, 1.44),
    (-4.15, 5.88),
    (0.26, 3.52),
    (1.32, 5.58),
    (-4.56, 3.63),
    (2.97, 1.15),
    (0.24, 5.6),
    (2.83, 5.37),
    (-4.23, 1.83),
    (-1.47, 3.74),
    (0.58, 3.92),
    (-2.7, 1.68),
    (-0.45, 5.67),
    (-0.59, 1.44),
    (1.42, -0.47),
    (0.56, -0.66),
    (-3.44, 5.96),
    (-1.81, 5.74),
    (1.73, 3.34),
    (3.44, 0.26),
    (2.59, 0.28),
    (-2.02, 2.12),
    (-0.45, -0.29),
    (-4.38, 5.25),
    (3.56, 4.0),
    (-3.38, 4.26),
    (-3.47, 1.81),
    (3.43, 3.16),
    (1.56, 1.33),
    (-0.01, 3.6),
    (3.15, -0.06),
    (0.13, 1.41),
    (0.32, 1.9),
    (-2.73, 5.82),
    (2.0, -0.17),
    (-0.2, -0.69),
    (3.13, 1.87),
    (0.95, 5.59),
    (-2.33, 1.62),
    (-1.28, 1.55),
    (-1.91, 3.72),
    (3.63, 5.3),
    (2.44, 5.39),
    (3.34, 2.46),
    (-4.67, 2.4),
    (1.12, -0.4),
    (-0.45, 0.73),
    (-1.47, 5.78),
    (-3.44, 3.92)
]

# offset = 5.1
# circle1 = plt.Circle((3.1, 2.1), radius=1, fill=False, ec="red")
# circle2 = plt.Circle((7.1, 2.1), radius=1, fill=False, ec="red")
# circle3 = plt.Circle((5.1-offset, 5.1-offset), radius=1, fill=False, ec="red")
# circle4 = plt.Circle((7.1, 8.1), radius=1, fill=False, ec="red")
# square1 = plt.Rectangle((2.35, 7.35), width=1.5, height=1.5, fill=False, ec="red")
# square2 = plt.Rectangle((0.35, 4.35), width=1.5, height=1.5, fill=False, ec="red")
# square3 = plt.Rectangle((8.35, 4.35), width=1.5, height=1.5, fill=False, ec="red")
inner_wall = plt.Rectangle((blc_x + offset, blc_y + offset), width=widthofmap, height= heightofmap, fill=False)
outer_wall = plt.Rectangle((blc_x, blc_y), width=widthofmap + offset, height=heightofmap + offset, fill=False)

# Convert the list of tuples into a numpy array
walls = np.array(walls)

# Plot the walls or obstacles
plt.scatter(walls[:, 0], walls[:, 1], color='red')

# plt.gca().add_patch(circle1)
# plt.gca().add_patch(circle2)
# plt.gca().add_patch(circle3)
# plt.gca().add_patch(circle4)
# plt.gca().add_patch(square1)
# plt.gca().add_patch(square2)
# plt.gca().add_patch(square3)
plt.gca().add_patch(inner_wall)
plt.gca().add_patch(outer_wall)
# plt.axis("scaled")


plt.grid(color='lightgray',linestyle='--')

