#!/usr/bin/env python

# Task /Tour Allocation Node
# This node is responsible for allocating the Tours to each Turtlebot

import rospy
from idk.msg import Tour

def allocate_tours():
  rospy.init_node('allocation_node', anonymous=True)
  rospy.Subscriber('tours', Tour, tour_callback)
  rospy.spin()

def tour_callback(tour):
  # Allocate the tour to a specific Turtlebot
  allocated_tour = allocate_tour(tour)
  #### BO - DO YOU WANT ME TO PUBLISH THE ALLOCATED TOUR TO ANOTHER TOPIC
  #### tour_publisher.publish(allocated_tour)

def allocate_tour(tour):
#### ALLOCATION LOGIC HERE
#### eg return same tour

if __name__ == '__main__':
  allocate_tours()