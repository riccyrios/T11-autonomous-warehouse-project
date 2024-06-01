import map 
import matplotlib.pyplot as plt
import numpy as np
import utils
import algo

def main():
    clearance = 0.1
    rpm = [6, 4]
    # robot_radius = 0.089
    robot_radius = 0.1
    mode = 2
    epsilon = 0.2

    NODE_COORDINATES = {
    0: (0.00, 0.00), # Dock
    1: (2.2, 3), #works
    2: (2.2, 5.2), #works
    3: (0.4, 5.2), #works
    4: (-0.9, 5.2), #works
    5: (-2.6, 5.2), #works
    6: (-3.8, 5.2), #works
    7: (-3.8, 4.6), #works
    8: (-2.7, 4.5), #works
    9: (-3.4, 4.2), #works
    10: (-1.15, 4.2), #works
    11: (0.9, 4.2), #works
    12: (0.9, 3.4), #works
    13: (-1.15, 3.5), #works
    14: (-3.4, 3.4), #works
    15: (-4, 3.1), #works
    16: (-4, 2.7), #works
    17: (-3.3, 1.9), #works
    18: (-1.25, 1.9), #works
    19: (0.9, 1.9), #works
    20: (0.9, 1.5) #works
    }

    # mode 0 calculate chosen row
    if mode == 0:
        distances_from_node_0 = []
        for i in range(1, 21):
            start_point = [NODE_COORDINATES[5][0], NODE_COORDINATES[5][1], 0]
            
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
        with open('/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/LKH-3.0.9', 'r') as file:
            lines = file.readlines()
            for line in lines:
                points = line.strip().replace('(', '').replace(')', '').split(',')
                goal_points.append((float(points[0]), float(points[1]), 0))

        paths = []
        start_point = (0, 0, 0)

        for goal in goal_points:
            print(f"Processing goal: {goal}")
            goal_point = goal
            s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
            try:
                path, explored = s1.astar()
                if path:
                    print(f"Path found to goal {goal}: {path}")
                    path = rdp(path, epsilon)  # Apply RDP algorithm to smooth the path
                    path.append(goal)
                    paths.append(path)
                    start_point = goal_point  # Update start point to current goal point
                else:
                    print(f"No valid path found to goal {goal}.")
            except Exception as e:
                print(f"Error while calculating path to goal {goal}: {e}")

        # Write paths to paths.txt
        with open('paths.txt', 'w') as file:
            for path in paths:
                path_str = ' '.join(f'({x[0]}, {x[1]})' for x in path)
                file.write(path_str + '\n')
        
def rdp(points, epsilon):

    if len(points) < 3:
        return points

    def point_line_distance(point, start, end):
        if start == end:
            return np.linalg.norm(np.array(point) - np.array(start))
        else:
            return np.abs(np.cross(np.array(end) - np.array(start), np.array(start) - np.array(point)) / np.linalg.norm(np.array(end) - np.array(start)))

    start, end = points[0], points[-1]
    max_dist = 0
    index = 0
    for i in range(1, len(points) - 1):
        dist = point_line_distance(points[i], start, end)
        if dist > max_dist:
            index = i
            max_dist = dist

    if max_dist > epsilon:
        result1 = rdp(points[:index + 1], epsilon)
        result2 = rdp(points[index:], epsilon)
        return result1[:-1] + result2
    else:
        return [start, end]

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

