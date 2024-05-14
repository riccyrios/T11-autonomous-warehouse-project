#!/usr/bin/env python

# TSP Solver Output Processing Node
# This node is responsible for executing the TSP solver with the generated problem instance and processing its output.

#!/usr/bin/env python

import rospy
import subprocess
import re
import json
import os

#from taskGeneration import NODE_COORDINATES
from idk.msg import Tour


# Define our node (I should be more consistent with how I name things)
NODE_NAME = "taskProcessing"

#reference_to_original_mapping = {1: 0, 2: 20, 3: 3, 4: 13, 5: 11, 6: 9}
mapping = {}


SOLVER_EXECUTABLE_PATH = "/home/chloe/Downloads/LKH-3.0.9/LKH"
TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.txt"
PAR_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.par"
SOLUTION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_SOLUTION"
CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_CONVERSION.txt"

def run_tsp_solver():
  # Run the LKH solver with the problem instance parameter file 
  subprocess.call([SOLVER_EXECUTABLE_PATH, PAR_FILE_PATH]) 

def is_file_empty(SOLUTION_FILE_PATH):
  return os.stat(SOLUTION_FILE_PATH).st_size == 0

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

  # Print the tours
  #for tour in tours:
  #  print(tour)

  return tours
 

def publish_tours(tours):
  rospy.init_node(NODE_NAME, anonymous = True)

  for i, nodes in enumerate(tours):
    #*** Create a unique topic name for each tour to be published to***#
    tour_topic = 'tour_' + str(i)

    #*** Create a publisher for the current tour topic***!
    tour_publisher = rospy.Publisher(tour_topic, Tour, queue_size = 10)

    #*** Create a Tour message***#
    tour_msg = Tour()
    #*** Breaking stuff, uncomment if this limps all over my bizkists
    tour_msg.nodes = nodes

    #*** Publish the Tour message***#
    tour_publisher.publish(tour_msg)

    ##### Adjust the sleep time 
    rospy.sleep(1)


def main():
  rospy.init_node(NODE_NAME, anonymous = True)
  ## Run the TSP solver
  run_tsp_solver()

  print_flag = True  # Set the print_flag to True initially

  while not rospy.is_shutdown():
    ## Extract the Tours from the solution file
    tours = parse_solution_file()
    #print(tours)

    mapping = node_mapping()
    #print(mapping)

    mapped_tours = map_tours(tours, mapping)
    #print(mapped_tours)

    ## Publish Tours as messages
    publish_tours(mapped_tours)
    
    if print_flag:
      for i, nodes in enumerate(mapped_tours):
        print("Tour published on topic: tour_" + str(i) + ": " + "[" +' '.join(map(str, nodes)) + "]")
      # Set the print_flag to False after printing the tours once
      print_flag = False


if __name__ == '__main__':
  if not is_file_empty(SOLUTION_FILE_PATH):
    print('File is not empty')
  else:
    print('TSP didn\'t write the best tour to the solution file??? IDK why this is happening')

  main()