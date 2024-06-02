#!/usr/bin/env python

# Single Travelling Salesman Problem

"""Problem Instance Generation Node"""
# This node is responsible for generating
# the TSP problem instance and writing it to
# a file that the solver can read.

import rospy
import random
import math
import os

NODE_NAME = "taskGeneration"

#*** File Paths for reading/writing ***#
"""Change to your own filepaths if you run on your own machine"""

#base_path = os.path.join(os.path.expanduser("~"), "Downloads/LKH-3.0.9")
base_path = os.path.join(os.path.expanduser("~"), "git/T11_multi_warehouse/main_ws/src/idk/LKH-3.0.9")

CONVERSION_FILE_PATH = os.path.join(base_path, "TSP_CONVERSION.txt")
COORDINATE_FILE_PATH = os.path.join(base_path, "TSP_COORDINATE.txt")
PAR_FILE_PATH = os.path.join(base_path, "TSP_TEST.par")
TASK_GENERATION_FILE_PATH = os.path.join(base_path, "TSP_TEST.txt")
BO = os.path.join(base_path, "distance_matrix.txt")
NEW_MATRIX = os.path.join(base_path, "matrixMaker.txt")


"""
#*** Make a global dictionary for other nodes to access ***#
NODE_COORDINATES = {
    0: (0.00, 0.00),
    1: (-2.913, 4.222),
    2: (-2.532, 4.162),
    3: (-0.890, 4.022),
    4: (-0.460, 3.972),
    5: (1.081, 3.892),
    6: (1.461, 3.852),
    7: (1.431, 3.342),
    8: (1.051, 3.392),
    9: (-0.440, 3.532),
    10: (-0.910, 3.572),
    11: (-2.532, 3.722),
    12: (-2.913, 3.762),
    13: (1.251, 1.841),
    14: (0.89, 1.821),
    15: (-0.66, 1.951),
    16: (-1.061, 1.981),
    17: (-2.662, 2.161),
    18: (-3.093, 2.181),
    19: (1.231, 1.29),
    20: (0.84, 1.34)
}
"""
NODE_COORDINATES = {
    0: (0.00, 0.00), # Dock
    1: (2.2, 3), #works
    2: (2.2, 5.2), #works
    3: (0.4, 5.2), #works
    4: (-0.9, 5.2), #works
    5: (-2.6, 5.2), #works
    6: (-3.8, 5.2), #works
    7: (-3.8, 4.6), #works
    8: (-2.7, 4.5), #works
    9: (-3.4, 4.2), #works
    10: (-1.15, 4.2), #works
    11: (0.9, 4.2), #works
    12: (0.9, 3.4), #works
    13: (-1.15, 3.5), #works
    14: (-3.4, 3.4), #works
    15: (-4, 3.1), #works
    16: (-4, 2.7), #works
    17: (-3.3, 1.9), #works
    18: (-1.25, 1.9), #works
    19: (0.9, 1.9), #works
    20: (0.9, 1.5) #works
    }

