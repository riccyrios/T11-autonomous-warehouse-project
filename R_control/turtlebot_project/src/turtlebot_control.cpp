#include "turtlebot_control.h"
#include "tf/transform_datatypes.h"
#include <cmath>

TurtlebotControl::TurtlebotControl(ros::NodeHandle nh, int ID): 
    nh_(nh), 
    turtlebot_ID_(ID), 
    current_waypoint_index_(0), 
    lin_vel_(0),
    ang_vel_(0),
    linear_tolerance_(0.1),
    angular_tolerance_(25*M_PI/180) //adjust
{

    odom_info_ = nh_.subscribe("/odom", 1, &TurtlebotControl::odoCallback, this);

    cmd_vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/cmd_vel", 1);

    waypointSet_ = std::vector<std::vector<geometry_msgs::Point>>();

    std::string file_path = "/home/riccrios/catkin_ws/src/turtlebot_project/src/paths.txt"; /////CHANGEE THISS

    loadWaypoints_(file_path);

    // potentially add the waypoint publisher, we should subscribe to a ros topic that subscribes to the waypoints being published by path planning node
    //waypoints_sub_ = nh_.subscribe("/waypoints", 1, &TurtlebotControl::setWaypoints, this);

}

void TurtlebotControl::loadWaypoints_(std::string& file_path){

    std::ifstream infile(file_path);

    if (!infile.is_open()) {
        ROS_ERROR("Failed to open paths.txt");
        return;
    }

    std::string line;

    while(std::getline(infile, line)){

        std::istringstream iss(line);
        std::vector<geometry_msgs::Point> waypoints;
        double x, y;
        char bracket1, comma, bracket2;

        while (iss >> bracket1 >> x >> comma >> y >> bracket2) {
            geometry_msgs::Point point;
            point.x = x;
            point.y = y;
            waypoints.push_back(point);
        }

        waypointSet_.push_back(waypoints);
    }
}

void TurtlebotControl::moveTurtlebot(){

    if (waypointSet_.size() == 0){
        ROS_WARN("No waypoints set for turtlebot. Exiting...");
        return;
    }

    ros::Rate wait_rate(1);

    while(ros::ok() && !odom_received_){
        ROS_INFO("Waiting for odometry information...");
        ros::spinOnce();
        wait_rate.sleep();
    }

    double waypointSet_index = 0; // Index of the current waypoint Set

    while (waypointSet_index < waypointSet_.size()){

        std::cout << "waypointSet index: " << waypointSet_index << std::endl;
        std::cout << "waypoint set size: " << waypointSet_.size() << std::endl;

        linear_tolerance_ = 0.5;
        angular_tolerance_ = 30*M_PI/180;


        double waypoints_index = 0; // Index of the current waypoints
        while (waypoints_index < waypointSet_[waypointSet_index].size()){

            std::vector<geometry_msgs::Point> waypoints = waypointSet_[waypointSet_index];

            if (waypoints_index == (waypoints.size()*0.9)){
                ROS_INFO("Reaching close to final goal");
                linear_tolerance_ = 0.1;
                angular_tolerance_ = 10*M_PI/180;
               
            }

            std::cout << "current goal: " << waypoints[waypoints_index].x << " " << waypoints[waypoints_index].y << std::endl;

            double distance_to_point = dist(waypoints[waypoints_index], odo_.pose.pose.position);

            std::cout << "distance to point: " << distance_to_point << std::endl;

            double bot_rotation = rotationAngle(waypoints[waypoints_index], odo_.pose.pose.position);

            while (distance_to_point > linear_tolerance_){
            
                distance_to_point = dist(waypoints[waypoints_index], odo_.pose.pose.position);

                bot_rotation = rotationAngle(waypoints[waypoints_index], odo_.pose.pose.position);

                std::cout << "bot_rotation before loop: " << bot_rotation << std::endl;

                while(std::fabs(bot_rotation) > angular_tolerance_){
                    
                    ROS_INFO("Turtlebot is not facing the target yet...");
                   
                    bot_rotation = rotationAngle(waypoints[waypoints_index], odo_.pose.pose.position);
                    ang_vel_ = 0.3*bot_rotation;

                    sendCommand(0, ang_vel_);
                    ros::spinOnce();
                    rate_.sleep();
                }

                ROS_INFO("Turtlebot is facing the target!");
                lin_vel_ = 0.3;
                ang_vel_ = 0;
            
                ROS_INFO_STREAM("Linear FT Velocity: " << lin_vel_);
                ROS_INFO_STREAM("Angular FT Velocity: " << ang_vel_);

                sendCommand(lin_vel_, ang_vel_);
                
                ros::spinOnce();
                rate_.sleep();

                distance_to_point = dist(waypoints[waypoints_index], odo_.pose.pose.position);

                std::cout << "distance to point: " << distance_to_point << std::endl;            

            }

            //within next waypoint tolerance

            double velocity = getVelocity(odo_);

            // if approaching last waypoint (Goal) in set
            if (waypoints_index == waypoints.size()-1){
                std::cout << "reached final waypoint in set" << std::endl;
                while (velocity > 0.01) {
                    stopTurtlebot();
                    ROS_INFO("STOPPING TURTLEBOT");
                    velocity = getVelocity(odo_);
                    ROS_INFO("linear velocity: %f", velocity);
                    ros::spinOnce();
                    rate_.sleep();
                }

                std::this_thread::sleep_for(std::chrono::seconds(3));
            }

            while (velocity > 0.35) {
                stopTurtlebot();
                ROS_INFO("max velocity reached, slowing turtlebot");
                std::cout << "linear velocity: " << velocity << std::endl; 
                velocity = getVelocity(odo_);
                ros::spinOnce();
                rate_.sleep();
            }

            stopTurtlebot();
            ROS_INFO("Reached waypoint!");
            waypoints_index++;
        }

        //next set of waypoints

        waypointSet_index++;
 
    }
    std::cout << "reached final goal" << std::endl;

}


