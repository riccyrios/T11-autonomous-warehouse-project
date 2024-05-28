# CHLOE'S TSP/MTSP shenanigans

Download LKH SOLVER @ `webhotel4.ruk.dk/~keld/research/LKH-3/` into your Downloads folder (you can change the destination, but you will have to change the file paths at the top of the code)

Execute following commands:
```
tar xvfz LKH-3.0.9.tgz
cd LKH-3.0.9
make
```

An executable file called LKH will now be available in the directory LKLH-3.0.9.

My files include different versions:
- TSP instance:
	-calculates cost by reading B's full distance matrix file
	-publishes node reference numbers to tour_0 topic
	-TSP1py, TSP2.py, TSPMain.py
- mTSP instance:
	-calculates cost by reading B's full distance matrix file
	-publishes node reference numbers to tour_(i) topics
- mTSP instance:
	-*** You'll have to manually change the file paths in the first two code files
	-calculates costs by the Manhattan Distance between node coordinates
	-published node reference numbers to tour_(i) topics	
	-task1.py, task2.py, mainTask.py???

## Before you can run my code:
Save the "idk" package to your catkin_ws.

At the top of each file, there will be filepaths declared. You will need to change the user to your own $USER name.
If you downloaded the LKH solver to a different directory, you will need to change that here as well.

#How to run any version:
In one terminal:
`roscore`
In another:
`cd catkin_ws`
`rosrun idk "insert main file name here.py"`
`e.g. rosrun idk mainTask.py`

It will ask you for the pick list length, and if mTSP, the number of salesmen
The solver should run and print out the tour/s
To view the topics, in another terminal run
`rostopic list`
To view the published messages
`rostopic echo /tour_(i)`
`e.g. rostopic echo /tour_0`

Does anyone need me to publish thangssss?
e.g. Publish coordinate list to tour_coord_(i) topics ???

