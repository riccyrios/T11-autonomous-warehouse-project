# T11_multi_warehouse

## Mapping

### Terminal Functions
cd git/T11_multi_warehouse/Y_Mapping/

roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/home/ubuntu/git/T11_multi_warehouse/Y_Mapping/cart3_map.yaml 

rosbag play -l cart3_map.bag

python3 extracting.py

python3 extracting_binary.py

python3 subsamplingV3.py

### Gmapping
Gmapping was the first method used to create a static map. Multimapping was used where two turtlebot3 mapped our environment. The map is saved as "map.pgm and map.yaml"

### Cartographer 
Cartographer was the second method used to create a map that continuously updates the map based on probability. The maps are saved as "cart_map.pgm, cart2_map.pgm, cart3_map.pgm and final_cart.pgm"

In the Python scripts, I used the cart3_map.pgm and cart3_map.yaml files.

### Python3 Scripts
Three python scripts are used to extract the pgm and yaml saved map images. 

extracting.py - This was used to extract all poses of occupied spaces in the map. It detected ~2000 points of the walls and tables of the environment. It saved the poses in a text file, called occupied_coordinates_cart.txt, and saved the plot image, called occupied_coord_plot.png

extracting_binary.py - This was used to extract the map's binary information of occupied spaces. It saved the information in a text and csv file called occupied_binary_cart.csv 

subsamplingV3.py - This was used to extract all poses of the occupied spaces in the map and used kmeans clustering to only plot 200 (x,y) points. It saved the poses in a text file, called subsampled_topic.txt, and saved the plot image, called subsampled_plot.png
