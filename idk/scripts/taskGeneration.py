#!/usr/bin/env python
"""
is this a comment?
nice it is all pink
this is pink comment
"""

# TSP Problem Instance Generation Node
# This node is responsible for generating the TSP problem instance and writing it to a file that the solver can read.

#!/usr/bin/env python

# Let's import the necessaries
import rospy
import random
import math

#from std_msgs.msg import String

# Define our node
NODE_NAME = "taskGeneration"

# Define where the TSP Problem Instance fie should be saved
####TASK_GENERATION_FILE_PATH = "/Home/Downloads/LKH-3.0.9/MTSP_TEST.txt"
TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.txt"
PAR_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.par"
#TASK_CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_CONVERSION.txt"

def calculate_min_cities(num_nodes_to_pick, num_salesmen):
  min_cities_per_salesmen = math.ceil(num_nodes_to_pick / num_salesmen * 0.4)
  return min_cities_per_salesmen

#*** Working with replacement, although I don't think we want replacement ***#
  # Why is my python so old :(((
#def choices_with_replacement(population, k):
#  return [random.choice(population) for _ in range (k)]

def generate_tasks(num_nodes_to_pick):
##def generate_tasks():
  # Define the number of locations/nodes (20 + the dock drop off)
  #NUM_LOCATIONS = 4
  
  # Define the coordinates (TBD)
  #INSERT REAL ARRAY HERE
  NODE_COORDINATES = {
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
    20: (0.84, 1.34),
    21: (0.0, 0.0) # Dock drop off. Starting and ending point
  }

  #specified_coordinates = [
  #  (-2.913, 4.222), (-2.532, 4.162), (-0.890, 4.022), (-0.460, 3.972),
  #  (1.081, 3.892), (1.461, 3.852), (1.431, 3.342), (1.051, 3.392),
  #  (-0.440, 3.532), (-0.910, 3.572), (-2.532, 3.722), (-2.913, 3.762),
  #  (-3.093, 2.181), (-2.662, 2.161), (-1.061, 1.981), (-0.660, 1.951),
  #  (0.890, 1.821), (1.251, 1.841), (1.231, 1.290), (0.840, 1.340)
#]

  ## Randomly select a subset of node coordinates
  #selected_nodes = random.sample(list(NODE_COORDINATES.values()), num_nodes_to_pick)
  #selected_nodes = random.choices(list(NODE_COORDINATES.items()), k = num_nodes_to_pick)
  #** Working
  #**selected_nodes = [random.choice(list(NODE_COORDINATES.values())) for _ in range(num_nodes_to_pick)]
  #### Initialise the list of selected nodes with the first coordinate
  selected_nodes = [(21, NODE_COORDINATES[21])]

  #### Randomly select the remaining coordinates
  remaining_nodes = list(NODE_COORDINATES.values())
  remaining_nodes.remove(NODE_COORDINATES[21]) # Remove Dock
  selected_nodes += [(i + 1, coord) for i, coord in enumerate(random.sample(remaining_nodes, num_nodes_to_pick - 1))]

  #*** Working with replacment, uncomment for replacement ***#
  #selected_nodes += [(i + 1, coord) for i, coord in enumerate(choices_with_replacement(remaining_nodes, num_nodes_to_pick - 1))]
  
  #*** Working
  #selected_nodes = [(i + 1, coord) for i, coord in enumerate(selected_nodes)]

  # Write to the Problem Instance file
  with open(TASK_GENERATION_FILE_PATH, 'w') as file:
    # Write the header information
    file.write("NAME : MTSP_TEST\n") 
    file.write("TYPE : TSP\n")
    file.write("COMMENT : Chloe Judson, Subsystem Test\n")
    ####file.write("SALESMEN : {}\n".format(num_nodes_to_pick))
    ####file.write(f"SALESMEN : {num_nodes_to_pick}\n")
    ####file.write("SALESMEN : 2\n")
    file.write("SALESMEN : {}\n".format(num_salesmen))
    file.write("DIMENSION : {}\n".format(num_nodes_to_pick))
    ####file.write("DIMENSION : {num_nodes_to_pick}\n")
    ###file.write("DIMENSION : 4\n")
    file.write("EDGE_WEIGHT_TYPE : MAN_2D\n")
    file.write("NODE_COORD_TYPE : TWOD_COORDS\n")
    file.write("DISPLAY_DATA_TYPE : COORD_DISPLAY\n")
    file.write("NODE_COORD_SECTION\n")

    #*** I need to get thes coordinates and unscramble them for the tour publishing

    # Write coordinates for each node
    ###for i in range(1, 5):
      ###x, y = NODE_COORDINATES[i]
      ###file.write("{} {} {}\n".format(i, x, y))
      ####file.write(f"{i} {x} {y}\n")

    #*** Working without Dock
    #for node, (x, y) in selected_nodes:
    #  file.write("{} {} {}\n".format(node, x, y))
      ####file.write(f"{node} {x} {y}\n")

    #*** Working with Dock and replacement
    new_node_number = 1
    for _, (x, y) in selected_nodes:
        file.write("{} {} {}\n".format(new_node_number, x, y))
        new_node_number += 1

    # Kind of optional -\_(o-o)_/-
    file.write("EOF\n")
    #file.write("#{}".format(NODE_COORDINATES.items()))

  #Write the list to the onversion file
  with open(TASK_CONVERSION_FILE_PATH, 'w') as file:
    new_node_number = 1
    for _, (x, y) in selected_nodes:
        file.write("{} {} {}\n".format(new_node_number, x, y))
        new_node_number += 1

###def task_generation():
  ###rospy.init_node('taskGeneration', anonymous = True)
  ###generate_tasks()
    
  #*** Write to the parameter file ***#
    min_cities_per_salesmen = num_nodes_to_pick // num_salesmen
    with open(PAR_FILE_PATH, 'w') as file:
      file.write("PROBLEM_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.txt\n")
      file.write("MTSP_MIN_SIZE = {}\n".format(min_cities_per_salesmen))
      #file.write("MTSP_MAX_SIZE = {}\n".format(max_cities_per_salesmen))
      file.write("MTSP_OBJECTIVE = MINSUM\n")
      file.write("MTSP_SOLUTION_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_SOLUTION\n")
      file.write("OUTPUT_TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_OUTPUT_TOUR\n")
      file.write("TOUR_FILE = /home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_TOUR")

      #*** MTSP_MIN_SIZE = < integer >: The minimum number of cities that must be visited by each salesman.
      #*** MTSP_MAX_SIZE = < integer >: The maximum number of cities that can be visited by each salesman.
      #*** MTSP_OBJECTIVE = MINMAX: The objective is to minimize the maximum distance traveled by any salesman.
      #*** MTSP_OBJECTIVE = MINMAX_SIZE: The objective is to minimize the size of the largest route
      #*** MTSP_OBJECTIVE = MINSUM: The objective is to minimize the total distance traveled by all salesmen.     

def task_generation(num_nodes_to_pick):
  rospy.init_node('taskGeneration', anonymous = True)
  min_cities_per_salesmen = calculate_min_cities(num_nodes_to_pick, num_salesmen)
  generate_tasks(num_nodes_to_pick)

###if __name__ == '__main__':
  ###try:
    ###task_generation()
  ###except rospy.ROSInterruptException:
    ###pass

if __name__ == '__main__':
  try:
    num_nodes_to_pick = 20 #### INPUT NUMBER OF NODES TO PICK FROM LIST
    num_salesmen = 3
    task_generation(num_nodes_to_pick)
  except rospy.ROSInterruptException:
    pass
