import math
import matplotlib.pyplot as plt
import numpy as np
import utils
import operator
import random 

def rdp(points, epsilon):
    """
    Ramer-Douglas-Peucker algorithm to reduce points in a path.
    :param points: List of (x, y) tuples.
    :param epsilon: Tolerance for simplifying.
    :return: Simplified path.
    """
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
