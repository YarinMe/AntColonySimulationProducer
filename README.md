# Ant Colony Solution for TSP

Here is an implementation of the Ant Colony System (ACS) for the Traveling Salesman Problem (TSP).
The program includes a simulation that logs data, and GIFs can be generated to visualize the simulation process.

The code is not intended for production use, but it is functional.
It is based on the paper "Ant Colony System: A Cooperative Learning Approach to the Traveling Salesman Problem" by Marco Dorigo and Luca M. Gambardella (which you can find in this repo).
Note that I have corrected and modified some details based on discrepancies found in the paper.

## How It Works
![](/how_main_works.png)

Running the main function will execute the entire process, including running the simulation and generating the GIF. Alternatively, you can run the simulation separately by executing ants_main.py, which will only log the results to the data folder.
You can modify the simulation parameters by editing the globals.py module.

## Limitations
One noticeable limitation is the lack of functionality for choosing the graph used in the simulation.
Currently, the simulation generates its own graph.

## Gifs Explenation
Note: These GIFs are sped up for demonstration purposes.
If you want the produced GIFs to be faster or slower, you can adjust the speed in each generate_gif.py script located in each animation directory.

The first GIF illustrates the decision-making process of the ants in each iteration.
The bold black lines represent the current best route, while the red lines indicate the edges selected by the ants.
The blinking orange highlights the end of an iteration.
The minimap is used to emphasize more the pheromones on each edge where the width of the edges in the main gif is the score of this edge
![](/fast_first_animation.gif)

The second GIF demonstrates the optimization mechanism employed by the ACS for TSP.
The bold edges represent the current best path, red edges indicate those that were part of the best path in the last two iterations, and the rest are regular edges.
![](/fast_second_animation.gif)
