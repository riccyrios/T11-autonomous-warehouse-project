import map 
import matplotlib.pyplot as plt
import numpy as np
import utils
import algo

def main():
    clearance = 0.1
    rpm = [6, 4]
    robot_radius = 0.089
    mode = 0

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
    11: (-2.532, 3.722),
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

    if mode == 0:
        distances_from_node_0 = []
        for i in range(1, 21):
            start_point = [NODE_COORDINATES[0][0], NODE_COORDINATES[0][1], 0]
            goal_point = [NODE_COORDINATES[i][0], NODE_COORDINATES[i][1]]
            s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
            path, explored = s1.astar()
            if path:
                distance = calculate_distance(path)
                distances_from_node_0.append(distance)
            else:
                distances_from_node_0.append(None)

        print(distances_from_node_0)

    elif mode == 1:
        start_point = [NODE_COORDINATES[0][0], NODE_COORDINATES[0][1], 0]
        goal_point = [NODE_COORDINATES[2][0], NODE_COORDINATES[2][1]]
        s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
        path, explored = s1.astar()
        # print(path)
        distance = calculate_distance(path)
        print(distance)


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

