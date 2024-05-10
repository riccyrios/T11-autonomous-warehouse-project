"""
Utility Functions

Authors:
Nalin Das (nalindas9@gmail.com)
Graduate Student pursuing Masters in Robotics,
University of Maryland, College Park
"""
import numpy as np
import math

walls = [
    (-0.13, 1.88),
    (-1.45, 4.12),
    (3.38, 2.82),
    (-3.89, 3.9),
    (1.16, -0.69),
    (1.71, 5.53),
    (-3.99, 2.33),
    (-2.12, 5.8),
    (2.9, 0.5),
    (-0.1, 5.66),
    (0.6, 3.57),
    (-2.12, 1.8),
    (-0.42, 0.08),
    (3.21, 5.33),
    (-3.8, 5.91),
    (-0.94, 1.48),
    (2.99, 1.54),
    (-4.58, 4.29),
    (-3.59, 2.27),
    (-1.12, 5.75),
    (0.16, -0.66),
    (3.66, 4.5),
    (2.29, 0.07),
    (-4.63, 3.22),
    (-4.59, 1.88),
    (0.59, 5.61),
    (0.08, 3.96),
    (-0.4, 0.41),
    (-3.03, 5.88),
    (1.6, 1.87),
    (-4.46, 4.77),
    (0.44, 1.53),
    (-3.08, 1.71),
    (-0.47, -0.61),
    (3.5, 3.57),
    (2.08, 5.45),
    (1.71, -0.39),
    (-0.78, 5.69),
    (1.76, 3.89),
    (-1.63, 2.07),
    (-4.3, 5.61),
    (-3.71, 4.36),
    (0.88, -0.69),
    (3.7, 4.97),
    (-2.42, 5.79),
    (2.98, 0.82),
    (-4.64, 2.79),
    (-0.34, 1.04),
    (-1.56, 1.71),
    (-1.89, 4.11),
    (3.25, 2.16),
    (-0.22, 1.44),
    (-4.15, 5.88),
    (0.26, 3.52),
    (1.32, 5.58),
    (-4.56, 3.63),
    (2.97, 1.15),
    (0.24, 5.6),
    (2.83, 5.37),
    (-4.23, 1.83),
    (-1.47, 3.74),
    (0.58, 3.92),
    (-2.7, 1.68),
    (-0.45, 5.67),
    (-0.59, 1.44),
    (1.42, -0.47),
    (0.56, -0.66),
    (-3.44, 5.96),
    (-1.81, 5.74),
    (1.73, 3.34),
    (3.44, 0.26),
    (2.59, 0.28),
    (-2.02, 2.12),
    (-0.45, -0.29),
    (-4.38, 5.25),
    (3.56, 4.0),
    (-3.38, 4.26),
    (-3.47, 1.81),
    (3.43, 3.16),
    (1.56, 1.33),
    (-0.01, 3.6),
    (3.15, -0.06),
    (0.13, 1.41),
    (0.32, 1.9),
    (-2.73, 5.82),
    (2.0, -0.17),
    (-0.2, -0.69),
    (3.13, 1.87),
    (0.95, 5.59),
    (-2.33, 1.62),
    (-1.28, 1.55),
    (-1.91, 3.72),
    (3.63, 5.3),
    (2.44, 5.39),
    (3.34, 2.46),
    (-4.67, 2.4),
    (1.12, -0.4),
    (-0.45, 0.73),
    (-1.47, 5.78),
    (-3.44, 3.92)
]

# Function to check if the given point lies outside the final map or in the obstacle space
def check_node(node, clearance):
  # radius = 0.5
  # Checking if point inside map
  # if node[0] + clearance >= 10.1-offset or node[0] - clearance <= 0.1-offset  or node[1] + clearance >= 10.1-offset  or node[1] - clearance <= 0.1-offset :
  #   print('Sorry the point is out of bounds! Try again.')
  #   return False
  # Checking if point inside circles
  # elif (node[0] - (3.1-offset) ) ** 2 + (node[1] - (2.1-offset)) ** 2 <= (1+clearance) ** 2 :
  #   print('Sorry the point is in the circle 1 obstacle space! Try again')
  #   return False
  # elif (node[0] - (7.1-offset)) ** 2 + (node[1] - (2.1-offset)) ** 2 <= (1+clearance) ** 2 :
  #   print('Sorry the point is in the circle 2 obstacle space! Try again')
  #   return False
  # elif (node[0] - (5.1-offset)) ** 2 + (node[1] - (5.1-offset)) ** 2 <= (1+clearance) ** 2 :
  #   print('Sorry the point is in the circle 3 obstacle space! Try again')
  #   return False
  # elif (node[0] - (7.1-offset)) ** 2 + (node[1] - (8.1-offset)) ** 2 <= (1+clearance) ** 2 :
  #   print('Sorry the point is in the circle 4 obstacle space! Try again')
  #   return False
  # # Checking if point inside squares
  # elif node[0] + clearance >= 0.35-offset  and node[0] - clearance <=1.85-offset  and node[1] + clearance>= 4.35-offset  and node[1] - clearance< 5.85-offset :
  #   print('Sorry the point is in the square 1 obstacle space! Try again')
  #   return False
  # elif node[0] + clearance >= 2.35-offset  and node[0] - clearance <= 3.85-offset  and node[1] + clearance>= 7.35-offset  and node[1] - clearance <= 8.85-offset :
  #   print('Sorry the point is in the square 2 obstacle space! Try again')
  #   return False
  # elif node[0] + clearance >= 8.35-offset  and node[0] - clearance <= 9.85-offset  and node[1] + clearance>= 4.35-offset  and node[1] - clearance <= 5.85-offset :
  #   print('Node is:', node[0] + clearance >= 8.25)
  #   print('Sorry the point is in the square 3 obstacle space! Try again')
    # return False
  # else:

  x = node[0]
  y = node[1]
  # Checking if point inside circles
  for wall in walls:
      # Calculate the distance between the node and the wall
      distance = ((x - wall[0])**2 + (y - wall[1])**2)**0.5
      # If the distance is less than the radius of the wall, the node is inside the wall
      if distance < clearance:
          print('Sorry the point is in an obstacle space! Try again')
          return False
  return True
  # return True   
  