void TurtlebotControl::sendCommand(double throttle, double steering){

    std::cout << "throttle sent to sendcommand " << throttle << std::endl;
    std::cout << "steering sent to sendcommand " << steering << std::endl;
    // Create a message of type Twist
    geometry_msgs::Twist msg;

    // Set the linear and angular velocities
    msg.linear.x = throttle; // Using throttle
    msg.angular.z = steering; // Using steering

    // Publish the message

    cmd_vel_pub_.publish(msg);

}

void TurtlebotControl::odoCallback(const nav_msgs::Odometry::ConstPtr& msg){

    // Store the odometry information
    odo_ = *msg;

    ROS_INFO("Position: x = %f, y = %f", odo_.pose.pose.position.x, odo_.pose.pose.position.y);

    odom_received_ = true;
}

double TurtlebotControl::rotationAngle(geometry_msgs::Point p1 , geometry_msgs::Point p2){

    
    // Calculate the angle of rotation
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;

    double angle = std::atan2(dy, dx);

    // Get the yaw of the odometry
    double odoYaw = tf::getYaw(odo_.pose.pose.orientation);

    // Calculate the difference in angles
    double angleDiff = angle - odoYaw;

    while (angleDiff > M_PI) {
        angleDiff -= 2*M_PI;
    }

    while (angleDiff < -M_PI){
        angleDiff += 2*M_PI;
    }

    return angleDiff;
}

void TurtlebotControl::stopTurtlebot(){
    geometry_msgs::Twist msg;

    msg.linear.x = 0;
    msg.linear.y = 0;
    msg.angular.z = 0;

    cmd_vel_pub_.publish(msg);
}

double TurtlebotControl::getVelocity(nav_msgs::Odometry odo){

    double velocity_x = odo.twist.twist.linear.x;
    double velocity_y = odo.twist.twist.linear.y;

    double velocity = std::sqrt(std::pow(velocity_x, 2) + std::pow(velocity_y, 2));

    return velocity;
    
}

double TurtlebotControl::dist(geometry_msgs::Point p1, geometry_msgs::Point p2){
    return std::sqrt(std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2));
}