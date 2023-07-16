from utils import Utils
from globals import Globals

import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def createSnapshot(adjacencies, pharamons, figureNuber, iterationNumber, almostBestEdges = [] ,bestEdges = []):
    bigGraphmatrix = np.zeros((Globals.graphSize, Globals.graphSize))
        
    for i in range(Globals.graphSize):
        for j in range(Globals.graphSize):
            if adjacencies[i][j] == 0:
                continue
                
            bigGraphmatrix[i][j] = Utils.getScore(pharamons[i][j], adjacencies[i][j])

    fig, ax = plt.subplots()

    # Create a graph from the adjacency matrix
    graph = nx.from_numpy_array(bigGraphmatrix, create_using=nx.DiGraph)

    # Draw the graph
    pos = nx.circular_layout(graph)  # Position nodes in a circular layout

    # Determine the edge widths based on the edge weights
    edge_widths = [ 100 * graph[u][v]['weight'] for u, v in graph.edges()]

    # Draw edges with varying thickness based on weights
    nx.draw_networkx_edges(graph, pos, width=edge_widths, arrows=True, arrowstyle='simple',
                        edge_color='darkgray', connectionstyle='arc3, rad = 0.1')

    for edge in almostBestEdges:
        edgeWidthsIndex = [ x for x, y in enumerate(graph.edges()) if y == edge ][0]
        nx.draw_networkx_edges(graph, pos, edgelist = [edge], width=edge_widths[edgeWidthsIndex], arrows=True, arrowstyle='simple',
        edge_color='red', connectionstyle='arc3, rad = 0.1')

    for edge in bestEdges:
        edgeWidthsIndex = [ x for x, y in enumerate(graph.edges()) if y == edge ][0]
        nx.draw_networkx_edges(graph, pos, edgelist = [edge], width= edge_widths[edgeWidthsIndex], arrows=True, arrowstyle='simple',
        edge_color='black', connectionstyle='arc3, rad = 0.1')


    # Draw nodes and labels
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color='blue', edgecolors='black')
    nx.draw_networkx_labels(graph, pos, font_color='white')
    
    # Creation of the text:

    # Add text at the top left corner
    ax.text(0.05, 0.95, f'Iteration: {iterationNumber}', transform=ax.transAxes, ha='left', va='top')

    fig.patch.set_visible(False)
    ax.axis('off')

    # Save the figure to a file
    fig.savefig(f"second_figs/{figureNuber}.jpg")

    # Close the figure
    plt.close(fig)

def loadIterationPharamons(index):
    data = dict()
    
    for i in range(Globals.graphSize + 1):
        data[i] = np.load(f"data/{index}_{i}.npy")
    
    return data

def loadTours():
    with open('data/tours.json') as json_file:
        data = json.load(json_file)
    
    return data

def loadBestTours():
    with open('data/best_tours.json') as json_file:
        data = json.load(json_file)
    
    return data

def main(): 
    tours = loadTours()
    bestTours = loadBestTours()
    bestTour = []

    adjacencies = np.load("data/adjacencies.npy")
    initialPharamons = np.load("data/0_0.npy")

    createSnapshot(adjacencies, initialPharamons, 0, 0)

    figureNuber = 1
    bestEdges = list()
    prevBestTour = list()
    secondPrevBestTour = list()
    for i in range(1, Globals.numOfIterations):
        tour = tours[f"{i}"]
        try:
            bestEdges = [(bestTours[f"{i - 1}"][l], bestTours[f"{i - 1}"][l+1]) for l in range(Globals.graphSize - 1)]
        except:
            pass

        try:
            prevBestTour = [(bestTours[f"{i - 2}"][l], bestTours[f"{i - 2}"][l+1]) for l in range(Globals.graphSize - 1)]
        except:
            pass

        try:
            secondPrevBestTour = [(bestTours[f"{i - 3}"][l], bestTours[f"{i - 3}"][l+1]) for l in range(Globals.graphSize - 1)]
        except:
            pass

        iterationPharamons = loadIterationPharamons(i)
        createSnapshot(adjacencies, initialPharamons, figureNuber, i, almostBestEdges = list(set(prevBestTour + secondPrevBestTour)) ,bestEdges = bestEdges)
        figureNuber = figureNuber + 1