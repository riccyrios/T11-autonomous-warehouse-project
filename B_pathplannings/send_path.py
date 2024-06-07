
from turtlebot_astar import map 
import matplotlib.pyplot as plt
import numpy as np
from turtlebot_astar import utils
from turtlebot_astar import algo
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import Float32

def main():
    rospy.init_node('path_publisher', anonymous=True)
    path_pub = rospy.Publisher('/path', Point, queue_size=10)
    distance_pub = rospy.Publisher('/path_distance', Float32, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    NODE_COORDINATES = [
    (0, 0.00, 0.00), # Dock
    (1, -2.913, 4.222),
    (2, -2.532, 4.162),
    (3, -0.890, 4.022),
    (4, -0.460, 3.972),
    (5, 1.081, 3.892),
    (6, 1.461, 3.852),
    (7, 1.431, 3.342),
    (8, 1.051, 3.392),
    (9, -0.440, 3.532),
    (10, -0.910, 3.572),
    (11, -2.532, 3.722),
    (12, -2.913, 3.762),
    (13, 1.251, 1.841),
    (14, 0.89, 1.821),
    (15, -0.66, 1.951),
    (16, -1.061, 1.981),
    (17, -2.662, 2.161),
    (18, -3.093, 2.181),
    (19, 1.231, 1.29),
    (20, 0.84, 1.34)
    ]

    clearance = 0.1
    start_point = [1, 1, 0]  # Set the start point
    goal_point = [-3, 5]     # Set the goal point
    rpm = [6, 4]             # Set the RPM

    robot_radius = 0.089
    s1 = algo.Node(start_point, goal_point, [0, 0], robot_radius + clearance, rpm[0], rpm[1])
    path, explored = s1.astar()

    if path is not None:
        while not rospy.is_shutdown():
            for point in path:
                path_msg = Point()
                path_msg.x = point[0]
                path_msg.y = point[1]
                path_pub.publish(path_msg)
            rospy.loginfo("Path published successfully!")
            
            total_distance = 0
            for i in range(1, len(path)):
                x1, y1 = path[i-1]
                x2, y2 = path[i]
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                total_distance += round(distance, 2)
            distance_pub.publish(total_distance)
            rospy.loginfo("Total path distance published successfully!")
            rate.sleep()
    else:
        rospy.logerr("No path found!")

    rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass


