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

    //////////////////////////////////////////
    // while (ros::ok()) {
    //     if (waypoints_.empty()) {
    //         ROS_WARN("No valid points available. Exiting...");
    //         return;
    //     }

    //     // Calculate direction to the next point
    //     ROS_INFO_STREAM("Current waypoint: " << currentWayPoint_.x << ", " << currentWayPoint_.y);
    //     ROS_INFO_STREAM("Odom position: " << odo_.pose.pose.position.x << ", " << odo_.pose.pose.position.y);

    //     double dx = currentWayPoint_.x- odo_.pose.pose.position.x;
    //     double dy = currentWayPoint_.y - odo_.pose.pose.position.y;
    //     double distance_to_target = sqrt(dx * dx + dy * dy);

    //     // Print the number of points left to reach
    //     int points_left = waypoints_.size() - current_point_index_;
    //     //ROS_INFO_STREAM("Points left to reach: " << points_left);

    //     // Calculate angle to the next point
    //     double angle_to_target = atan2(dy, dx);

    //     double angle_to_target_degrees = angle_to_target * 180 / M_PI;

    //     //Initalise vleocities 
    //     double linear_vel = 0;
    //     double angular_vel = 0;
    //     double bot_angle = tf::getYaw(odo_.pose.pose.orientation);
    //     double calculate_angular_vel = 0.5 * (angle_to_target - bot_angle);

    
    //     angular_vel = calculate_angular_vel;   
    //     // Set maximum linear velocity
    //     double max_linear_vel = 0.3;
    //     // Set minimum linear velocity
    //     double min_linear_vel = 0.1;

    //     // // Set angle tolerance
    //     // double angle_tolerance = 20; //in degress Use angle_to_target_degrees when refering to this 
    //     // double angle_threshold = M_PI / 4; //in degrees Use angle_to_target_degrees when refering to this

    //     //Speed increment
    //     double speedIn = 0.01;

    //     // Calculate angle difference between current orientation and angle to the target
    //     double angle_difference = fabs(angle_to_target - bot_angle);

    //     // Define a threshold angle difference for considering the turtlebot facing the target
    //     double facing_threshold = 20 * M_PI / 180; // 20 degrees in radians

    //     // Check if the angle difference is within the threshold
    //     if (angle_difference < facing_threshold && !points_left <= 2)
    //     {
    //         // Turtlebot is facing the target, so you can perform some action here
    //         ROS_INFO("Turtlebot is facing the target!");
    //         linear_vel = linear_vel + speedIn; //speed up since turtlebot is on track
    //         ROS_INFO_STREAM("Linear FT Velocity: " << linear_vel); //FT Facing Target

    //         angular_vel = 0; // no need for rotatiion, turtlebot is on track

    //         // Ensure linear velocity does not exceed maximum or fall below minimum
    //     if (linear_vel > max_linear_vel) {
    //         linear_vel = max_linear_vel;
    //     }
        
    //     if (linear_vel < min_linear_vel && linear_vel != 0) {
    //         linear_vel = min_linear_vel;
    //     }


    //     }
    //     else
    //     {
    //         // Turtlebot is not facing the target yet
    //         ROS_INFO("Turtlebot is not facing the target yet...");
    //         linear_vel = linear_vel - speedIn; // slow down as turtlebot needs more time to roate
    //         ROS_INFO_STREAM("Linear NFT Velocity: " << linear_vel); //NFT Not Facing Target

    //         angular_vel = calculate_angular_vel; // rotate the turtlebot so its within the cone of tolerance
    //         ROS_INFO_STREAM("Angular NFT Velocity: " << angular_vel);
    //         // Ensure linear velocity does not exceed maximum or fall below minimum
    //     if (linear_vel > max_linear_vel) {
    //         linear_vel = max_linear_vel;
    //     }
        
    //     if (linear_vel < min_linear_vel && linear_vel != 0) {
    //         linear_vel = min_linear_vel;
    //     }

    //     }

    //     // If the current point is the final point or there are 2 points left, reduce linear velocity
    //     if (points_left <= 2) {
    //         linear_vel = linear_vel- speedIn; // Adjust as needed

    //         // Ensure linear velocity does not exceed maximum or fall below minimum
    //     if (linear_vel > max_linear_vel) {
    //         linear_vel = max_linear_vel;
    //     }
        
    //     if (linear_vel < min_linear_vel && linear_vel != 0) {
    //         linear_vel = min_linear_vel;
    //     }

    //     }

    //     // // Ensure linear velocity does not exceed maximum or fall below minimum
    //     // if (linear_vel > max_linear_vel) {
    //     //     linear_vel = max_linear_vel;
    //     // }
        
    //     // if (linear_vel < min_linear_vel && linear_vel != 0) {
    //     //     linear_vel = min_linear_vel;
    //     // }

    //     if (distance_to_target < 0.1) {
    //         // Reached the target point
    //         ROS_INFO_STREAM("Reached point " << current_point_index_+1);

    //         // Move to the next point
    //         current_point_index_++;
    //         if (current_point_index_ >= waypoints_.size()){
    //             // Reached the final point, stop the Turtlebot
    //             linear_vel = 0;
    //             angular_vel = 0;
    //             stopTurtlebot();
    //             return;
    //         }

    //         currentWayPoint_ = waypoints_[current_point_index_];
    //     }

    //     // Publish the velocity commands
    //     geometry_msgs::Twist vel_cmd;
    //     vel_cmd.linear.x = linear_vel;
    //     vel_cmd.angular.z = angular_vel;

    //     //ROS_INFO_STREAM("Linear Velocity: " << linear_vel);
    //     //ROS_INFO_STREAM("Angle to Target Degrees: " << angle_to_target_degrees);

    //     cmd_vel_pub_.publish(vel_cmd);

    //     ros::spinOnce();
    //     rate_.sleep();
    // }

