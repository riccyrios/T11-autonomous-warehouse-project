
import map 
import matplotlib.pyplot as plt
import numpy as np
import utils
import algo
import math

NODE_COORDINATES = {
    0: (0.00, 0.00), # Dock
    1: (2.525, 1.993),
    2: (2.782, 4.615),
    3: (0.922, 4.843),
    4: (0.399, 4.815),
    5: (-2.513, 5.196),
    6: (-3.338, 5.459),
    7: (-4.011, 5.418),
    8: (-4.035, 4.801),
    9: (-2.771, 4.324),
    10: (-0.738, 3.522),
    11: (1.189, 3.916),
    12: (1.118, 3.321),
    13: (-0.757, 4.034),
    14: (-2.809, 3.681), 
    15: (-4.197, 3.459),
    16: (-4.259, 2.775),
    17: (-2.847, 2.256),
    18: (-0.910, 1.972),
    19: (0.900, 2.035),
    20: (1.032, 1.316)
  }

walls = [
    (-0.33, -0.7),
    (-1.64, 5.77),
    (3.55, 3.9),
    (-4.16, 1.89),
    (0.07, 3.69),
    (2.96, 0.66),
    (-0.15, 1.73),
    (-3.36, 4.27),
    (0.18, 5.53),
    (-2.04, 2.16),
    (1.67, -0.49),
    (-3.35, 5.95),
    (2.85, 5.37),
    (-1.5, 4.15),
    (3.17, 2.1),
    (-4.43, 4.87),
    (-4.57, 3.43),
    (-0.41, 0.2),
    (-3.43, 1.73),
    (1.4, 5.57),
    (3.71, 5.03),
    (-1.37, 1.55),
    (-2.58, 5.74),
    (1.6, 1.87),
    (1.01, -0.75),
    (1.73, 3.34),
    (-0.42, 5.68),
    (-4.28, 5.7),
    (-4.64, 2.72),
    (2.2, -0.0),
    (2.99, 1.62),
    (-0.32, 1.12),
    (0.66, 3.85),
    (-2.79, 1.7),
    (2.03, 5.46),
    (3.38, 2.96),
    (0.37, -0.68),
    (0.78, 5.61),
    (-1.9, 3.73),
    (-4.63, 2.0),
    (-0.38, -0.3),
    (0.43, 1.88),
    (-0.9, 1.54),
    (2.94, 1.13),
    (-3.79, 2.33),
    (-3.82, 5.89),
    (-2.38, 1.63),
    (-1.0, 5.72),
    (-0.49, 0.77),
    (-2.17, 5.81),
    (-4.62, 4.26),
    (3.44, 0.26),
    (-0.45, 0.59),
    (3.32, 5.31),
    (-3.9, 3.9),
    (1.12, -0.56),
    (3.66, 4.5),
    (0.42, 1.43),
    (-1.6, 2.09),
    (2.49, 0.24),
    (-0.47, 1.44),
    (-0.1, 4.03),
    (1.56, 1.33),
    (-1.44, 3.72),
    (-4.39, 5.22),
    (3.37, 2.59),
    (3.48, 3.37),
    (1.19, -0.38),
    (-1.88, 4.15),
    (1.76, 3.89),
    (-4.66, 2.97),
    (1.99, -0.1),
    (3.15, -0.06),
    (-2.94, 5.9),
    (-0.03, 5.66),
    (0.5, 3.5),
    (0.52, 3.99),
    (-1.82, 5.71),
    (2.22, 5.43),
    (0.75, -0.68),
    (-4.5, 1.81),
    (0.37, 5.6),
    (-4.56, 3.82),
    (-3.58, 3.86),
    (0.57, -0.65),
    (-0.06, 1.95),
    (0.01, -0.64),
    (0.97, 5.6),
    (1.62, 5.53),
    (-3.22, 1.71),
    (3.65, 5.31),
    (-0.01, 1.41),
    (-4.04, 2.36),
    (2.97, 1.37),
    (-4.25, 5.9),
    (3.1, 1.83),
    (-0.42, 2.04),
    (2.99, 0.85),
    (-3.74, 4.37),
    (0.06, 3.91),
    (-0.66, 5.77),
    (-1.43, 5.78),
    (-0.36, 0.88),
    (3.33, 2.4),
    (-4.66, 2.5),
    (-1.83, 2.09),
    (-3.52, 2.15),
    (-0.69, 1.44),
    (0.64, 3.59),
    (-4.55, 4.38),
    (-0.54, -0.69),
    (-2.1, 1.92),
    (-3.6, 5.96),
    (-1.16, 1.61),
    (1.72, -0.29),
    (-2.36, 5.72),
    (0.2, 1.93),
    (1.17, 5.6),
    (-1.57, 1.87),
    (-1.65, 3.66),
    (-2.83, 5.79),
    (-0.42, -0.03),
    (3.02, 1.03),
    (3.51, 3.61),
    (2.65, 0.3),
    (2.62, 5.37),
    (1.49, -0.48),
    (3.68, 4.77),
    (-2.57, 1.66),
    (0.23, 3.52),
    (3.6, 4.19),
    (-1.21, 5.77),
    (-4.34, 1.83),
    (2.8, 0.38),
    (-0.06, 3.54),
    (1.22, -0.74),
    (-0.23, 5.67),
    (-4.5, 4.63),
    (-0.28, 1.36),
    (-4.13, 5.87),
    (-3.54, 1.91),
    (-4.56, 3.64),
    (-2.17, 1.66),
    (0.24, 4.01),
    (3.09, 5.36),
    (3.32, 2.77),
    (-1.98, 5.8),
    (-3.4, 3.87),
    (-2.27, 3.75),
    (3.27, 2.23),
    (-0.47, -0.49),
    (-4.63, 3.22),
    (1.04, -0.35),
    (-0.6, 5.62),
    (-0.15, -0.69),
    (-4.65, 1.79),
    (-0.47, 0.4),
    (1.86, -0.3),
    (2.06, -0.2),
    (-3.11, 5.9),
    (-4.67, 2.28),
    (3.42, 3.15),
    (1.33, -0.45),
    (-2.39, 5.87),
    (0.45, 1.65),
    (-3.57, 2.32),
    (-0.3, 0.39),
    (-4.32, 5.47),
    (0.57, 5.61),
    (-0.95, 1.41),
    (-1.36, 4.14),
    (1.84, 5.52),
    (0.16, 5.67),
    (-4.19, 1.73),
    (-3.04, 1.65),
    (-4.55, 4.07),
    (2.35, 0.11),
    (-1.68, 4.2),
    (-1.89, 3.95),
    (-3.01, 1.77),
    (-1.55, 1.6),
    (-2.23, 4.27),
    (-3.4, 4.04),
    (0.17, 1.4),
    (-3.53, 4.35),
    (-1.4, 3.94),
    (2.41, 5.39),
    (-0.81, 5.67),
    (-1.15, 1.48),
    (0.9, -0.67),
    (-0.51, -0.28),
    (-0.16, 1.48),
    (-4.0, 5.89),
    (-2.38, 2.22),
    (-4.1, 2.12),
    (-2.65, 5.88),
    (3.44, 2.79),
    (2.93, 0.5),
    (0.18, -0.66),
    (3.24, 1.99)
]

