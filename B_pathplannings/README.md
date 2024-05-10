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
1. Navigate to the folder "turtlebot_astar" <br>
2. To view the simulation video for the following parameters - Start : (1, 1, 0) Goal : (-3, 5) <br>
3. To run the code, from the terminal, run the command `python3 main.py` <br>
4. The program will ask for the clearance (in meters) from the obstacles, provide input in 'float' format. For eg: 0.2<br>
5. Next program will ask for start point, provide input in [x,y,theta] format. For eg: `1, 1, 0`. If the points provided are in the obstacle space or out of bounds, program will ask you to re-enter points.<br>
6. Next program will ask for goal point, provide input in [x,y] format. For eg: `-3,5`.
If the points provided are in the obstacle space or out of bounds, program will ask you to re-enter points.<br>
7. You will then be asked the two RPM's for the wheels, provide input in [rpm1,rpm2] format, For eg: `6,4` <br>

The blue circle is the start point, and the yellow circle is the goal with threshold radius of 0.25 meters. The green color is for the explored nodes, while the black color signifies the final path. 


