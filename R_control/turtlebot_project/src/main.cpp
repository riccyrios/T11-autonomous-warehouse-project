#include <ros/ros.h>
#include "turtlebot_control.h"
#include <thread>
#include <fstream>

int main (int argc, char **argv){

    ros::init(argc, argv, "turtlebot_project");

    ros::NodeHandle nh;

    std::shared_ptr<TurtlebotControl> turtlebot1 = std::make_shared<TurtlebotControl>(nh, 0);

    std::this_thread::sleep_for(std::chrono::milliseconds(50));

    turtlebot1.get()->moveTurtlebot();
     
    std::cout << "turtlebot path finished" << std::endl;

    ros::spin();

    ros::shutdown();

    return 0;

}