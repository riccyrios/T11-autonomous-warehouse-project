# T11_multi_warehouse

## Task Allocation

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
  - calculates cost using B's full distance matrix file
  - publishes tour node numbers to tour_0 topic
  - publishes tour coordinates as goemetry messages to tour0 topic
  - TSP1.py, TSP2.py, TSPMain.py
- mTSP instance:
  - calculates cost using B's full distance matrix file
  - publishes tour node numbers to tour_{i} topic
  - publishes tour coordinates as goemetry messages to tour{i} topic
  - task1.py (old), 1_mTSP_Integration.py, task2.py, taskMain.py (will use old file)
  - // to use new file "1_mTSP_Integration.py", run files "1_mTSP_Integration.py" and "task2.py" separately, instead of running the "taskMain.py" file. Alternatively, change the "taskMain.py" code to import the new file.

## Before you can run my code:
Save the "idk" package to your catkin_ws.

At the top of each file, there will be filepaths declared. I have used the os module so that, assuming you have downloaded the solver to the Downloads directory, you should be able to run without modifying the filepaths.
If you downloaded the LKH solver to a different directory, you will need to change the filepaths declared at the top of the code.

Make sure to make each script an executable before trying to run.

### How to run any version:
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
