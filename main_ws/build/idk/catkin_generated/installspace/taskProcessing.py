#!/usr/bin/env python3

# TSP Solver Output Processing Node
# This node is responsible for executing the TSP solver with the generated problem instance and processing its output.

#!/usr/bin/env python

import rospy
import subprocess
import re

#from taskGeneration import NODE_COORDINATES
from idk.msg import Tour

#from std_msgs.msg import String

# Define our node (I should be more consistent with how I name things)
NODE_NAME = "taskProcessing"

# Define where the solver executable is
SOLVER_EXECUTABLE_PATH = "/home/chloe/Downloads/LKH-3.0.9/LKH"

## SOLVER_EXECUTABLE_PATH = os.path.join(
##  rospy.get_param("/", ""),
##  "find the LKH solver",
##  "LKH"
##)

# Define where the taskGeneration file is
TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.par"

## INSTANCE_FILE_PATH = os.path.join(
##  rospy.get_param("/", ""),
##  "find the problem_instances",
##  "MTSP parameter file"
##)

# Define where the Solution file is
SOLUTION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_SOLUTION"

def run_tsp_solver():
  # Run the LKH solver with the problem instance parameter file
##  subprocess.run([SOLVER_EXECUTABLE_PATH, TASK_GENERATION_FILE_PATH])
  subprocess.call([SOLVER_EXECUTABLE_PATH, TASK_GENERATION_FILE_PATH])


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
#        tour_info = lines[i + 1].split(" Cost: ")
#        ## Remove the bad characters eg hash
#        nodes_str = re.sub(r'#[\d]*|[^\d\s]', '', tour_info[0])
#        ## Convert the cleaned-up string into a list of integers
#        nodes = [int(node) for node in nodes_str.split()]
#        #cost = int(tour_info[1])
#        tours.append(nodes)

  # Print the tours
  for tour in tours:
    print(tour)


####    for line in lines:
##    for i, line in enumerate(lines):
##      if line.startswith("The tours traveled"):
####        tour_info = line.split(": ")[1].strip().split(" Cost: ")
##        tour_info = lines[i + 1].split(" Cost: ")
##        nodes = [int(node) for node in tour_info[0].split()]
##        cost = int(tour_info[1])
##        tours.append((nodes, cost))

  return tours
"""
def convert_node_numbers_to_coordinates(node_numbers, NODE_COORDINATES):
  coordinates = []
  for node_number in node_numbers:
    if node_number == 1:
      coordinates.append(NODE_COORDINATES[21])
    else:
      coordinates.append(NODE_COORDINATES[node_number])
  return coordinates
"""    

def publish_tours(tours):
  print("I AM TRYING TO INITIALISE Q.Q...")
  rospy.init_node(NODE_NAME, anonymous = True)
  print("ROS NODE INITIALISED ???")
####  tour_publisher = rospy.Publisher('tours', Tour, queue_size = 10)
#  rospy.loginfo("Publishing tours...")

  for i, nodes in enumerate(tours):
    #*** Create a unique topic name for each tour to be published to***#
    tour_topic = 'tour_' + str(i)

    #*** Create a publisher for the current tour topic***!
    tour_publisher = rospy.Publisher(tour_topic, Tour, queue_size = 10)
    
    #*** Call me Limp Bizkit because I'm about to Break Stuff
    ####tour_coordinates = convert_node_numbers_to_coordinates(nodes)

    #*** Create a Tour message***#
    tour_msg = Tour()
    #*** Breaking stuff, uncomment if this limps all over my bizkists
    tour_msg.nodes = nodes

    #*** Rollin' Rollin' Rollin' Rollin' (What?)***#
    ####tour_msg.nodes = tour_coordinates  

    #*** Publish the Tour message***#
    tour_publisher.publish(tour_msg)

    ##### Print for fun?
    print("Tour published on topic", tour_topic, ":", nodes)
    ##### Adjust the sleep time 
    rospy.sleep(1)

    

#  print("PUBLISHING TOURS???...")
#  for nodes in tours:
#    tour_msg = Tour()
#    tour_msg.nodes = nodes
#    #tour_msg.cost = cost
#    tour_publisher.publish(tour_msg)
#    print("TOUR PUBLISHED")
#    # What sleep duration???
#    rospy.sleep(1) 

print("ALLTOURS PUBLISHED WHERE???")

#  rospy.loginifor("All tours published.")

def main():
  rospy.init_node(NODE_NAME, anonymous = True)
  ## Run the TSP solver
  run_tsp_solver()

  while not rospy.is_shutdown():
    ## Extract the Tours from the solution file
    tours = parse_solution_file()

    ## Publish Tours as messages
    publish_tours(tours)

  ## Extract the Tours from the solution file
  ####tours = parse_solution_file()

  ## Publisher Tours as messages
  ####publish_tours(tours)

#  rospy.spin()

if __name__ == '__main__':
  main()