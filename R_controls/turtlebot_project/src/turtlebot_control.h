#include <iostream>
#include <cmath>
#include <vector> 

#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/Point.h>
#include <nav_msgs/Odometry.h>


class TurtlebotControl{

    public:

    TurtlebotControl(ros::NodeHandle nh, int ID);

    // Initiates moving the turtlebot to goal.
    void moveTurtlebot();

    void setWaypoints(std::vector<geometry_msgs::Point> waypoints);
    

    void sendCommand(double throttle, double steering);

    private:

    void odoCallback(const nav_msgs::Odometry::ConstPtr& msg);

    double rotationAngle(double x, double y);

    void stopTurtlebot();

    double getVelocity(nav_msgs::Odometry odo);

    ros::NodeHandle nh_; // Node handle for communication with ROS
    int turtlebot_ID_; // ID of the turtlebot

    ros::Subscriber odom_info_; // Subscriber for the odometry information
    ros::Publisher cmd_vel_pub_; // Publisher for the velocity commands
    ros::Rate rate_{10}; // Rate for the loop 10 Hz

    nav_msgs::Odometry odo_; // Odometry information

    std::vector<geometry_msgs::Point> waypoints_; // Waypoints to reach goal
    geometry_msgs::Point currentWayPoint_; // Current waypoint to reach
    geometry_msgs::Point currentGoal_; // Goal to reach 
    unsigned int current_point_index_;
    double linear_tolerance_;
    double angular_tolerance_;
    bool odom_received_;




};