# This is the full distance matrix for all nodes. this is not dynamic. Change to subscribe/reading txt file
"""
FULL_DISTANCE_MATRIX = [
    [0, 7.36, 7.79, 5.35, 5.02, 4.42, 4.52, 3.93, 3.83, 4.62, 4.95, 6.7, 7.09, 2.44, 2.24, 4.39, 4.79, 6.93, 7.19, 1.78, 1.85],
    [7.36, 0, 0.2, 2.28, 2.61, 4.79, 4.98, 5.02, 4.52, 2.9, 2.54, 0.5, 0.5, 5.38, 4.98, 3.23, 2.97, 2.28, 2.21, 5.87, 5.51],
    [7.79, 0.2, 0, 2.67, 2.77, 5.02, 5.25, 5.11, 4.52, 2.8, 2.11, 0.4, 0.59, 4.98, 4.59, 3.2, 2.8, 2.18, 2.44, 5.44, 5.08],
    [5.35, 2.28, 2.67, 0, 0.2, 2.24, 2.64, 2.84, 2.94, 0.66, 0.59, 2.24, 2.64, 3.4, 3.3, 2.28, 2.18, 3.07, 2.97, 3.89, 3.53],
    [5.02, 2.61, 2.77, 0.2, 0, 3.2, 3.37, 2.97, 2.14, 0.4, 0.82, 3.56, 3.4, 3.1, 2.87, 2.24, 2.67, 3.37, 3.76, 3.7, 3.3],
    [4.42, 4.79, 5.02, 2.24, 3.2, 0, 0.2, 0.5, 0.59, 2.31, 3.23, 4.98, 5.08, 2.31, 2.31, 3.56, 4.49, 5.18, 5.15, 2.9, 2.9],
    [4.52, 4.98, 5.25, 2.64, 3.37, 0.2, 0, 0.59, 0.79, 2.67, 3.3, 4.82, 5.21, 2.15, 2.31, 3.13, 3.53, 5.31, 5.71, 2.54, 3.0],
    [3.93, 5.02, 5.11, 2.84, 2.97, 0.5, 0.59, 0, 0.69, 2.84, 3.3, 5.05, 5.61, 1.78, 1.95, 3.33, 3.5, 5.34, 5.91, 2.34, 2.54],
    [3.83, 4.52, 4.52, 2.94, 2.14, 0.59, 0.79, 0.69, 0, 2.71, 2.67, 4.42, 4.88, 1.98, 1.72, 2.97, 3.33, 5.64, 5.12, 2.21, 2.74],
    [4.62, 2.9, 2.8, 0.66, 0.4, 2.31, 2.67, 2.84, 2.71, 0, 0.89, 3.1, 3.23, 2.64, 2.24, 1.75, 1.95, 3.1, 3.17, 2.84, 2.74],
    [4.95, 2.54, 2.11, 0.59, 0.82, 3.23, 3.3, 3.3, 2.67, 0.89, 0, 2.05, 2.44, 3.07, 2.87, 1.72, 1.91, 2.94, 3.14, 3.47, 3.27],
    [6.7, 0.5, 0.4, 2.24, 3.56, 4.98, 4.82, 5.05, 4.42, 3.1, 2.05, 0, 1.15, 4.62, 4.49, 2.71, 2.31, 1.62, 2.08, 5.12, 4.88],
    [7.09, 0.5, 0.59, 2.64, 3.4, 5.08, 5.21, 5.61, 4.88, 3.23, 2.44, 1.15, 0, 5.68, 4.82, 3.07, 2.8, 1.68, 1.52, 5.41, 5.11],
    [2.44, 5.38, 4.98, 3.4, 3.1, 2.31, 2.15, 1.78, 1.98, 2.64, 3.07, 4.62, 5.68, 0, 0.5, 2.97, 3.37, 5.51, 5.71, 0.56, 0.79],
    [2.24, 4.98, 4.59, 3.3, 2.87, 2.31, 2.31, 1.95, 1.72, 2.24, 2.87, 4.49, 4.82, 0.5, 0, 3.23, 3.47, 4.59, 5.12, 0.5, 0.59],
    [4.39, 3.23, 3.2, 2.28, 2.24, 3.56, 3.13, 3.33, 2.97, 1.75, 1.72, 2.71, 3.07, 2.97, 3.23, 0, 0.66, 2.74, 3.33, 3.76, 3.6],
    [4.79, 2.97, 2.8, 2.18, 2.67, 4.49, 3.53, 3.5, 3.33, 1.95, 1.91, 2.31, 2.8, 3.37, 3.47, 0.66, 0, 2.21, 2.77, 3.3, 3.0],
    [6.93, 2.28, 2.18, 3.07, 3.37, 5.18, 5.31, 5.34, 5.64, 3.1, 2.94, 1.62, 1.68, 5.51, 4.59, 2.74, 2.21, 0, 0.79, 5.35, 5.41],
    [7.19, 2.21, 2.44, 2.97, 3.76, 5.15, 5.71, 5.91, 5.12, 3.17, 3.14, 2.08, 1.52, 5.71, 5.12, 3.33, 2.77, 0.79, 0, 6.3, 6.17],
    [1.78, 5.87, 5.44, 3.89, 3.7, 2.9, 2.54, 2.34, 2.21, 2.84, 3.47, 5.12, 5.41, 0.56, 0.5, 3.76, 3.3, 5.35, 6.3, 0, 0.66],
    [1.85, 5.51, 5.08, 3.53, 3.3, 2.9, 3.0, 2.54, 2.74, 2.74, 3.27, 4.88, 5.11, 0.79, 0.59, 3.6, 3.0, 5.41, 6.17, 0.66, 0]
]
"""

