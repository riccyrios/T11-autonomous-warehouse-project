import map 
import matplotlib.pyplot as plt
import numpy as np
import utils
import algo

def main():
    clearance = 0.1
    rpm = [6, 4]
    robot_radius = 0.089
    mode = 2

    NODE_COORDINATES = {
    0: (0.00, 0.00), # Dock
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
    # 11: (-2.532, 3.722),
    11: (-2.547, 3.722),
    12: (-2.913, 3.762),
    13: (1.251, 1.841),
    14: (0.89, 1.821),
    15: (-0.66, 1.951),
    16: (-1.061, 1.981),
    17: (-2.662, 2.161),
    18: (-3.093, 2.181),
    19: (1.231, 1.29),
    20: (0.84, 1.34)
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
        distance_matrix = np.full((21, 21), "N/A")
        for i in NODE_COORDINATES:
            start_point = [NODE_COORDINATES[i][0], NODE_COORDINATES[i][1], 0]
            for j in range(i+1, 21):
                goal_point = [NODE_COORDINATES[j][0], NODE_COORDINATES[j][1]]
                s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
                path, explored = s1.astar()
                if path:
                    dis = calculate_distance(path)
                    distance_matrix[i][j] = round(dis, 2)
        for row in distance_matrix:
            print(list(row))


def calculate_distance(path):
    total_distance = 0
    for i in range(1, len(path)):
        x1, y1 = path[i-1]
        x2, y2 = path[i]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        total_distance += distance
    return round(total_distance, 2)

if __name__ == "__main__":
    main()