// ///////////////////////////////////////////////


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
        
        while (velocity > 0.11) {
            stopTurtlebot();
            ROS_INFO("STOPPING TURTLEBOT");
            std::cout << "linear velocity: " << velocity << std::endl; 
            velocity = getVelocity(odo_);
        }

        stopTurtlebot();
        ROS_INFO("Reached waypoint!!!!!!!!!!!!!!!!!!!!!!!");
        waypoint_index++;

        

        // PID controller for steering

        // if (odo_.twist.twist.linear.x > 0.5 || odo_.twist.twist.linear.x < 0.1){
        //     lin_vel = 0.3;
        // }

        // if (std::abs(bot_rotation) < 0.1){
        //     ang_vel = 0;

        //     lin_vel = 0.3;
        //     ROS_INFO("Turtlebot is facing the target");
        // }

        

        // // Change the linear velocity halfway through the waypoints
        // // if (waypoint_index > waypoints_.size()/2){
        // //     lin_vel = 0.1; 
        // // }

        // if (distance_to_point < 0.5){

        //     ROS_INFO_STREAM("Reached waypoint: " << waypoint_index);

        //     sendCommand(0, 0);

        //     waypoint_index++;
            
        //     // if (waypoint_index >= waypoints_.size()){
        //     //     ROS_INFO("Reached goal");
        //     //     sendCommand(0, 0);
        //     //     return;
        //     // }

        // }

        // std::cout <<"command about to be sent" << std::endl;
        // ROS_INFO_STREAM("Linear NFT Velocity: " << lin_vel); 
        // ROS_INFO_STREAM("Angular NFT Velocity: " << ang_vel);
        // ROS_INFO_STREAM("Distance to point: " << distance_to_point);
        // ROS_INFO_STREAM("Odom position: " << odo_.pose.pose.position.x << ", " << odo_.pose.pose.position.y);


        // sendCommand(lin_vel, ang_vel);

        // ros::spinOnce();
        // rate_.sleep();
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