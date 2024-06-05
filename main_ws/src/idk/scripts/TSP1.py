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



NODE_COORDINATES = {
    0: (0.00, 0.00), # Dock
    1: (2.2, 3), #works
    2: (2.2, 5.2), #works
    3: (0.4, 5.2), #works
    4: (-0.9, 5.2), #works
    5: (-2.6, 5.2), #works
    6: (-3.8, 5.2), #works
    7: (-3.8, 4.7), #works
    8: (-2.7, 4.5), #works
    9: (-3.4, 4.2), #works
    10: (-1.15, 4.2), #works
    11: (0.9, 4.2), #works
    12: (0.9, 3.4), #works
    13: (-1.15, 3.5), #works
    14: (-3.4, 3.4), #works
    15: (-4, 3.1), #works
    16: (-4, 2.7), #works
    17: (-3.3, 2.0), #works
    18: (-1.25, 1.9), #works
    19: (0.9, 1.9), #works
    20: (0.9, 1.5) #works
    }


FULL_DISTANCE_MATRIX = [
	[0, 4.55, 6.34, 6.01, 6.96, 7.92, 8.84, 8.65, 8.28, 8.05, 6.34, 4.79, 3.99, 5.25, 7.29, 7.99, 7.99, 7.89, 5.71, 2.48, 2.14],
	[4.55, 0, 2.77, 3.96, 5.21, 6.5, 8.58, 7.95, 6.7, 7.79, 5.21, 2.54, 3.3, 4.19, 6.66, 6.9, 7.23, 6.2, 4.09, 2.57, 2.51],
	[6.34, 2.77, 0, 2.34, 3.76, 5.84, 7.62, 7.03, 6.27, 7.36, 4.88, 2.11, 2.87, 5.87, 8.18, 8.94, 8.78, 8.45, 5.64, 5.58, 4.98],
	[6.01, 3.96, 2.34, 0, 1.88, 3.73, 5.05, 7.26, 3.8, 5.02, 2.21, 1.22, 1.98, 3.3, 5.18, 5.68, 6.6, 7.46, 6.01, 3.83, 4.26],
	[6.96, 5.21, 3.76, 1.88, 0, 2.61, 3.5, 3.6, 3.66, 3.53, 1.35, 2.74, 3.23, 2.11, 4.16, 4.69, 5.15, 4.88, 3.89, 4.55, 5.44],
	[7.92, 6.5, 5.84, 3.73, 2.61, 0, 2.38, 1.78, 0.99, 1.91, 1.95, 4.22, 4.75, 3.04, 2.94, 3.0, 5.94, 3.96, 4.03, 5.54, 6.04],
	[8.84, 8.58, 7.62, 5.05, 3.5, 2.38, 0, 1.09, 1.58, 1.12, 3.1, 5.31, 6.27, 5.01, 2.44, 2.87, 3.23, 3.89, 5.21, 6.8, 6.93],
	[8.65, 7.95, 7.03, 7.26, 3.6, 1.78, 1.09, 0, 1.19, 1.22, 2.87, 5.41, 5.87, 3.3, 1.55, 1.95, 2.34, 3.1, 4.69, 7.39, 7.29],
	[8.28, 6.7, 6.27, 3.8, 3.66, 0.99, 1.58, 1.19, 0, 3.07, 1.78, 4.72, 5.12, 2.21, 4.55, 4.16, 4.52, 5.15, 4.06, 5.25, 5.68],
	[8.05, 7.79, 7.36, 5.02, 3.53, 1.91, 1.12, 1.22, 3.07, 0, 2.57, 5.18, 5.61, 3.3, 1.22, 1.58, 1.91, 2.64, 3.43, 6.14, 6.5],
	[6.34, 5.21, 4.88, 2.21, 1.35, 1.95, 3.1, 2.87, 1.78, 2.57, 0, 2.61, 3.07, 0.96, 3.27, 3.86, 3.96, 3.8, 2.8, 4.12, 3.83],
	[4.79, 2.54, 2.11, 1.22, 2.74, 4.22, 5.31, 5.41, 4.72, 5.18, 2.61, 0, 0.99, 3.2, 5.77, 6.86, 7.62, 5.91, 4.32, 3.0, 3.23],
	[3.99, 3.3, 2.87, 1.98, 3.23, 4.75, 6.27, 5.87, 5.12, 5.61, 3.07, 0.99, 0, 2.84, 5.25, 5.77, 6.04, 6.04, 3.0, 1.98, 2.21],
	[5.25, 4.19, 5.87, 3.3, 2.11, 3.04, 5.01, 3.3, 2.21, 3.3, 0.96, 3.2, 2.84, 0, 3.3, 3.9, 3.89, 3.5, 1.98, 3.24, 3.27],
	[7.29, 6.66, 8.18, 5.18, 4.16, 2.94, 2.44, 1.55, 4.55, 1.22, 3.27, 5.77, 5.25, 3.3, 0, 1.22, 1.19, 1.78, 3.1, 5.38, 5.71],
	[7.99, 6.9, 8.94, 5.68, 4.69, 3.0, 2.87, 1.95, 4.16, 1.58, 3.86, 6.86, 5.77, 3.9, 1.22, 0, 0.59, 1.39, 3.43, 6.04, 5.94],
	[7.99, 7.23, 8.78, 6.6, 5.15, 5.94, 3.23, 2.34, 4.52, 1.91, 3.96, 7.62, 6.04, 3.89, 1.19, 0.59, 0, 1.19, 7.49, 7.79, 5.87],
	[7.89, 6.2, 8.45, 7.46, 4.88, 3.96, 3.89, 3.1, 5.15, 2.64, 3.8, 5.91, 6.04, 3.5, 1.78, 1.39, 1.19, 0, 3.27, 5.87, 5.87],
	[5.71, 4.09, 5.64, 6.01, 3.89, 4.03, 5.21, 4.69, 4.06, 3.43, 2.8, 4.32, 3.0, 1.98, 3.1, 3.43, 7.49, 3.27, 0, 2.77, 3.1],
	[2.48, 2.57, 5.58, 3.83, 4.55, 5.54, 6.8, 7.39, 5.25, 6.14, 4.12, 3.0, 1.98, 3.24, 5.38, 6.04, 7.79, 5.87, 2.77, 0, 0.59],
	[2.14, 2.51, 4.98, 4.26, 5.44, 6.04, 6.93, 7.29, 5.68, 6.5, 3.83, 3.23, 2.21, 3.27, 5.71, 5.94, 5.87, 5.87, 3.1, 0.59, 0]
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
