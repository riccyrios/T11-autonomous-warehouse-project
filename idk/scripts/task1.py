#!/usr/bin/env python

"""Problem Instance Generation Node"""
# This node is responsible for generating
# the TSP problem instance and writing it to
# a file that the solver can read.

import rospy
import random
import math
import os

NODE_NAME = "taskGeneration"

#*** File Paths for writing ***#
"""Change to your own filepaths if you run on your own machine"""

TASK_CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_CONVERSION.txt"
TASK_COORDINATES_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_COORDINATES.txt"
PAR_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.par"
TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.txt"
BOS_EDGE_WEIGHTS_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/Bos_Path_Planning_Output.txt"

#*** Make a global dictionary for other nodes to access ***#
NODE_COORDINATES = {
    0: (0.00, 0.00), # Dock
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

original_to_reference_mapping = {}
selected_nodes = []

#*** Random Node Picking process for the parameter file ***#
""" 1. Pick the Dock node
    1.1 Assign the reference number 1
    1.2 Write the coordinates of the Dock node and the reference number to the parameter file
    1.3 Add the reference number, node number, and coordinates to an array
    1.4 Remove the Dock node from the NODE_COORDINATES list

    2. Randomly select a coordinate from the NODE_COORDINATES dictionary
    2.1 Increment and assign the reference number
    2.2 Write the coordinates of the node and the reference number to the parameter file
    2.3 Add the reference number, node number, and coordinates to the array
    
    3. Repeat loop until the num_nodes_to_pick is reached
"""

#*** Introduce a parameter for the minimum number of cities to be allocated per salesman ***#
def calculate_min_cities(num_nodes_to_pick, num_salesmen):
    min_cities_per_salesmen = math.ceil((num_nodes_to_pick / num_salesmen) * 0.4)
    return int(min_cities_per_salesmen)

#*** Generate the task list ***#
def generate_tasks(num_nodes_to_pick):
    global selected_nodes
    selected_nodes = []
    ## original_to_reference_mapping = {0: 0}  # Mapping from original node numbers to reference numbers

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
    rospy.init_node('taskGeneration', anonymous=True)
    min_cities_per_salesmen = calculate_min_cities(num_nodes_to_pick, num_salesmen)
    selected_nodes, original_to_reference_mapping = generate_tasks(num_nodes_to_pick)

    #*** Write the original and reference numbers to the parameter file ***#
    with open(PAR_FILE_PATH, 'w') as file:
        file.write("PROBLEM_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.txt\n")
        file.write("MTSP_MIN_SIZE = {}\n".format(min_cities_per_salesmen))
        file.write("MTSP_OBJECTIVE = MINMAX\n")
        file.write("MTSP_SOLUTION_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_SOLUTION\n")
        file.write("OUTPUT_TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_OUTPUT_TOUR\n")
        file.write("TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_TOUR\n")
        # Print mapping to the par file for funsies
        ## THIS BREAKS THE CPODE THIS IS NOT A COMMENT !!!!!!!!!
        ##file.write("#NODE_MAPPING = {}\n".format(original_to_reference_mapping))

        #*** MTSP_MIN_SIZE = < integer >: The minimum number of cities that must be visited by each salesman.
        #*** MTSP_MAX_SIZE = < integer >: The maximum number of cities that can be visited by each salesman.
        #*** MTSP_OBJECTIVE = MINMAX: The objective is to minimize the maximum distance traveled by any salesman.
        #*** MTSP_OBJECTIVE = MINMAX_SIZE: The objective is to minimize the size of the largest route
        #*** MTSP_OBJECTIVE = MINSUM: The objective is to minimize the total distance traveled by all salesmen.

    #*** Write the original, reference, and coordinates to the conversion file ***#
    with open(TASK_CONVERSION_FILE_PATH, 'w') as file:
        #file.write("Ref | Orig | Coord\n\n")
        file.write("{\n")
        for reference, original, (x, y) in selected_nodes:
            #file.write("{} | {} | ({}, {})\n".format(reference, original, x, y))
            file.write('    "{}": {},\n'.format(reference, original))
        file.seek(0, os.SEEK_END)  # Go to the end of the file
        file.seek(file.tell() - 2, os.SEEK_SET)  # Go back 2 characters from the end
        file.truncate()  # Remove the last 2 characters
        file.write("\n}")

    with open(TASK_COORDINATES_FILE_PATH, 'w') as file:
        file.write("{\n")
        for reference, original, (x, y) in selected_nodes:
            file.write('    "{}": [{}, {}],\n'.format(reference, x, y))
        file.seek(0, os.SEEK_END)  # Go to the end of the file
        file.seek(file.tell() - 2, os.SEEK_SET)  # Go back 2 characters from the end
        file.truncate()  # Remove the last 2 characters
        file.write("\n}")

    #*** Write the selected nodes to the task generation file ***#
    with open(TASK_GENERATION_FILE_PATH, 'w') as file:
        file.write("NAME : MTSP_TEST\n") 
        file.write("TYPE : TSP\n")
        file.write("COMMENT : Chloe Judson, Subsystem Test\n")
        file.write("SALESMEN : {}\n".format(num_salesmen))
        file.write("DIMENSION : {}\n".format(num_nodes_to_pick + 1))
        file.write("EDGE_WEIGHT_TYPE : MAN_2D\n")
        file.write("NODE_COORD_TYPE : TWOD_COORDS\n")
        file.write("DISPLAY_DATA_TYPE : COORD_DISPLAY\n")
        file.write("NODE_COORD_SECTION\n")

        for reference, original_node, (x, y) in selected_nodes:
            file.write("{} {} {}\n".format(reference, x, y))

        file.write("EOF\n")

    """
    #*** Using the Edge Weights from Bo's Path Planning, dynamic integration ***#
    # Bo's Path Planning Output Text File
    with open(Bos_Path_Planning_Output.txt, 'r') as file:
        path_planning_edge_weights = file.read()
    
    with open(TASK_GENERATION_FILE_PATH, 'w') as file:
        file.write("NAME : MTSP_TEST\n") 
        file.write("TYPE : TSP\n")
        file.write("COMMENT : Chloe Judson, Bo Coordinate Test\n")
        file.write("SALESMEN : {}\n".format(num_salesmen))
        file.write("DIMENSION : {}\n".format(num_nodes_to_pick + 1))
        #*** Change EGDE_WEIGHT_TYPE to EXPLICIT ***#
        file.write("EDGE_WEIGHT_TYPE : EXPLICIT\n")
        #*** Add EDGE_WEIGHT_FORMAT to LOWER_DIAG_ROW/LOWER_ROW/FULL_MATRIX ***#
        #*** Change DISPLAY_DATA_TYPE to TWOD_DISPLAY ***#
        file.write("DISPLAY_DATA_TYPE : TWOD_DISPLAY\n")
        #*** Add Node Coordinates to the file ***#
        #*** Change NODE_COORD_SECTION to EDGE_WEIGHT_SECTION ***#
        file.write("EDGE_WEIGHT_SECTION\n")
        #*** Write the edge weights from Bo's Path Planning to the task generation file ***#
        file.write(path_planning_edge_weights)
        file.write("EOF\n")
    """

def node_picking_num():
    num_valid_entries = len(NODE_COORDINATES) - 1        
    num_nodes_to_pick = int(input("Enter the pick list length (up to " + str(num_valid_entries) + "): "))
    return num_nodes_to_pick


if __name__ == '__main__':
  try:
    
    num_nodes_to_pick = node_picking_num()
    num_salesmen = int(input("Enter the number of Teenage Mutant Ninja Turtlebots: "))

    if (num_nodes_to_pick, num_salesmen) == (1, 1):
        print("Generating a task list with 1 node for 1 Turtlebot...")
    elif num_nodes_to_pick == 1:
        if num_salesmen > num_nodes_to_pick:
            print("Seriously -_-...? This is a bit redundant...")
        print("Generating a task list with 1 node for {} Turtlebots...".format(num_salesmen))
    elif num_salesmen == 1:
        print("Generating a task list with {} nodes for 1 Turtlebot...".format(num_nodes_to_pick))
    else:
        print("Generating a problem instance with {} nodes for {} Turtlebots...".format(num_nodes_to_pick, num_salesmen))

    task_generation(num_nodes_to_pick)

    print('Reference to Original Node Mapping:', original_to_reference_mapping)
    print('Node List:', selected_nodes)

  except rospy.ROSInterruptException:
    pass