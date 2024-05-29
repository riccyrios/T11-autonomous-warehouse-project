#!/usr/bin/env python3

import rospy

# Assuming TSP1 and TSP2 are in the same directory as mainmain.py or properly within a package structure
from idk.scripts.TSP1 import main as TSP1_main
from idk.scripts.TSP2 import main as TSP2_main

def main():
    TSP1_main()
    TSP2_main()

if __name__ == '__main__':
    rospy.init_node('NODE_NAME', anonymous=True)
    main()

