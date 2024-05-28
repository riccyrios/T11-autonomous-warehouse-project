#!/usr/bin/env python

"""Problem Instance Solver Node"""
# TSP Solver Output Processing Node
# This node is responsible for executing 
# the TSP solver with the generated problem 
# instance and processing its output.

import rospy
import subprocess
import re
import json
import os

from idk.msg import Tour

NODE_NAME = "taskProcessing"

#*** File Paths for writing ***#
"""Change to your own filepaths if you run on your own machine"""
"""Feel free to change the file names as well, I have made it a little confusing"""

base_path = os.path.join(os.path.expanduser("~"), "Downloads/LKH-3.0.9")

# This is the path to the LKH TSP solver
#SOLVER_EXECUTABLE_PATH = "/home/chloe/Downloads/LKH-3.0.9/LKH"
SOLVER_EXECUTABLE_PATH = os.path.join(base_path, "LKH")
# This is the path to the file that the solver reads
#TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST.txt"
TASK_GENERATION_FILE_PATH = os.path.join(base_path, "TSP_TEST.txt")
# This is the path to the parameter file that the solver reads
#PAR_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST.par"
PAR_FILE_PATH = os.path.join(base_path, "TSP_TEST.par")
# This is the path to the file that contains the dictionary mapping reference numbers to real node numbers
#CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_CONVERSION.txt"
CONVERSION_FILE_PATH = os.path.join(base_path, "TSP_CONVERSION.txt")
# This is the path to the file that contains the dictionary mappping reference numbers to coordinates in JSON format
#COORDINATE_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_COORDINATE.txt"
COORDINATE_FILE_PATH = os.path.join(base_path, "TSP_COORDINATE.txt")
# This is the path to the file that contains the best tour found by the solver
#BO = "/home/chloe/Downloads/LKH-3.0.9/TSP_BO.txt"
BO = os.path.join(base_path, "TSP_BO.txt")
# This is the path to the file that contains the solution tour
#SOLUTION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST_TOUR"
SOLUTION_FILE_PATH = os.path.join(base_path, "TSP_TEST_TOUR")

mapping = {}

def run_tsp_solver():
    subprocess.call([SOLVER_EXECUTABLE_PATH, PAR_FILE_PATH])


# Delete any old TSP files, this is not important for the TSP version, but it is for the mTSP version
def delete_old_tour_file():
    directory = "/home/chloe/Downloads/LKH-3.0.9/"
    file_path = os.path.join(directory, "Tour_0")

    if os.path.exists(file_path):
        os.remove(file_path)
        print("'{}' has been deleted.".format(file_path))
    else:
        print("No such file: '{}'".format(file_path))

# Idk why I couldn't get the JSON file to work with the keys as ints, but this function turns the key strings into ints
def node_mapping():
    with open(CONVERSION_FILE_PATH, 'r') as f:
        mapping = json.load(f)
    mapping = {int(k): v for k, v in mapping.items()}
    return mapping

# This function goes through each tour (only 1 in TSP) and replaces the reference node number with the original node number from the reference_to_original_mapping dictionary
def map_tours(tours, reference_to_original_mapping):
  for i, tour in enumerate(tours):
    tours[i] = [reference_to_original_mapping.get(node) for node in tour]
  return tours

# This function reads the the solution file and extracts the tour from it and adds the dock node to the end of the tour. There is no list of tours since it's a TSP instnace
def parse_solution_file():
    tours = []
    tour = []
    with open(SOLUTION_FILE_PATH, 'r') as file:
        lines = file.readlines()
        start_reading = False
        for line in lines:
            if line.strip() == "EOF":
                break
            if start_reading:
                if line.strip() != "-1":
                    tour.append(int(line.strip()))
                else:
                    tour.append(1)
                    tours.append(tour)
                    tour = []
                    start_reading = False
            if line.strip() == "TOUR_SECTION":
                start_reading = True

    return tours

# DOn't worry 
def write_first_tour_to_file(tour, mapping, BO):
    with open(BO, 'w') as file:
        coordinates_str = ', '.join(str(mapping[node]) for node in tour if node in mapping)
        file.write("[" + coordinates_str + "]")

# This function publishes the tours as a list of nodes to the ROS topic tour_0. It has not been updated to publish coordinates.
def publish_tours(tours):

  for i, nodes in enumerate(tours):
    tour_topic = 'tour_' + str(i)
    tour_publisher = rospy.Publisher(tour_topic, Tour, queue_size = 10)
    tour_msg = Tour()
    tour_msg.nodes = nodes
    tour_publisher.publish(tour_msg)
    rospy.sleep(1)

# This function, the same as the node mapping, puts the JSON file content into a dictionary and changes the keys to ints and values into tuples
def coordinate_mapping():
    with open(COORDINATE_FILE_PATH, 'r') as f:
        coord_mapping = json.load(f)
    coord_mapping = {int(k): tuple(v) for k, v in coord_mapping.items()}
    return coord_mapping

# This function, same as map_tours, but for coordinates. It replaces the reference node number with the coordinates of the original node number
def map_tours_to_coordinates(tours, coord_mapping):
    for i, tour in enumerate(tours):
        tours[i] = [coord_mapping.get(node) + (0,) for node in tour]
    return tours

# THis function writes the tours to a file in the format of a list of coordinates. In TSP, only 1 tour file
def write_coordinate_tour_to_file(tour, file_path):
   with open(file_path, 'w') as file:
      for i, coordinate in enumerate(tour):
         if i == len(tour) - 1:
            file.write(str(coordinate) + "\n")
         else:
            file.write(str(coordinate) + ",\n")

def main():
  run_tsp_solver()
  delete_old_tour_file()
  cmapping = coordinate_mapping()
  mapping = node_mapping()

  print_flag = True
  while not rospy.is_shutdown():
    tours = parse_solution_file()
    cmapped_tours = map_tours_to_coordinates(tours, cmapping)
    tours = parse_solution_file()
    mapped_tours = map_tours(tours, mapping)
    publish_tours(mapped_tours)
    
    if print_flag:
      for i, nodes in enumerate(tours):
        print("Tour_" + str(i) + " written to file and topic: Tour_" + str(i) + ": " + "[" +' '.join(map(str, nodes)) + "]")
        file_path = "/home/chloe/Downloads/LKH-3.0.9/Tour_{}.txt".format(i)
        write_coordinate_tour_to_file(cmapped_tours[i], file_path)
      print_flag = False

if __name__ == '__main__':
  rospy.init_node(NODE_NAME, anonymous = True)

  main()