def main():
  # Taking inputs from the user
  # clearance = eval(input('Please enter the clearance value of the robot from the obstacle:'))
  # print('The clearance value you entered is:', clearance)
  # print('')
  clearance = 0.1
  rpm = [8, 8]
  robot_radius = 0.2
  start_node = 0
  goal_node = 14

  print('The default clearance value is:', clearance)
  start_point = eval(input('Please enter the start coordinates for the robot in this format - [x, y]:'))
  start_point = tuple(start_point) + (0,)
  # start_point = [NODE_COORDINATES[start_node][0], NODE_COORDINATES[start_node][1], 0]
  while not utils.check_node(start_point, clearance):
    start_point = eval(input('Please enter the start coordinates in this format - [x, y, theta]:'))
  # start_circle = plt.scatter(start_point[0], start_point[1], c = 'b')
  print('The start point you entered is:', start_point)
  print('')  
  # goal_point = eval(input('Please enter the goal coordinates of the robot in this format - [x, y]:'))
  goal_point = [NODE_COORDINATES[goal_node][0], NODE_COORDINATES[goal_node][1]]
  while not utils.check_node(goal_point, clearance):
    goal_point = eval(input('Please enter the goal coordinates of the robot in this format - [x, y]:'))
  # goal_circle = plt.scatter(goal_point[0], goal_point[1], c = 'y')
  print('The goal point you entered is:', goal_point)
  print('')
  # goal_circle = plt.Circle((goal_point[0], goal_point[1]), radius= 0.25,fill=False)
  # plt.gca().add_patch(goal_circle)
  # # rpm = eval(input('Please enter the RPM for both the wheels in this format - [RPM1,RPM2]:'))
  # print("The wheel RPM's you entered for both the wheels are:", rpm)
  
  # print('')
  s1 = algo.Node(start_point, goal_point, [0,0], robot_radius+clearance, rpm[0], rpm[1])
  path1, explored1 = s1.astar()
  
  if path1:
    # path1 = rdp(path1, epsilon=0.01)
    threshold = 0.3  # Distance threshold
    path1 = filter_close_points(path1, threshold)
    path1.append(goal_point)
    for p in path1:
      print(p)
    # print(', '.join(str(path1)))
  else:
    print('No path found')
  

  cont = input('Do you want to plan another path? (y/n): ')
  if cont.lower() == 'y':
    for p in path1:
      utils.add_obstacle(p)
      add_obstacle(p)
    print('The default clearance value is:', clearance)
    start_point = eval(input('Enter start coordinates for the 2nd robot - [x, y]:'))
    start_point = tuple(start_point) + (0,)
    while not utils.check_node(start_point, clearance, walls):
      start_point = eval(input('Enter start coordinates for the 2nd robot - [x, y]:'))
      start_point = tuple(start_point) + (0,)
    # start_circle = plt.scatter(start_point[0], start_point[1], c = 'b')
    print('The start point you entered is:', start_point)
    print('')  
    goal_point = eval(input('Enter the goal coordinates for the 2nd robot - [x, y]:'))
    while not utils.check_node(goal_point, clearance, walls):
      goal_point = eval(input('Enter the goal coordinates for the 2nd robot - [x, y]:'))
    # goal_circle = plt.scatter(goal_point[0], goal_point[1], c = 'y')
    print('The goal point you entered is:', goal_point)
    print('')
    # goal_circle = plt.Circle((goal_point[0], goal_point[1]), radius= 0.25,fill=False)
    # plt.gca().add_patch(goal_circle)

    s2 = algo.Node(start_point, goal_point, [0,0], robot_radius+clearance, rpm[0], rpm[1])
    path2, explored2 = s2.astar()
    map.create_map(walls)

    make_a_plot([explored1, explored2], [path1, path2])
  else:
      map.create_map(walls)
      make_a_plot([explored1], [path1])
    