FULL_DISTANCE_MATRIX = [
    [0, 4.69, 6.34, 6.01, 6.96, 7.92, 9.57, 8.51, 8.25, 7.99, 5.94, 4.79, 3.99, 5.25, 7.29, 8.02, 7.92, 7.66, 5.25, 2.48, 2.14],
    [4.69, 0, 2.77, 3.96, 5.21, 6.5, 7.85, 7.92, 6.7, 7.09, 5.21, 2.54, 1.92, 5.58, 6.66, 6.9, 7.23, 6.43, 4.09, 3.07, 2.97],
    [6.34, 2.77, 0, 2.34, 3.76, 5.84, 6.93, 10.43, 5.81, 7.36, 5.15, 2.11, 3.0, 4.98, 8.25, 8.78, 8.78, 8.05, 5.71, 4.55, 4.98],
    [6.01, 3.96, 2.34, 0, 1.88, 3.73, 5.05, 5.08, 3.8, 5.05, 2.21, 1.22, 1.98, 3.3, 5.25, 5.97, 6.37, 7.69, 4.79, 3.83, 4.26],
    [6.96, 5.21, 3.76, 1.88, 0, 2.61, 3.5, 3.7, 2.57, 3.36, 1.32, 2.74, 3.23, 2.51, 4.29, 4.92, 5.05, 5.28, 3.7, 5.18, 4.69],
    [7.92, 6.5, 5.84, 3.73, 2.61, 0, 2.38, 2.34, 0.99, 1.52, 2.08, 4.22, 5.15, 2.71, 2.31, 2.94, 3.3, 3.76, 4.85, 5.44, 5.94],
    [9.57, 7.85, 6.93, 5.05, 3.5, 2.38, 0, 0.92, 1.58, 1.12, 3.1, 5.31, 6.27, 4.19, 2.08, 2.64, 3.2, 4.42, 4.39, 6.53, 7.16],
    [8.51, 7.92, 10.43, 5.08, 3.7, 2.34, 0.92, 0, 1.19, 2.93, 3.33, 5.84, 5.91, 4.19, 3.63, 4.22, 2.57, 4.72, 5.58, 6.47, 6.86],
    [8.25, 6.7, 5.81, 3.8, 2.57, 0.99, 1.58, 1.19, 0, 1.19, 1.78, 4.72, 5.38, 2.64, 1.78, 2.15, 2.51, 3.4, 4.52, 5.84, 5.68],
    [7.99, 7.09, 7.36, 5.05, 3.36, 1.52, 1.12, 2.93, 1.19, 0, 2.87, 5.71, 5.81, 4.72, 1.22, 1.98, 2.18, 2.77, 3.63, 5.77, 6.4],
    [5.94, 5.21, 5.15, 2.21, 1.32, 2.08, 3.1, 3.33, 1.78, 2.87, 0, 2.61, 4.39, 0.96, 4.88, 4.65, 4.75, 4.29, 2.74, 4.16, 3.83],
    [4.79, 2.54, 2.11, 1.22, 2.74, 4.22, 5.31, 5.84, 4.72, 5.71, 2.61, 0, 1.52, 4.29, 5.97, 6.77, 6.63, 6.7, 4.32, 2.77, 3.17],
    [3.99, 1.92, 3.0, 1.98, 3.23, 5.15, 6.27, 5.91, 5.38, 5.81, 4.39, 1.52, 0, 2.77, 5.25, 5.77, 6.04, 5.84, 3.0, 1.98, 2.21],
    [5.25, 5.58, 4.98, 3.3, 2.51, 2.71, 4.19, 4.19, 2.64, 4.72, 0.96, 4.29, 2.77, 0, 3.3, 3.9, 3.89, 3.56, 1.98, 4.19, 4.16],
    [7.29, 6.66, 8.25, 5.25, 4.29, 2.31, 2.08, 3.63, 1.78, 1.22, 4.88, 5.97, 5.25, 3.3, 0, 1.22, 1.19, 2.11, 3.1, 5.25, 5.68],
    [8.02, 6.9, 8.78, 5.97, 4.92, 2.94, 2.64, 4.22, 2.15, 1.98, 4.65, 6.77, 5.77, 3.9, 1.22, 0, 0.59, 1.52, 3.66, 5.84, 5.94],
    [7.92, 7.23, 8.78, 6.37, 5.05, 3.3, 3.2, 2.57, 2.51, 2.18, 4.75, 6.63, 6.04, 3.89, 1.19, 0.59, 0, 1.95, 4.85, 5.64, 6.04],
    [7.66, 6.43, 8.05, 7.69, 5.28, 3.76, 4.42, 4.72, 3.4, 2.77, 4.29, 6.7, 5.84, 3.56, 2.11, 1.52, 1.95, 0, 3.86, 5.18, 5.61],
    [5.25, 4.09, 5.71, 4.79, 3.7, 4.85, 4.39, 5.58, 4.52, 3.63, 2.74, 4.32, 3.0, 1.98, 3.1, 3.66, 4.85, 3.86, 0, 2.77, 3.04],
    [2.48, 3.07, 4.55, 3.83, 5.18, 5.44, 6.53, 6.47, 5.84, 5.77, 4.16, 2.77, 1.98, 4.19, 5.25, 5.84, 5.64, 5.18, 2.77, 0, 0.59],
    [2.14, 2.97, 4.98, 4.26, 4.69, 5.94, 7.16, 6.86, 5.68, 6.4, 3.83, 3.17, 2.21, 4.16, 5.68, 5.94, 6.04, 5.61, 3.04, 0.59, 0]
]


