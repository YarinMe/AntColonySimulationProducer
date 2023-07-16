from utils import Utils
from globals import Globals

import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def createSnapshot(adjacencies, pharamons, figureNuber, iterationNumber, edge = None, node = None, nodeColor = None, pharamonEdges = [], bestTour = []):
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
    edge_widths = [40 * graph[u][v]['weight'] for u, v in graph.edges()]

    # Draw edges with varying thickness based on weights
    nx.draw_networkx_edges(graph, pos, width=edge_widths, arrows=True, arrowstyle='simple',
                        edge_color='darkgray', connectionstyle='arc3, rad = 0.1')

    for e in bestTour:
        edgeWidthsIndex = [ x for x, y in enumerate(graph.edges()) if y == e ][0]
        nx.draw_networkx_edges(graph, pos, edgelist = [e], width=edge_widths[edgeWidthsIndex], arrows=True, arrowstyle='simple',
        edge_color='black', connectionstyle='arc3, rad = 0.1')


    # Draw nodes and labels
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color='blue', edgecolors='black')
    nx.draw_networkx_labels(graph, pos, font_color='white')

    if edge:
        edgeWidthsIndex = [ x for x, y in enumerate(graph.edges()) if y == edge ][0]
        nx.draw_networkx_edges(graph, pos, edgelist = [edge], width=edge_widths[edgeWidthsIndex], arrows=True, arrowstyle='simple',
            edge_color='red', connectionstyle='arc3, rad = 0.1')

    if node is not None:
        if nodeColor:
            nx.draw_networkx_nodes(graph, pos,  nodelist=[node], node_size=500, node_color=nodeColor, edgecolors='black')
        else:
            nx.draw_networkx_nodes(graph, pos,  nodelist=[node], node_size=500, node_color='red', edgecolors='black')

    # Creation of second the text:

    # Add text at the top left corner
    ax.text(0.05, 0.95, f'Iteration: {iterationNumber}', transform=ax.transAxes, ha='left', va='top')

    # Creation of second small graph:

    # Create an undirected graph from the adjacency matrix for the additional graph
    graph_additional = nx.from_numpy_array(pharamons, create_using=nx.DiGraph)

    # Create a small window for the additional graph
    ax_additional = plt.axes([0.75, 0.75, 0.2, 0.2])  # Define the position and size of the additional graph window
    pos_additional = nx.circular_layout(graph_additional)  # Position nodes in a circular layout
    edge_widths_additional = [15 * graph_additional[u][v]['weight'] for u, v in graph.edges()]

    # Draw the additional graph
    nx.draw_networkx_edges(graph_additional, pos_additional, width=edge_widths_additional, arrows=True, arrowstyle='-|>',
                        edge_color='darkgray', connectionstyle='arc3, rad = 0.1', ax=ax_additional)
    
    for edge in pharamonEdges:
            edgeWidthsIndex = [ x for x, y in enumerate(graph.edges()) if y == edge ][0]
            nx.draw_networkx_edges(graph_additional, pos_additional, edgelist = [edge], width=edge_widths_additional[edgeWidthsIndex], arrows=True, arrowstyle='-|>',
                        edge_color='red', connectionstyle='arc3, rad = 0.1', ax=ax_additional)
    
    nx.draw_networkx_nodes(graph_additional, pos_additional, node_size=200, node_color='blue', edgecolors='black', ax=ax_additional)
    nx.draw_networkx_labels(graph_additional, pos_additional, font_color='white')

    fig.patch.set_visible(False)
    ax.axis('off')

    # Save the figure to a file
    fig.savefig(f"figs/{figureNuber}.jpg")

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
    for i in range(1, Globals.numOfIterations):
        tour = tours[f"{i}"]
        try:
            bestTour = [(bestTours[f"{i - 1}"][l], bestTours[f"{i - 1}"][l+1]) for l in range(Globals.graphSize - 1)]
        except:
            pass

        iterationPharamons = loadIterationPharamons(i)
        edges = [(tour[l], tour[l+1]) for l in range(Globals.graphSize - 1)]
        
        usedEdges = list()
        # Figs for path
        for j in range(Globals.graphSize - 1):

            createSnapshot(adjacencies, iterationPharamons[j], figureNuber, i, node = tour[j], pharamonEdges = usedEdges, bestTour=bestTour)
            figureNuber = figureNuber + 1

            createSnapshot(adjacencies, iterationPharamons[j], figureNuber, i, edge = edges[j], pharamonEdges = usedEdges, bestTour=bestTour)
            usedEdges.append(edges[j])
            figureNuber = figureNuber + 1
        
        # Figs for last city visited
        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize - 1], figureNuber, i, node = tour[Globals.graphSize - 1], nodeColor = 'Orange', pharamonEdges = usedEdges, bestTour=bestTour)
        figureNuber = figureNuber + 1

        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize - 1], figureNuber, i, pharamonEdges = usedEdges, bestTour=bestTour)
        figureNuber = figureNuber + 1

        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize - 1], figureNuber, i, node = tour[Globals.graphSize - 1], nodeColor = 'Orange', pharamonEdges = usedEdges, bestTour=bestTour)
        figureNuber = figureNuber + 1

        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize - 1], figureNuber, i, pharamonEdges = usedEdges, bestTour=bestTour)
        figureNuber = figureNuber + 1

        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize - 1], figureNuber, i, node = tour[Globals.graphSize - 1], nodeColor = 'Orange', pharamonEdges = usedEdges, bestTour=bestTour)
        figureNuber = figureNuber + 1

        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize - 1], figureNuber, i, pharamonEdges = usedEdges, bestTour=bestTour)
        figureNuber = figureNuber + 1

        # Fig for graph after all local updates
        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize - 1], figureNuber, i, bestTour=bestTour)
        figureNuber = figureNuber + 1
        
        # Fig for graph after global updates
        createSnapshot(adjacencies, iterationPharamons[Globals.graphSize], figureNuber, i, bestTour=bestTour)
        figureNuber = figureNuber + 1