#include "turtlebot_control.h"
#include "tf/transform_datatypes.h"
#include <cmath>

TurtlebotControl::TurtlebotControl(ros::NodeHandle nh, int ID): nh_(nh), turtlebot_ID_(ID){

    std::cout << "TurtlebotControl constructor" << std::endl;

    // Initialize the subscriber and publisher
    odom_info = nh_.subscribe("/odom", 1, &TurtlebotControl::odoCallback, this);
    //cmd_vel_pub = nh_.advertise<geometry_msgs::Twist>("/tb"+std::to_string(turtlebot_ID_)+"/cmd_vel", 1);
    cmd_vel_pub = nh_.advertise<geometry_msgs::Twist>("/cmd_vel", 1);
    // potentially add the waypoint publisher, we should subscribe to a ros topic that subscribes to the waypoints being published by path planning node



}

void TurtlebotControl::setWaypoints(std::vector<geometry_msgs::Point> waypoints){

    std::cout << "setwaypoints function started for turtlebot" << std::endl;
    // Set the waypoints
    waypoints_ = waypoints;

    // Set the current waypoint to the first waypoint
    currentWayPoint = waypoints_[0];

    // Set the current goal to the last waypoint
    currentGoal_ = waypoints_[waypoints_.size()-1];

}

void TurtlebotControl::moveTurtlebot(){

    std::cout << "moveTurtlebot function started for turtlebot" << std::endl;

    if (waypoints_.size() == 0){
        ROS_WARN("No waypoints set for turtlebot. Exiting...");
        return;
    }

    double lin_vel = 0.3; // Linear velocity
    double ang_vel = 0.3; // Angular velocity

    double waypoint_index = 0; // Index of the current waypoint

    std::cout << "initial odometry: " << odo_.pose.pose.position.x << " " << odo_.pose.pose.position.y << std::endl;

    while (waypoint_index < waypoints_.size()){

        std::cout << "waypoint index: " << waypoint_index << std::endl;

        double dx = waypoints_[waypoint_index].x - odo_.pose.pose.position.x;
        double dy = waypoints_[waypoint_index].y - odo_.pose.pose.position.y;

        double distance_to_point = std::hypot(dx, dy);

        std::cout << "distance to point: " << distance_to_point << std::endl;

        std::cout << "about to get angle of rotation" << std::endl;
        double bot_rotation = rotationAngle(dx, dy);

        std::cout << "bot rotation: " << bot_rotation << std::endl;

        ang_vel *= bot_rotation;

        std::cout << "ang_vel" << ang_vel << std::endl;

        

        // PID controller for steering

        if (std::abs(bot_rotation) < 0.5){
            ang_vel = 0;
        }

        // Change the linear velocity halfway through the waypoints
        // if (waypoint_index > waypoints_.size()/2){
        //     lin_vel = 0.1; 
        // }

        if (distance_to_point < 0.5){

            ROS_INFO_STREAM("Reached waypoint: " << waypoint_index + 1);

            waypoint_index++;
            
            if (waypoint_index >= waypoints_.size()){
                ROS_INFO("Reached goal");
                sendCommand(0, 0);
                return;
            }
        }

        std::cout <<"command about to be sent" << std::endl;
        sendCommand(lin_vel, ang_vel);

        ros::spinOnce();
        rate_.sleep();
    }

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

    cmd_vel_pub.publish(msg);

}

void TurtlebotControl::odoCallback(const nav_msgs::Odometry::ConstPtr& msg){

    // Store the odometry information
    odo_ = *msg;

    std::cout << "odo:" << odo_.pose.pose.position.x << " " << odo_.pose.pose.position.y << std::endl;
}

double TurtlebotControl::rotationAngle(double x, double y){

    double odoYaw;
    
    // Calculate the angle of rotation
    double angle = std::atan2(y, x);

    std::cout << "angle: " << angle << std::endl;

    std::cout << "odo angle" << odo_.pose.pose.orientation << std::endl;

    // Get the yaw of the odometry
    odoYaw = tf::getYaw(odo_.pose.pose.orientation);



    std::cout << "odoYaw: " << odoYaw << std::endl;

    // Calculate the difference in angles
    double angleDiff = angle - odoYaw;

    std::cout << "angleDiff: " << angleDiff << std::endl;

    while (angleDiff > M_PI){
        angleDiff -= 2*M_PI;
    }

    while (angleDiff < -M_PI){
        angleDiff += 2*M_PI;
    }

    return angleDiff;
}