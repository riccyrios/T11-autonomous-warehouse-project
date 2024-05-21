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

#*** File Paths for writing ***#
"""Change to your own filepaths if you run on your own machine"""

CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_CONVERSION.txt"
COORDINATE_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_COORDINATE.txt"
PAR_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST.par"
TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST.txt"
BOS_EDGE_WEIGHTS_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/Bos_Path_Planning_Output.txt"

#*** Make a global dictionary for other nodes to access ***#
# This is not needed if path planning costs are used and there is no graphical representation

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

original_to_reference_mapping = {}
selected_nodes = []
num_nodes_to_pick = 0

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
    rospy.init_node('taskGeneration', anonymous=True)
    selected_nodes, original_to_reference_mapping = generate_tasks(num_nodes_to_pick)

    with open(PAR_FILE_PATH, 'w') as file:
        file.write("PROBLEM_FILE = /home/chloe/Downloads/LKH-3.0.9/TSP_TEST.txt\n")
        file.write("OUTPUT_TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/TSP_TEST_OUTPUT_TOUR\n")
        file.write("TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/TSP_TEST_TOUR\n")

    with open(CONVERSION_FILE_PATH, 'w') as file:
        file.write("{\n")
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
    main()