original_to_reference_mapping = {}
selected_nodes = []
num_nodes_to_pick = 0

#*** Matrix Making Functions and Process ***#
# The LKH solver needs a distance matrix of the nodes to provide a distance based cost solution
# This should be set up as a rosservice to request the full node distance matrix
# In lieu, this code readds from a text file.
""" 1. Finding the real node number from the reference number

    2. Creating a smaller distance matrix that only includes the selected_nodes
    2.1 Iterate over each pair of nodes in selected_nodes
    2.2 Retrieve the real node numbers from the reference numbers
    2.3 Retrieve the corresponding distance from the full distance matrix
    2.4 Add the distance to the row until all distances are added

    3. Write the smaller distance matrix to a file for the TSP solver to read
    3.1 Open the file and write each row of the matrix to the file as strings
    3.2 Separate each distance value with a tab (I hope this doesnt mess up reading it)
"""

def get_real_node(reference_number):
    return original_to_reference_mapping[reference_number]

def create_smaller_distance_matrix(FULL_DISTANCE_MATRIX, selected_nodes):
    smaller_distance_matrix = []

    for node1, _, _ in selected_nodes:
        row = []
        real_node1 = get_real_node(node1)
        for node2, _, _ in selected_nodes:
            real_node2 = get_real_node(node2)
            # Retrieve distance from full matrix based on real node numbers
            row.append(FULL_DISTANCE_MATRIX[real_node1][real_node2])
        smaller_distance_matrix.append(row)

    return smaller_distance_matrix

def write_distance_matrix_to_file(new_distance_matrix, NEW_MATRIX):
    with open(NEW_MATRIX, 'w') as file:
        for row in new_distance_matrix:
            # Convert each distance value to a string and join them with tabs
            row_str = '\t'.join(map(str, row))
            # Write the row to the file
            file.write(row_str + '\n')

#*** Random Node Picking process for the parameter file ***#
            
# The LKH solver requires the parameter file to label the nodes with reference numbers starting from 1 and incrementing by 1.      
## This has been designed so that a user input number of node locations can be chosen, and the code will randomly select that number from the pool of locations.
""" 1. Choose length of pick list
    2. Create pick list and keep track of reference and original node numbers
    3. Create the necessary files for the LKH Solver:
        * Parameter file
        * Problem file
        * Reference node to coordinate mapping file
        * Reference node to original node mapping file
"""
def generate_tasks(num_nodes_to_pick):
    global selected_nodes
    selected_nodes = []
    reference_node = 0
    selected_nodes.append((1, 0, NODE_COORDINATES[0]))  # Add the Dock node first to the list of selected nodes
    original_to_reference_mapping[1] = reference_node # Store the mapping
    reference_node += 1

    del NODE_COORDINATES[0]  # Remove the Dock node from the NODE_COORDINATES list

    for i in range(1, num_nodes_to_pick + 1):
        # Randomly select a node from the list of NODE_COORDINATES
        original_node = random.sample(list(NODE_COORDINATES.keys()), 1)[0]
        # Increment and assign the reference number
        reference_node += 1
        # Add the reference number, node number, and coordinates to the array
        selected_nodes.append((reference_node, original_node, NODE_COORDINATES[original_node]))
        # Store the mapping
        original_to_reference_mapping[reference_node] = original_node
        # Remove the selected node from the NODE_COORDINATES list
        del NODE_COORDINATES[original_node]

    return selected_nodes, original_to_reference_mapping