# def make_a_plot(explored, path):
#   plt.title('Path planning implemented for Turtlebot 3 using A* Algorithm',fontsize=10)
  
#   # Plotting the explored nodes and final path
#   points1x = []
#   points1y = []
#   points2x = []
#   points2y = []
#   points3x = []
#   points3y = []
#   points4x = []
#   points4y = []
  
#   for point in range(1,len(explored)):
#     #print('Explored point:', explored[point])
#     points1x.append(explored[point][4][0])
#     points1y.append(explored[point][4][1])
#     points2x.append(explored[point][1][0]-(explored[point][4][0]))
#     points2y.append(explored[point][1][1]-(explored[point][4][1]))
#     #plt.quiver(explored[point][4][0], explored[point][4][1], explored[point][1][0]-(explored[point][4][0]), explored[point][1][1]-(explored[point][4][1]), units='xy' ,scale=1, label = 'Final Path', color = 'g', width =0.02, headwidth = 1,headlength=0)
#     #if point%10 == 0:
#       #plt.savefig('/home/nalindas9/Desktop/images/'+'img' + str(point) + '.png', dpi = 300)
   
#   if path != None:
#     for point in range(len(path)):
#       if point+1 < len(path):
#         points3x.append(path[point][0])
#         points3y.append((path[point][1]))
#         points4x.append((path[point+1][0])-(path[point][0]))
#         points4y.append((path[point+1][1])-(path[point][1]))
#         #plt.quiver(path[point][0], (path[point][1]), (path[point+1][0])-(path[point][0]), (path[point+1][1])-(path[point][1]), units='xy' ,scale=1, label = 'Final Path', width =0.07, headwidth = 1,headlength=0)
#         #plt.savefig('/home/nalindas9/Desktop/images/'+'img' + str(point+len(explored)) + '.png', dpi = 300)
#       else:
#         points3x.append(path[point][0])
#         points3y.append((path[point][1]))
#         points4x.append((path[-1][0])-(path[point][0]))
#         points4y.append((path[-1][1])-(path[point][1]))
#         #plt.quiver(path[point][0], (path[point][1]), (path[-1][0])-(path[point][0]), (path[-1][1])-(path[point][1]), units='xy' ,scale=1, label = 'Final Path', width =0.07, headwidth = 1,headlength=0)
#         #plt.savefig('/home/nalindas9/Desktop/images/'+'img' + str(point+len(explored)) + '.png', dpi = 300)
    
