#include <ros/ros.h>
#include "turtlebot_control.h"
#include <thread>


int main (int argc, char **argv){



    std::cout<<"Starting the turtlebot project..." << std::endl;

    ros::init(argc, argv, "turtlebot_project");
    ros::NodeHandle nh;

    std::cout << "ros init setup" << std::endl;

    std::shared_ptr<TurtlebotControl> turtlebot1 = std::make_shared<TurtlebotControl>(nh, 0);

    std::cout <<"made shared point turtlebot1" << std::endl;

    std::vector<geometry_msgs::Point> waypoints;

    geometry_msgs::Point point1;
    point1.x = 3.0;
    point1.y = 0.0;
    waypoints.push_back(point1);

    geometry_msgs::Point point2;
    point2.x = 3.0;
    point2.y = 3.0;
    waypoints.push_back(point2);

    std::cout << "waypoints defined" << std::endl;

    turtlebot1.get()->setWaypoints(waypoints);

    std::cout << "waypoints set" << std::endl;

    std::cout << "moving turtlebot" << std::endl;

    std::this_thread::sleep_for(std::chrono::milliseconds(50));

    turtlebot1.get()->moveTurtlebot();
    
    std::cout << "turtlebot path finished" << std::endl;

    ros::spin();
    std::cout << "ros spin" << std::endl;

    ros::shutdown();


    std::cout << "ros shutdown" << std::endl;

    return 0;

}