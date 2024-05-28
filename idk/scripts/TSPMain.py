#!/usr/bin/env python

import rospy

from TSP1 import main as TSP1_main
from TSP2 import main as TSP2_main

def main():
    TSP1_main()
    TSP2_main()

if __name__ == '__main__':
    rospy.init_node('NODE_NAME', anonymous=True)
    main()