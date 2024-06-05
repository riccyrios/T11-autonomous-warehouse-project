#include "turtlebot_control.h"
#include "tf/transform_datatypes.h"
#include <cmath>

TurtlebotControl::TurtlebotControl(ros::NodeHandle nh, int ID): nh_(nh), turtlebot_ID_(ID){

    std::cout << "TurtlebotControl constructor" << std::endl;

    // Initialize the subscriber and publisher
    //odom_info_ = nh_.subscribe("/odom", 1, &TurtlebotControl::odoCallback, this);
    odom_info_ = nh_.subscribe("/odom", 1, &TurtlebotControl::odoCallback, this);
    //cmd_vel_pub = nh_.advertise<geometry_msgs::Twist>("/tb"+std::to_string(turtlebot_ID_)+"/cmd_vel", 1);
    cmd_vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/cmd_vel", 1);

    // potentially add the waypoint publisher, we should subscribe to a ros topic that subscribes to the waypoints being published by path planning node
    //waypoints_sub_ = nh_.subscribe("/waypoints", 1, &TurtlebotControl::setWaypoints, this);

    linear_tolerance_ = 0.1;
    angular_tolerance_ = 5*M_PI/180; //might need to make this tolerance smaller too wide right now i think
}

//void TurtlebotControl::setWaypoints(const std::vector<geometry_msgs::Point>::ConstPtr& waypoints){
    //waypoints_ = *waypoints;
void TurtlebotControl::setWaypoints(std::vector<geometry_msgs::Point> waypoints){

    std::cout << "setwaypoints function started for turtlebot" << std::endl;

    // this is where i'll accept the points from Bo, subscribe to the topic that publishes the waypoints

    // Set the waypoints
    waypoints_ = waypoints;

    // Set the current waypoint to the first waypoint
    current_point_index_ = 0;
    currentWayPoint_ = waypoints_[current_point_index_];



    // Set the current goal to the last waypoint
    currentGoal_ = waypoints_[waypoints_.size()-1];

}

void TurtlebotControl::moveTurtlebot(){


    if (waypoints_.size() == 0){
        ROS_WARN("No waypoints set for turtlebot. Exiting...");
        return;
    }

    ros::Rate wait_rate(1);
    while(ros::ok() && !odom_received_){
        ROS_INFO("Waiting for odometry information...");
        ros::spinOnce();
        wait_rate.sleep();
    }

    double lin_vel = 0; // Linear velocity
    double ang_vel = 0; // Angular velocity

    double waypoint_index = 0; // Index of the current waypoint

    std::cout << "initial odometry: " << odo_.pose.pose.position.x << " " << odo_.pose.pose.position.y << std::endl;

    while (waypoint_index < waypoints_.size()){

        std::cout << "waypoint index: " << waypoint_index << std::endl;
        std::cout << "waypoint size: " << waypoints_.size() << std::endl;

        double dx = waypoints_[waypoint_index].x - odo_.pose.pose.position.x;
        double dy = waypoints_[waypoint_index].y - odo_.pose.pose.position.y;

        double distance_to_point = std::hypot(dx, dy);

        std::cout << "distance to point: " << distance_to_point << std::endl;

        std::cout << "about to get angle of rotation" << std::endl;
        double bot_rotation = rotationAngle(dx, dy);

        ang_vel = ang_vel*bot_rotation;

        std::cout << "ang_vel" << ang_vel << std::endl;

        while (distance_to_point > linear_tolerance_){
            double dx = waypoints_[waypoint_index].x - odo_.pose.pose.position.x;
            double dy = waypoints_[waypoint_index].y - odo_.pose.pose.position.y;

            distance_to_point = std::hypot(dx, dy);

            double bot_rotation = rotationAngle(dx, dy);
            std::cout << "bot_rotation before loop: " << bot_rotation << std::endl;

            while(std::fabs(bot_rotation) > angular_tolerance_){
                
                ROS_INFO("Turtlebot is not facing the target yet...");
                ROS_INFO_STREAM("Linear NFT Velocity: " << lin_vel);
                ROS_INFO_STREAM("Angular NFT Velocity: " << ang_vel);
                double dx = waypoints_[waypoint_index].x - odo_.pose.pose.position.x;
                double dy = waypoints_[waypoint_index].y - odo_.pose.pose.position.y;
                bot_rotation = rotationAngle(dx, dy);
                ang_vel = 0.4*bot_rotation;
                std::cout << "bot_rotation in rotating loop: " << bot_rotation << std::endl;
                sendCommand(0, ang_vel);
                ros::spinOnce();
                rate_.sleep();
                std::cout << "bot_rotation in rotating loop after spinOnce: " << bot_rotation << std::endl;
                std::cout << "angular tolerance: " << angular_tolerance_ << std::endl;
                std::cout << "distance to point: " << distance_to_point << std::endl;

            }
            std::cout << "distance to point: " << distance_to_point << std::endl;

            ROS_INFO("Turtlebot is facing the target!");
            lin_vel = 0.3;
            ang_vel = 0;
        
            ROS_INFO_STREAM("Linear FT Velocity: " << lin_vel);
            ROS_INFO_STREAM("Angular FT Velocity: " << ang_vel);

            sendCommand(lin_vel, ang_vel);
            
            ros::spinOnce();
            rate_.sleep();

            distance_to_point = std::hypot(dx, dy);

            std::cout << "distance to point: " << distance_to_point << std::endl;
            std::cout << "linear tolerance: " << linear_tolerance_ << std::endl;

        

        }

        double velocity = getVelocity(odo_);
        
        while (velocity > 1) {
            stopTurtlebot();
            ROS_INFO("STOPPING TURTLEBOT");
            std::cout << "linear velocity: " << velocity << std::endl; 
            velocity = getVelocity(odo_);
        }

        stopTurtlebot();
        ROS_INFO("Reached waypoint!!!!!!!!!!!!!!!!!!!!!!!");
        waypoint_index++;

        
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

    std::cout << "odo:" << odo_.pose.pose.position.x << " " << odo_.pose.pose.position.y << std::endl;
    odom_received_ = true;
}

double TurtlebotControl::rotationAngle(double x, double y){

    double odoYaw;
    
    // Calculate the angle of rotation
    double angle = std::atan2(y, x);

    // Get the yaw of the odometry
    odoYaw = tf::getYaw(odo_.pose.pose.orientation);

    std::cout << "odoYaw: " << odoYaw << std::endl;

    // Calculate the difference in angles
    double angleDiff = angle - odoYaw;

    std::cout << "angleDiff: " << angleDiff << std::endl;

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
