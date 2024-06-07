
import matplotlib.pyplot as plt
import numpy as np
from math import pi



# offset = 5.1
# circle1 = plt.Circle((3.1, 2.1), radius=1, fill=False, ec="red")
# circle2 = plt.Circle((7.1, 2.1), radius=1, fill=False, ec="red")
# circle3 = plt.Circle((5.1-offset, 5.1-offset), radius=1, fill=False, ec="red")
# circle4 = plt.Circle((7.1, 8.1), radius=1, fill=False, ec="red")
# square1 = plt.Rectangle((2.35, 7.35), width=1.5, height=1.5, fill=False, ec="red")
# square2 = plt.Rectangle((0.35, 4.35), width=1.5, height=1.5, fill=False, ec="red")
# # square3 = plt.Rectangle((8.35, 4.35), width=1.5, height=1.5, fill=False, ec="red")
# inner_wall = plt.Rectangle((blc_x + offset, blc_y + offset), width=widthofmap, height= heightofmap, fill=False)
# outer_wall = plt.Rectangle((blc_x, blc_y), width=widthofmap + offset, height=heightofmap + offset, fill=False)
# Plotting the final map

def create_map(walls, widthofmap=9, heightofmap=6, blc_x=4, blc_y=-1, offset=0.2):
    fig = plt.figure()
    plt.axes()
    plt.xlim(-5, 4.2)
    plt.ylim(-1, 7)
    plt.gca().invert_xaxis()  
    plt.gca().invert_yaxis()  
    # Convert the list of tuples into a numpy array
    walls = np.array(walls)

    # Plot the walls or obstacles
    plt.scatter(walls[:, 0], walls[:, 1], color='gray')
    plt.grid(color='lightgray',linestyle='--')

# plt.gca().add_patch(circle1)
# plt.gca().add_patch(circle2)
# plt.gca().add_patch(circle3)
# plt.gca().add_patch(circle4)
# plt.gca().add_patch(square1)
# plt.gca().add_patch(square2)
# plt.gca().add_patch(square3)
# plt.gca().add_patch(inner_wall)
# plt.gca().add_patch(outer_wall)
# plt.axis("scaled")




