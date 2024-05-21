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

SOLVER_EXECUTABLE_PATH = "/home/chloe/Downloads/LKH-3.0.9/LKH"
TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST.txt"
PAR_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST.par"
CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_CONVERSION.txt"
COORDINATE_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_COORDINATES.txt"
BO = "/home/chloe/Downloads/LKH-3.0.9/TSP_BO.txt"
SOLUTION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/TSP_TEST_TOUR"

mapping = {}

def run_tsp_solver():
    subprocess.call([SOLVER_EXECUTABLE_PATH, PAR_FILE_PATH])

def delete_old_tour_file():
    directory = "/home/chloe/Downloads/LKH-3.0.9/"
    file_path = os.path.join(directory, "Tour_0")

    if os.path.exists(file_path):
        os.remove(file_path)
        print("'{}' has been deleted.".format(file_path))
    else:
        print("No such file: '{}'".format(file_path))

def node_mapping():
    with open(CONVERSION_FILE_PATH, 'r') as f:
        mapping = json.load(f)
    mapping = {int(k): v for k, v in mapping.items()}
    return mapping

def map_tours(tours, reference_to_original_mapping):
  for i, tour in enumerate(tours):
    tours[i] = [reference_to_original_mapping.get(node) for node in tour]
  return tours

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

def write_first_tour_to_file(tour, mapping, BO):
    with open(BO, 'w') as file:
        coordinates_str = ', '.join(str(mapping[node]) for node in tour if node in mapping)
        file.write("[" + coordinates_str + "]")

def publish_tours(tours):

  for i, nodes in enumerate(tours):
    tour_topic = 'tour_' + str(i)
    tour_publisher = rospy.Publisher(tour_topic, Tour, queue_size = 10)
    tour_msg = Tour()
    tour_msg.nodes = nodes
    tour_publisher.publish(tour_msg)
    rospy.sleep(1)

def coordinate_mapping():
    with open(COORDINATE_FILE_PATH, 'r') as f:
        coord_mapping = json.load(f)
    # Convert string keys to integers
    coord_mapping = {int(k): tuple(v) for k, v in coord_mapping.items()}
    return coord_mapping

def map_tours_to_coordinates(tours, coord_mapping):
    for i, tour in enumerate(tours):
        tours[i] = [coord_mapping.get(node) + (0,) for node in tour]
    return tours

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