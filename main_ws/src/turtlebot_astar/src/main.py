
import map 
import matplotlib.pyplot as plt
import numpy as np
import utils
import algo

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
    19: (1.036, 1.896),
    20: (1.032, 1.316)
  }

def main():
  # Taking inputs from the user
  # clearance = eval(input('Please enter the clearance value of the robot from the obstacle:'))
  # print('The clearance value you entered is:', clearance)
  # print('')
  clearance = 0.1
  print('The default clearance value is:', clearance)
  start_point = eval(input('Please enter the start coordinates for the robot in this format - [x, y]:'))
  start_point = tuple(start_point) + (0,)
  # start_point = [NODE_COORDINATES[1][0], NODE_COORDINATES[1][1], 0]
  # goal_point = [0, 0, 0]
  while not utils.check_node(start_point, clearance):
    start_point = eval(input('Please enter the start coordinates in this format - [x, y, theta]:'))
  start_circle = plt.scatter(start_point[0], start_point[1], c = 'b')
  print('The start point you entered is:', start_point)
  print('')  
  goal_point = eval(input('Please enter the goal coordinates of the robot in this format - [x, y]:'))
  while not utils.check_node(goal_point, clearance):
    goal_point = eval(input('Please enter the goal coordinates of the robot in this format - [x, y]:'))
  goal_circle = plt.scatter(goal_point[0], goal_point[1], c = 'y')
  print('The goal point you entered is:', goal_point)
  print('')
  goal_circle = plt.Circle((goal_point[0], goal_point[1]), radius= 0.25,fill=False)
  plt.gca().add_patch(goal_circle)
  # # rpm = eval(input('Please enter the RPM for both the wheels in this format - [RPM1,RPM2]:'))
  # print("The wheel RPM's you entered for both the wheels are:", rpm)
  rpm = [6, 4]
  # print('')

  robot_radius = 0.1
  s1 = algo.Node(start_point, goal_point, [0,0], robot_radius+clearance, rpm[0], rpm[1])
  path, explored = s1.astar()
  
  plt.title('Path planning implemented for Turtlebot 3 using A* Algorithm',fontsize=10)
  
  
  # Plotting the explored nodes and final path
  points1x = []
  points1y = []
  points2x = []
  points2y = []
  points3x = []
  points3y = []
  points4x = []
  points4y = []
  
  for point in range(1,len(explored)):
    #print('Explored point:', explored[point])
    points1x.append(explored[point][4][0])
    points1y.append(explored[point][4][1])
    points2x.append(explored[point][1][0]-(explored[point][4][0]))
    points2y.append(explored[point][1][1]-(explored[point][4][1]))
    #plt.quiver(explored[point][4][0], explored[point][4][1], explored[point][1][0]-(explored[point][4][0]), explored[point][1][1]-(explored[point][4][1]), units='xy' ,scale=1, label = 'Final Path', color = 'g', width =0.02, headwidth = 1,headlength=0)
    #if point%10 == 0:
      #plt.savefig('/home/nalindas9/Desktop/images/'+'img' + str(point) + '.png', dpi = 300)
   
  if path != None:
    for point in range(len(path)):
      if point+1 < len(path):
        points3x.append(path[point][0])
        points3y.append((path[point][1]))
        points4x.append((path[point+1][0])-(path[point][0]))
        points4y.append((path[point+1][1])-(path[point][1]))
        #plt.quiver(path[point][0], (path[point][1]), (path[point+1][0])-(path[point][0]), (path[point+1][1])-(path[point][1]), units='xy' ,scale=1, label = 'Final Path', width =0.07, headwidth = 1,headlength=0)
        #plt.savefig('/home/nalindas9/Desktop/images/'+'img' + str(point+len(explored)) + '.png', dpi = 300)
      else:
        points3x.append(path[point][0])
        points3y.append((path[point][1]))
        points4x.append((path[-1][0])-(path[point][0]))
        points4y.append((path[-1][1])-(path[point][1]))
        #plt.quiver(path[point][0], (path[point][1]), (path[-1][0])-(path[point][0]), (path[-1][1])-(path[point][1]), units='xy' ,scale=1, label = 'Final Path', width =0.07, headwidth = 1,headlength=0)
        #plt.savefig('/home/nalindas9/Desktop/images/'+'img' + str(point+len(explored)) + '.png', dpi = 300)
    
  plt.quiver(np.array(points1x), np.array(points1y), np.array(points2x), np.array(points2y), units='xy' ,scale=1, label = 'Final Path', color = 'g', width =0.02, headwidth = 1,headlength=0)
     
  plt.quiver(np.array(points3x), np.array(points3y), np.array(points4x), np.array(points4y), units='xy' ,scale=1, label = 'Final Path', width =0.07, headwidth = 1,headlength=0)
  
  plt.show()
  plt.close()
  # Initialize a matrix to store the paths
  # Initialize a 20x20 matrix with None
  # distance_matrix = np.full((21, 21), 0.0)

  # # Calculate distances and fill the upper triangle of the matrix
  # explored = None
  # for i in range(len(NODE_COORDINATES)):
  #   start_point = [NODE_COORDINATES[i][1], NODE_COORDINATES[i][2], 0]
  #   for j in range(i+1, 20):
  #       goal_point = [NODE_COORDINATES[j][1], NODE_COORDINATES[j][2]]
  #       s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
  #       path, explored = s1.astar()
  #       if path:
  #           total_distance = sum(((path[k][0] - path[k-1][0]) ** 2 + (path[k][1] - path[k-1][1]) ** 2) ** 0.5 for k in range(1, len(path)))
  #           distance_matrix[i][j] = round(total_distance, 2)
  # print('The distance matrix is:')
  # for row in distance_matrix:
  #     print(row)
    

  # # Print the distance matrix
  # for row in distance_mat
  
  

  # clearance = 0.1
  # rpm = [6, 4]
  # robot_radius = 0.089

  # def calculate_distance(path):
  #   total_distance = 0
  #   for i in range(1, len(path)):
  #       x1, y1 = path[i-1]
  #       x2, y2 = path[i]
  #       distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
  #       total_distance += distance
  #   return round(total_distance, 2)


  # distance_matrix = np.full((21, 21), None)
  # for i in NODE_COORDINATES:
  #   start_point = [NODE_COORDINATES[i][0], NODE_COORDINATES[i][1], 0]
  #   for j in range(i+1, 21):
  #     goal_point = [NODE_COORDINATES[j][0], NODE_COORDINATES[j][1]]
  #     s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
  #     path, explored = s1.astar()
  #     if path:
  #       dis = calculate_distance(path)
  #       distance_matrix[i][j] = round(dis, 2)
    
  # def calculate_distance(path):
  #   if path:
  #       return round(sum(((path[k][0] - path[k-1][0]) ** 2 + (path[k][1] - path[k-1][1]) ** 2) ** 0.5 for k in range(1, len(path))), 2)
  #   return None

  # for i in range(21):
  #   start_point = [NODE_COORDINATES[i][0], NODE_COORDINATES[i][1], 0]
  #   for j in range(i+1, 21):
  #       goal_point = [NODE_COORDINATES[j][0], NODE_COORDINATES[j][1]]
  #       s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
  #       path, explored = s1.astar()
  #       distance_matrix[i][j] = calculate_distance(path)

  # for row in distance_matrix:
  #     print(row)
  
if __name__ == '__main__':
  main()
