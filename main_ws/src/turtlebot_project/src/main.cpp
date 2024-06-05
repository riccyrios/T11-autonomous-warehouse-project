#include <ros/ros.h>
#include "turtlebot_control.h"
#include <thread>
#include <fstream>

int main (int argc, char **argv){



    std::cout<<"Starting the turtlebot project..." << std::endl;

    ros::init(argc, argv, "turtlebot_project");
    ros::NodeHandle nh;

    // std::cout << "ros init setup" << std::endl;
    
    ROS_INFO("DOES THIS HAPPEN");

    std::shared_ptr<TurtlebotControl> turtlebot1 = std::make_shared<TurtlebotControl>(nh, 0);
    
    ROS_INFO("DOES THIS HAPPEN AFTER OBJECT CREATED");

    std::cout <<"made shared point turtlebot1" << std::endl;

    std::cout <<"waypoints vector defined" << std::endl;
    std::vector<geometry_msgs::Point> waypoints;

    char comma; 
    char bracket1;
    char bracket2;

    std::cout << "reading file..." << std::endl;

    std::ifstream file("/home/ubuntu/git/T11_multi_warehouse/main_ws/src/turtlebot_astar/src/paths.txt");

    std::cout << "file trying to open " << std::endl;

    if (!file.is_open()) {
        ROS_ERROR("Failed to open paths.txt");
        return 0;
    }

    // Read the points from the file
    double x, y;
    while (file >> bracket1>> x >> comma >> y >> bracket2) {
        geometry_msgs::Point point;
        point.x = x;
        std::cout<< "x: " << x << std::endl;
        point.y = y;
        std::cout << "y: " << y << std::endl;
        
        waypoints.push_back(point);
    }



    // Close the file
    file.close();

    std::cout << "waypoints defined" << std::endl;

    turtlebot1.get()->setWaypoints(waypoints);

    std::this_thread::sleep_for(std::chrono::milliseconds(50));

    turtlebot1.get()->moveTurtlebot();
    
    std::cout << "turtlebot path finished" << std::endl;

    ros::spin();
    // std::cout << "ros spin" << std::endl;

    ros::shutdown();


    // std::cout << "ros shutdown" << std::endl;

    return 0;

}