def task_generation(num_nodes_to_pick):
    global original_to_reference_mapping
    #rospy.init_node('taskGeneration', anonymous=True)
    selected_nodes, original_to_reference_mapping = generate_tasks(num_nodes_to_pick)

    smaller_distance_matrix = create_smaller_distance_matrix(FULL_DISTANCE_MATRIX, selected_nodes)
    write_distance_matrix_to_file(smaller_distance_matrix, NEW_MATRIX)

    with open(PAR_FILE_PATH, 'w') as file:
        # file.write("PROBLEM_FILE = /home/chloe/Downloads/LKH-3.0.9/TSP_TEST.txt\n")
        # file.write("OUTPUT_TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/TSP_TEST_OUTPUT_TOUR\n")
        # file.write("TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/TSP_TEST_TOUR\n")
        file.write("PROBLEM_FILE = {}\n".format(os.path.join(base_path, "TSP_TEST.txt")))
        file.write("OUTPUT_TOUR_FILE = {}\n".format(os.path.join(base_path, "TSP_TEST_OUTPUT_TOUR")))
        file.write("TOUR_FILE = {}\n".format(os.path.join(base_path, "TSP_TEST_TOUR")))

    with open(CONVERSION_FILE_PATH, 'w') as file:
        file.write("{\n")
        global reference
        global original
        for reference, original, (x, y) in selected_nodes:
            file.write('    "{}": {},\n'.format(reference, original))
        file.seek(0, os.SEEK_END)
        file.seek(file.tell() - 2, os.SEEK_SET)
        file.truncate()
        file.write("\n}")

    with open(COORDINATE_FILE_PATH, 'w') as file:
        file.write("{\n")
        for reference, original, (x, y) in selected_nodes:
            file.write('    "{}": [{}, {}],\n'.format(reference, x, y))
        file.seek(0, os.SEEK_END)
        file.seek(file.tell() - 2, os.SEEK_SET)
        file.truncate()
        file.write("\n}")

    """
    with open(TASK_GENERATION_FILE_PATH, 'w') as file:
        file.write("NAME : TSP_TEST\n") 
        file.write("TYPE : TSP\n")
        file.write("COMMENT : Chloe Judson, TSP Test\n")
        file.write("DIMENSION : {}\n".format(num_nodes_to_pick + 1))
        file.write("EDGE_WEIGHT_TYPE : MAN_2D\n")
        file.write("NODE_COORD_TYPE : TWOD_COORDS\n")
        file.write("DISPLAY_DATA_TYPE : COORD_DISPLAY\n")
        file.write("NODE_COORD_SECTION\n")

        for reference, original_node, (x, y) in selected_nodes:
            file.write("{} {} {}\n".format(reference, x, y))

        file.write("EOF\n")
    """

    with open(NEW_MATRIX, 'r') as file:
        path_planning_edge_weights = file.read()
    
    with open(TASK_GENERATION_FILE_PATH, 'w') as file:
        file.write("NAME : TSP_TEST\n") 
        file.write("TYPE : TSP\n")
        file.write("COMMENT : Chloe Judson, Bo Coordinate Test\n")
        #file.write("DIMENSION : {}\n".format(num_nodes_to_pick + 1))
        file.write("DIMENSION : {}\n".format(num_nodes_to_pick + 1))
        #*** Change EGDE_WEIGHT_TYPE to EXPLICIT ***#
        file.write("EDGE_WEIGHT_TYPE : EXPLICIT\n")
        #*** Add EDGE_WEIGHT_FORMAT to LOWER_DIAG_ROW/LOWER_ROW/FULL_MATRIX ***#
        file.write("EDGE_WEIGHT_FORMAT : FULL_MATRIX\n")
        #*** Change DISPLAY_DATA_TYPE to TWOD_DISPLAY ***#
        file.write("DISPLAY_DATA_TYPE : TWOD_DISPLAY\n")
        #*** Add Node Coordinates to the file ***#
        #*** Change NODE_COORD_SECTION to EDGE_WEIGHT_SECTION ***#
        file.write("EDGE_WEIGHT_SECTION\n")
        #*** Write the edge weights from Bo's Path Planning to the task generation file ***#
        file.write(path_planning_edge_weights)
        file.write("EOF\n")

def node_picking_num():
    num_valid_entries = len(NODE_COORDINATES) - 1        
    num_nodes_to_pick = int(input("Enter the pick list length (up to " + str(num_valid_entries) + "): "))
    return num_nodes_to_pick

def main():
  try:
        global num_nodes_to_pick
        num_nodes_to_pick = node_picking_num()
        task_generation(num_nodes_to_pick)

        print('Reference to Original Node Mapping:', original_to_reference_mapping)
        print('Node List:', selected_nodes)
  except rospy.ROSInterruptException:
    pass
  
if __name__ == '__main__':
    rospy.init_node('taskGeneration', anonymous=True)
    # INITIALISE NODE HERE!!
    main()