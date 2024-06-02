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

from idk.msg import tourNodes
from idk.msg import tourCoordinates
from geometry_msgs.msg import Point


NODE_NAME = "taskProcessing"

#*** File Paths for reading/writing ***#
"""Change the file paths if you've downloaded the LKH solver in a different directory."""

#base_path = os.path.join(os.path.expanduser("~"), "Downloads/LKH-3.0.9")
base_path = os.path.join(os.path.expanduser("~"), "git/T11_multi_warehouse/main_ws/src/idk/LKH-3.0.9")

SOLVER_EXECUTABLE_PATH = os.path.join(base_path, "LKH")
TASK_GENERATION_FILE_PATH = os.path.join(base_path, "TSP_TEST.txt")
PAR_FILE_PATH = os.path.join(base_path, "TSP_TEST.par")
CONVERSION_FILE_PATH = os.path.join(base_path, "TSP_CONVERSION.txt")
COORDINATE_FILE_PATH = os.path.join(base_path, "TSP_COORDINATE.txt")
BO = os.path.join(base_path, "TSP_BO.txt")
SOLUTION_FILE_PATH = os.path.join(base_path, "TSP_TEST_TOUR")

mapping = {}

#*** LKH Solver Execution ***#
def run_tsp_solver():
    subprocess.call([SOLVER_EXECUTABLE_PATH, PAR_FILE_PATH])

#*** Delete any old TSP files, this is not important for the TSP version, but it is for the mTSP version
def delete_old_tour_file():
    file_path = os.path.join(base_path, "Tour_0")

    if os.path.exists(file_path):
        os.remove(file_path)
        print("'{}' has been deleted.".format(file_path))
    #else:
    #    print("No such file: '{}'".format(file_path))
    ###Yara don't worry about this fake error message


#*** Converts JSON Files of the Reference to Original/Coordinates into a Python Dictionary ***#
def node_mapping():
    with open(CONVERSION_FILE_PATH, 'r') as f:
        mapping = json.load(f)
    mapping = {int(k): v for k, v in mapping.items()}
    return mapping
      
def coordinate_mapping():
    with open(COORDINATE_FILE_PATH, 'r') as f:
        coord_mapping = json.load(f)
    coord_mapping = {int(k): tuple(v) for k, v in coord_mapping.items()}
    return coord_mapping

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

#*** Mapping the Solver Node Reference Numbers to the Original Numbers and Coordinates ***#
""" 1. Translate the solver node reference numbers to the original node numbers.
    1.1 Take the list of tours and the reference to original mapping dictionary
    1.2 Iterate over each tour in the list of tours
    1.3 Replace the solver node reference number with the original node number and create a new list
    1.4 Replace the original tour in the list of tours with the new list
"""

def map_tours(tours, reference_to_original_mapping):
  for i, tour in enumerate(tours):
    tours[i] = [reference_to_original_mapping.get(node) for node in tour]
  return tours

def map_tours_to_coordinates(tours, coord_mapping):
    for i, tour in enumerate(tours):
       tours[i] = [coord_mapping.get(node) for node in tour]
    return tours

#*** FOr BOOOOO ***#
def write_first_tour_to_file(tour, mapping, BO):
    with open(BO, 'w') as file:
        coordinates_str = ', '.join(str(mapping[node]) for node in tour if node in mapping)
        file.write("[" + coordinates_str + "]")

#*** Publishing Functions ***#
# The publish_tours function publishes the tours as a list of nodes to the ROS topic tour_0.
# The publish_coordinate_tours function publishes the tour coordinates as Points using the geometry messages package.
def publish_tours(tours):

  for i, nodes in enumerate(tours):
    tour_topic = 'tour_' + str(i)
    tour_publisher = rospy.Publisher(tour_topic, tourNodes, queue_size = 10)
    tour_msg = tourNodes()
    tour_msg.nodes = nodes
    tour_publisher.publish(tour_msg)
    rospy.sleep(1)

def publish_coordinate_tours(tours):
    for i, nodes in enumerate(tours):
        tour_topic = 'tour' + str(i)
        tour_publisher = rospy.Publisher(tour_topic, tourCoordinates, queue_size=10)
        tour_msg = tourCoordinates()

        coordinates = []

        # Convert tuples to Point messages
        for node in nodes:
            point_msg = Point()
            point_msg.x = node[0]
            point_msg.y = node[1]
            coordinates.append(point_msg)

        tour_msg.coordinates = coordinates

        tour_publisher.publish(tour_msg)
        rospy.sleep(1)


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
    publish_coordinate_tours(cmapped_tours)
    
    if print_flag:
      for i, nodes in enumerate(tours):
        print("\n")
        print("Node Tour_" + str(i) + " written to file and topic: Tour_" + str(i) + ": " + "[" +' '.join(map(str, nodes)) + "]")
        print("\n")
        print("Coordinate Tour" + str(i) + " published to topic: Tour" + str(i) + ": " + str(cmapped_tours[i]))
        file_path = os.path.join(base_path, "Tour_{}.txt".format(i))
        write_coordinate_tour_to_file(cmapped_tours[i], file_path)
      print_flag = False

if __name__ == '__main__':
  rospy.init_node(NODE_NAME, anonymous = True)

  main()