#   plt.quiver(np.array(points1x), np.array(points1y), np.array(points2x), np.array(points2y), units='xy' ,scale=1, label = 'Final Path', color = 'g', width =0.02, headwidth = 1,headlength=0)
     
#   plt.quiver(np.array(points3x), np.array(points3y), np.array(points4x), np.array(points4y), units='xy' ,scale=1, label = 'Final Path', width =0.07, headwidth = 1,headlength=0)
  
#   plt.show()
#   plt.close()

def add_obstacle(point):
  walls.append(point)

def make_a_plot(explored_list, path_list):
    plt.title('Path planning implemented for Turtlebot 3 using A* Algorithm', fontsize=10)
    
    # Plotting the explored nodes and final path for each run
    for explored, path in zip(explored_list, path_list):
        points1x, points1y, points2x, points2y = [], [], [], []
        points3x, points3y, points4x, points4y = [], [], [], []

        for point in range(1, len(explored)):
            points1x.append(explored[point][4][0])
            points1y.append(explored[point][4][1])
            points2x.append(explored[point][1][0] - explored[point][4][0])
            points2y.append(explored[point][1][1] - explored[point][4][1])
        
        if path is not None:
            for point in range(len(path)):
                if point + 1 < len(path):
                    points3x.append(path[point][0])
                    points3y.append(path[point][1])
                    points4x.append(path[point + 1][0] - path[point][0])
                    points4y.append(path[point + 1][1] - path[point][1])
                else:
                    points3x.append(path[point][0])
                    points3y.append(path[point][1])
                    points4x.append(path[-1][0] - path[point][0])
                    points4y.append(path[-1][1] - path[point][1])
        
        # plt.quiver(np.array(points1x), np.array(points1y), np.array(points2x), np.array(points2y),
        #            units='xy', scale=1, color='g', width=0.02, headwidth=1, headlength=0)
        # plt.quiver(np.array(points3x), np.array(points3y), np.array(points4x), np.array(points4y),
        #            units='xy', scale=1, color='b', width=0.07, headwidth=1, headlength=0)
    
    path_list1 = np.array(path_list[0])
    plt.scatter(path_list1[:, 0], path_list1[:, 1], color='orange')

    if len(path_list) > 1:
      path_list2 = np.array(path_list[0+1])
      plt.scatter(path_list2[:, 0], path_list2[:, 1], color='blue')

    plt.show()
    plt.close()
  
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def filter_close_points(path, threshold):
  filtered_path = [path[0]]  # Start with the first point

  for point in path[1:]:
      if distance(filtered_path[-1], point) >= threshold:
          filtered_path.append(point)

  return filtered_path

def rdp(points, epsilon):
    """Ramer-Douglas-Peucker algorithm for path simplification."""
    if len(points) < 3:
        return points

    def point_line_distance(point, start, end):
        if start == end:
            return math.dist(point, start)
        else:
            n = abs((end[1] - start[1]) * point[0] - (end[0] - start[0]) * point[1] + end[0] * start[1] - end[1] * start[0])
            d = math.dist(start, end)
            return n / d

    start = points[0]
    end = points[-1]

    max_dist = 0
    max_index = 0
    for i in range(1, len(points) - 1):
        dist = point_line_distance(points[i], start, end)
        if dist > max_dist:
            max_dist = dist
            max_index = i

    if max_dist > epsilon:
        left = rdp(points[:max_index + 1], epsilon)
        right = rdp(points[max_index:], epsilon)
        return left[:-1] + right
    else:
        return [start, end]



if __name__ == '__main__':
  main()
