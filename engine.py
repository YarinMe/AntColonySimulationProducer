from utils import Utils
from globals import Globals
from ant import Ant

import random
import math
import copy
import numpy as np

class Engine:

    def __init__(self, logger):
        self.adjacencies = Utils.createAdjacencies()
        self.initialPharamons = Utils.createPheromone(self.adjacencies)
        self.pharamons = np.matrix.copy(self.initialPharamons)
        self.resetAnts()
        self.bestTour = None
        self.bestLength = np.inf
        self.logger = logger

        self.logger.logAdjacencies(self.adjacencies)
        self.logger.logPharamons(0, self.initialPharamons)

    def resetAnts(self):
        ants = list()
        cities = [False] * Globals.graphSize
        
        # Ant's city is being picked randomly but with maximum of one ant in one city (for the case of antsNumber < graphSize)
        for i in range(Globals.antsNumber):
            city = random.randint(0, Globals.graphSize - 1)
            
            while cities[city]:
                city = random.randint(0, Globals.graphSize - 1)
            
            cities[city] = True
            ants.append(Ant(city))
        
        self.ants = ants

    def tour(self):
        self.logger.newIteration()

        # This is minus one because we start in a city, then we have graphSize - 1 cities to visit
        for i in range(Globals.graphSize - 1):
            [ self.iterate(ant) for ant in self.ants ]
            self.logger.logPharamons(i, self.pharamons)

        self.logger.logPharamons(Globals.graphSize - 1, self.pharamons)
        self.globalUpdate()
        self.logger.logPharamons(Globals.graphSize, self.pharamons)
        
        self.logger.logTour(self.ants[random.randint(0, Globals.antsNumber - 1)].getTour())

        print(self.pharamons)
        
    def iterate(self, ant):
        # Note that the default value of a score is 0, and we update in score only with dedicated values
        scores = np.zeros(Globals.graphSize)

        for j in ant.getUnvisitedCities():
            scores[j] = Utils.getScore(self.pharamons[ant.currentCity][j], self.adjacencies[ant.currentCity][j])
        
        nextCity = ant.iterate(scores)
            
        self.pharamons[ant.currentCity][nextCity] = Utils.localUpdateRule(
            self.pharamons[ant.currentCity][nextCity], self.initialPharamons[ant.currentCity][nextCity])

        ant.visit(nextCity)
    
    def calculateTourLenth(self, ant):
        lengths = np.zeros(Globals.graphSize)

        for i in range(Globals.graphSize - 1):
            # This doesn't flow out of index because the tours has one more walk to the beginning of the tour
            lengths[i] = self.adjacencies[ant.tour[i]][ant.tour[i+1]]

        return np.sum(lengths)

    def globalUpdate(self):
        lengths = [ self.calculateTourLenth(ant) for ant in self.ants ]
        bestLength = np.min(lengths)
        
        print(f"in global update. best lenght for is {bestLength} out of {lengths}, with current best {self.bestLength}")
        if bestLength < self.bestLength:
            print(f"caught new best! for {bestLength}")
            self.bestTour = copy.copy((self.ants[np.argmin(lengths)]).getTour())
            print(f"new best {self.bestTour}")
            self.bestLength = bestLength
            self.logger.logBestTour(self.bestTour)

        bestTourCoordinates = [ ( self.bestTour[i], self.bestTour[i + 1]) for i in range(Globals.graphSize - 1) ]

        for i in range(Globals.graphSize):
            for j in range(Globals.graphSize):
                if (i, j) in bestTourCoordinates:
                    self.pharamons[i][j] = Utils.globalUpdateRule(self.pharamons[i][j], self.bestLength)
                else:
                    self.pharamons[i][j] = Utils.globalUpdateRule(self.pharamons[i][j], 0)

        