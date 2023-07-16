from globals import Globals

import numpy as np
import math

class Utils:
    def getNearestNeighbor(rowIndex, adjacencies):
        # Remove the diagonal ones because they always has 0 in them.
        neighbors = adjacencies[rowIndex]
        tempNeighbor = 0
        min = np.inf
        for i in range(Globals.graphSize):
            if i == rowIndex:
                continue
            
            tempMin = neighbors[i]
            if (tempMin < min):
                min = tempMin
        
        return min

    def getDefaultPheromone(rowIndex, adjacencies):
        nearestNeighbor = Utils.getNearestNeighbor(rowIndex, adjacencies)
        return 1.0 / (Globals.graphSize * Utils.getNearestNeighbor(rowIndex, adjacencies))

    def createAdjacencies():
        adjacencies = np.random.randint(Globals.minDefaultWeight, Globals.maxDefaultWeight + 1, size=(Globals.graphSize, Globals.graphSize))
        np.fill_diagonal(adjacencies, 0)
        print(adjacencies)

        return adjacencies

    def createPheromone(adjacencies):
        defalutPheromones = np.zeros(Globals.graphSize)
        for i in range(Globals.graphSize):
            defalutPheromones[i] = Utils.getDefaultPheromone(i, adjacencies)

        # Extrapolate each scalar to fill one line in the correspondence line indexes in this scalar
        pheromones = np.tile(defalutPheromones, (len(defalutPheromones), 1))
        pheromones = pheromones.T

        np.fill_diagonal(pheromones, 0)
        print(pheromones)

        return pheromones

    def getScore(pheromone, distance):
        # The letter that looks like n
        etta = 1 / distance
        
        return pheromone * math.pow(etta, Globals.beta)

    def localUpdateRule(pheromone, initialPheromone):
        # Here delta = initialPheromone. It can be done with Ant-q implementation
        return (((1 - Globals.rho) * pheromone) + (Globals.rho * initialPheromone))

    def globalUpdateRule(pheromone, bestLength):
        if bestLength == 0:
            return ((1 - Globals.alpha) * pheromone)
        
        return (((1 - Globals.alpha) * pheromone) + (Globals.alpha / bestLength))