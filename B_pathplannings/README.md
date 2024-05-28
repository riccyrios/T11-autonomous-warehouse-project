# path-planning-astar-turtlebot
[![License:MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/nalindas9/path-planning-astar-turtlebot/blob/master/LICENSE)

## About
This is the repository for the project - Path planning implemented for the Turtlebot using A* Algorithm. 

## Turtlebot Path Planning using A*

### System and library requirements.
 - Python3
 - Numpy
 - matplotlib
 - math
 
### How to Run
Navigate to the folder "turtlebot_astar" <br>
Now you need to decide what you wanna do:<br>
a) If you want to test my algorithm from a chosen start and end point use command: `python3 main.py`<br>
b) If you want to pass on a list of goals and get a list of paths use command: `python3 main2.py`<br>
main2.py is set on mode 3 which reads from goals.txt and puts it through the astar algorithm and spits out the paths into paths.txt<br>
If you want to test different list of goals please edit goals.txt<br>


The blue circle is the start point, and the yellow circle is the goal with threshold radius of 0.25 meters. The green color is for the explored nodes, while the black color signifies the final path. 


