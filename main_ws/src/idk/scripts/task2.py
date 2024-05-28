#!/usr/bin/env python

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
TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.txt"
PAR_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.par"
SOLUTION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_SOLUTION"
CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_CONVERSION.txt"
COORDINATE_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_COORDINATES.txt"
BO = "/home/chloe/Downloads/LKH-3.0.9/Bo.txt"

mapping = {}

def run_tsp_solver():
  # Run the LKH solver with the problem instance parameter file 
  subprocess.call([SOLVER_EXECUTABLE_PATH, PAR_FILE_PATH]) 

def is_file_empty(SOLUTION_FILE_PATH):
  return os.stat(SOLUTION_FILE_PATH).st_size == 0

def delete_old_tour_files():
    global directory
    directory = "/home/chloe/Downloads/LKH-3.0.9/"
    global pattern
    pattern = re.compile(r"Tour_(?:[0-9]|1[0-9]|20)\.txt")
    for filename in os.listdir(directory):
      if pattern.match(filename):
         os.remove(os.path.join(directory, filename))
         print("Deleted: " + filename)

def node_mapping():
    with open(CONVERSION_FILE_PATH, 'r') as f:
        mapping = json.load(f)
    # Convert string keys to integers
    mapping = {int(k): v for k, v in mapping.items()}
    return mapping

def map_tours(tours, reference_to_original_mapping):
  for i, tour in enumerate(tours):
    tours[i] = [reference_to_original_mapping.get(node) for node in tour]
  return tours

def parse_solution_file():
  tours = []

  # Open the solution file and parse the tours
  with open(SOLUTION_FILE_PATH, 'r') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
      if line.startswith("The tours traveled"):
        for j in range (i + 1, len(lines)):
          tour_info = lines[j].split(" Cost: ")
          nodes_str = re.sub(r'#[\d]*|[^\d\s]', '', tour_info[0])
          nodes = [int(node) for node in nodes_str.split()]
          tours.append(nodes)

  return tours

def write_first_tour_to_file(tour, mapping, BO):
    with open(BO, 'w') as file:
        coordinates_str = ', '.join(str(mapping[node]) for node in tour if node in mapping)
        file.write("[" + coordinates_str + "]")

def publish_tours(tours):
  #rospy.init_node(NODE_NAME, anonymous = True)

  for i, nodes in enumerate(tours):
    #*** Create a unique topic name for each tour to be published to***#
    tour_topic = 'tour_' + str(i)

    #*** Create a publisher for the current tour topic***!
    tour_publisher = rospy.Publisher(tour_topic, Tour, queue_size = 10)

    #*** Create a Tour message ***#
    tour_msg = Tour()
    #*** Breaking stuff, uncomment if this limps all over my bizkists
    tour_msg.nodes = nodes

    #*** Publish the Tour message ***#
    tour_publisher.publish(tour_msg)

    ##### Adjust the sleep time ***#
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

"""
def write_coordinate_tour_to_file(tour, file_path):
   with open(file_path, 'w') as file:
      coordinates_str = ', '.join(str(coordinate) for coordinate in tour)
      file.write("[" + coordinates_str + "]")
"""

def write_coordinate_tour_to_file(tour, file_path):
   with open(file_path, 'w') as file:
      for i, coordinate in enumerate(tour):
         if i == len(tour) - 1:
            file.write(str(coordinate) + "\n")
         else:
            file.write(str(coordinate) + ",\n")


def main():
  #rospy.init_node(NODE_NAME, anonymous = True)
  run_tsp_solver()
  delete_old_tour_files()
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
      # Set the print_flag to False after printing the tours once
      print_flag = False


if __name__ == '__main__':
  if not is_file_empty(SOLUTION_FILE_PATH):
    print('File is not empty')
  else:
    print('File is empty')

  rospy.init_node(NODE_NAME, anonymous = True)

  main()