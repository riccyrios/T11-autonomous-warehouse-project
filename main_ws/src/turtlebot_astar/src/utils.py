import numpy as np
import math


walls = [
    (-0.33, -0.7),
    (-0.49, 3.45),
    (-0.48, 4.03),
    (-1.89, 3.5),
    (-2.75, 3.61),
    (-2.77, 3.60),
    (-2.77, 3.98),
    (-2.77, 4.12),
    (-1.64, 5.77),
    (-2.76, 3.79),
    (1.58, 1.58),
    (1.74, 3.61),
    (-4.11, 3.64),
    (-4.35, 4.17),
    (-4.53, 4.19),
    (-4.68, 4.18),
    (-4.78, 3.67),
    (-4.78, 3.50),
    (-4.6, 3.50),
    (-4.5, 3.50),
    (-4.33, 3.50),
    (-4.23, 3.49),
    (3.55, 3.9),
    (-4.78, 1.74),
    (-0.47, 3.69),
    (2.96, 0.66),
    (-0.46, 1.86),
    (-4.11, 3.5),
    (-5.08, 5.73),
    (-2.04, 2.16),
    (1.67, -0.49),
    (-3.35, 5.95),
    (2.85, 5.37),
    (-2.22, 4.15),
    (3.17, 2.1),
    (-5.34, 4.87),
    (-5.34, 3.43),
    (-0.41, 0.2),
    (-3.43, 1.62),
    (1.4, 5.57),
    (3.71, 5.03),
    (-1.37, 1.55),
    (-2.58, 5.74),
    (1.6, 1.87),
    (1.01, -0.75),
    (1.73, 3.34),
    (-0.42, 5.68),
    (-5.34, 5.7),
    (-3.99, 2.33),
    (2.2, -0.0),
    (2.99, 1.62),
    (-0.32, 1.12),
    (0.45, 3.85),
    (-2.79, 1.7),
    (2.03, 5.46),
    (3.38, 2.96),
    (0.37, -0.68),
    (0.78, 5.61),
    (-1.86, 3.73),
    (-5.34, 2.0),
    (-0.38, -0.3),
    (0.43, 1.98),
    (-0.9, 1.54),
    (2.94, 1.13),
    (-4.10, 1.71),
    (-3.82, 5.89),
    (-2.74, 2.22),
    (-1.0, 5.72),
    (-0.49, 0.77),
    (-2.17, 5.81),
    (-5.34, 4.26),
    (-5.34, 2.72),
    (-0.45, 0.59),
    (3.32, 5.31),
    (-4.12, 3.85),
    (1.12, -0.56),
    (3.66, 4.5),
    (0.42, 1.43),
    (-1.87, 1.60),
    (2.49, 0.24),
    (-0.47, 1.44),
    (-0.1, 4.03),
    (1.56, 1.33),
    (-2.31, 3.5),
    (-5.34, 5.22),
    (3.37, 2.59),
    (3.48, 3.37),
    (1.19, -0.38),
    (-1.84, 4.15),
    (1.76, 3.89),
    (-5.34, 2.97),
    (1.99, -0.1),
    (-2.70, 2.06),
    (-2.94, 5.9),
    (-0.03, 5.66),
    (0.5, 3.5),
    (0.52, 3.99),
    (-1.82, 5.71),
    (2.22, 5.43),
    (0.75, -0.68),
    (-5.34, 1.81),
    (0.37, 5.6),
    (-5.34, 3.82),
    (-4.80, 3.85),
    (0.57, -0.65),
    (-0.06, 1.95),
    (0.01, -0.64),
    (0.97, 5.6),
    (1.62, 5.53),
    (-3.22, 1.61),
    (3.65, 5.31),
    (-0.01, 1.41),
    (-4.80, 2.26),
    (2.97, 1.37),
    (-4.25, 5.9),
    (3.1, 1.83),
    (-0.42, 2.04),
    (2.99, 0.85),
    (-4.11, 4.20),
    (-0.47, 3.91),
    (-0.66, 5.77),
    (-1.43, 5.78),
    (-0.36, 0.88),
    (3.33, 2.4),
    (-5.34, 2.5),
    (-1.83, 2.09),
    (-4.10, 2.15),
    (-0.69, 1.44),
    (0.45, 3.59),
    (-5.34, 4.38),
    (-0.54, -0.69),
    (-2.74, 1.92),
    (-3.6, 5.96),
    (-1.16, 1.61),
    (1.72, -0.29),
    (-4.42, 5.72),
    (0.2, 1.93),
    (1.17, 5.6),
    (-1.87, 1.87),
    (-2.09, 3.5),
    (-4.76, 5.79),
    (-0.42, -0.03),
    (3.02, 1.03),
    (3.51, 3.61),
    (2.65, 0.3),
    (2.62, 5.37),
    (1.49, -0.48),
    (3.68, 4.77),
    (-2.47, 2.18),
    (0.23, 3.52),
    (3.6, 4.19),
    (-1.21, 5.77),
    (-4.55, 2.27),
    (2.8, 0.38),
    (-0.06, 3.54),
    (1.22, -0.74),
    (-0.23, 5.67),
    (-5.34, 4.63),
    (-0.28, 1.36),
    (-4.13, 5.87),
    (-4.10, 1.91),
    (-5.34, 3.64),
    (-2.17, 2.18),
    (0.24, 4.01),
    (3.09, 5.36),
    (3.32, 2.77),
    (-1.98, 5.8),
    (-4.11, 4.07),
    (-2.70, 3.5),
    (3.27, 2.23),
    (-0.47, -0.49),
    (-5.34, 3.22),
    (1.04, -0.35),
    (-0.6, 5.62),
    (-0.15, -0.69),
    (-5.05, 1.79),
    (-0.47, 0.4),
    (1.86, -0.3),
    (2.06, -0.2),
    (-3.11, 5.9),
    (-5.34, 2.28),
    (3.42, 3.15),
    (1.33, -0.45),
    (-2.39, 5.87),
    (0.45, 1.65),
    (-3.80, 1.72),
    (-0.3, 0.39),
    (-5.34, 5.47),
    (0.57, 5.61),
    (-0.24, 1.98),
    (-2.44, 4.14),
    (1.84, 5.52),
    (0.16, 5.67),
    (-4.29, 2.30),
    (-3.04, 1.65),
    (-5.34, 4.07),
    (2.35, 0.11),
    (-2.05, 4.2),
    (-1.89, 3.95),
    (-2.90, 1.63),
    (-1.55, 1.6),
    (-2.70, 4.27),
    (-4.80, 4.04),
    (0.17, 1.4),
    (-4.8, 4.15),
    (-2.45, 3.5),
    (2.41, 5.39),
    (-0.81, 5.67),
    (-0.45, 1.58),
    (0.9, -0.67),
    (-0.51, -0.28),
    (-0.16, 1.48),
    (-4.0, 5.89),
    (-2.74, 2.22),
    (-4.80, 2.12),
    (-4.55, 5.88),
    (3.44, 2.79),
    (2.93, 0.5),
    (0.18, -0.66),
    (3.24, 1.99),
    # vent 1
    (0.336, 0.500)
    # vent 2
    # (-3.3, 2.9)
    # vent 3
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
          # print('Sorry the point is in an obstacle space! Try again.')
          return False
  return True
  # return True   
  
