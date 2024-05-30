import map 
import matplotlib.pyplot as plt
import numpy as np
import utils
import algo
import math

def main():
    clearance = 0.1
    rpm = [8, 8]
    robot_radius = 0.089
    mode = 2

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
    # 0: (0.00, 0.00), # Dock
    # 1: (-2.913, 4.222),
    # 2: (-2.532, 4.162),
    # 3: (-0.890, 4.022),
    # 4: (-0.460, 3.972),
    # 5: (1.081, 3.892),
    # 6: (1.461, 3.852),
    # 7: (1.431, 3.342),
    # 8: (1.051, 3.392),
    # 9: (-0.440, 3.532),
    # 10: (-0.910, 3.572),
    # # 11: (-2.532, 3.722),
    # 11: (-2.547, 3.722),
    # 12: (-2.913, 3.762),
    # 13: (1.251, 1.841),
    # 14: (0.89, 1.821),
    # 15: (-0.66, 1.951),
    # 16: (-1.061, 1.981),
    # 17: (-2.662, 2.161),
    # 18: (-3.093, 2.181),
    # 19: (1.231, 1.29),
    # 20: (0.84, 1.34)
    }

    # mode 0 calculate chosen row
    if mode == 0:
        distances_from_node_0 = []
        for i in range(1, 21):
            start_point = [NODE_COORDINATES[11][0], NODE_COORDINATES[11][1], 0]
            
            goal_point = [NODE_COORDINATES[i][0], NODE_COORDINATES[i][1]]
            print(f"Calculating path from {start_point} to {goal_point}")
            
            if not utils.check_node(start_point, clearance):
                print(f"Start point is invalid for node {i}. Skipping.")
                distances_from_node_0.append(None)
                continue
            if not utils.check_node(goal_point, clearance):
                print(f"Goal point is invalid for node {i}. Skipping.")
                distances_from_node_0.append(None)
                continue

            s1 = None
            s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
            try:
                path, explored = s1.astar()
                if path:
                    distance = calculate_distance(path)
                    distances_from_node_0.append(distance)
                    print(f"Distance from node 0 to node {i}: {distance}")
                else:
                    distances_from_node_0.append(None)
                    print(f"No valid path found for node {i}.")
            except Exception as e:
                print(f"Error while calculating path for node {i}: {e}")
                distances_from_node_0.append(None)

        print("Distances from node 0 to all nodes:")
        print(distances_from_node_0)

    # mode 1 calculate path from node a to node b
    elif mode == 1:
        start_point = [NODE_COORDINATES[11][0], NODE_COORDINATES[11][1], 0]
        goal_point = [NODE_COORDINATES[12][0], NODE_COORDINATES[12][1]]
        s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
        try:
            path, explored = s1.astar()
            # Print the explored nodes and final path
            # print(f"Explored nodes: {explored}")
            # print(f"Path: {path}")
            if path:
                distance = calculate_distance(path)
                print(f"Distance: {distance}")
            else:
                print("No valid path found.")
        except Exception as e:
            print(f"Error while calculating path: {e}")

    # mode 2 calculate distance matrix
    elif mode == 2:
        distance_matrix = np.full((21, 21), None)
        for i in NODE_COORDINATES:
            start_point = [NODE_COORDINATES[i][0], NODE_COORDINATES[i][1], 0]
            for j in range(i, 21):
                goal_point = [NODE_COORDINATES[j][0], NODE_COORDINATES[j][1]]
                s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
                path, explored = s1.astar()
                if path:
                    dis = calculate_distance(path)
                    distance_matrix[i][j] = round(dis, 2)
                    distance_matrix[j][i] = round(dis, 2)
        for row in distance_matrix:
            print(list(row))

        with open("distance_matrix.txt", "w") as file:
            for row in distance_matrix:
                formatted_row = ' '.join(str(elem) if elem is not None else '' for elem in row)
                file.write(formatted_row + '\n')

    # mode 3 generate paths to a list of goal points
    elif mode == 3:
        goal_points = []
        with open('goals.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                points = line.strip().replace('(', '').replace(')', '').split(',')
                goal_points.append((float(points[0]), float(points[1]), 0))
        paths = []
        start_point = (0, 0, 0)

        # Find paths between start_location and the first goal, then between each consecutive goal
        for goal in goal_points:
            goal_point = goal
            s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
            path, explored = s1.astar()
            if path: 
                threshold = 0.3  # Distance threshold
                path = filter_close_points(path, threshold)
                paths.append(path)
            start_point = goal_point

        # Write paths to paths.txt
        with open('paths.txt', 'w') as file:
            for path in paths:
                path_str = ' '.join(f'({x[0]}, {x[1]})' for x in path)
                file.write(path_str + '\n')
        

def calculate_distance(path):
    total_distance = 0
    for i in range(1, len(path)):
        x1, y1 = path[i-1]
        x2, y2 = path[i]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        total_distance += distance
    return round(total_distance, 2)

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def filter_close_points(path, threshold):
  filtered_path = [path[0]]  # Start with the first point

  for point in path[1:]:
      if distance(filtered_path[-1], point) >= threshold:
          filtered_path.append(point)

  return filtered_path

if __name__ == "__main__":
    main()

