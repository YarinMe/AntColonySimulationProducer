from globals import Globals
from utils import Utils

import random
import numpy as np

class Ant:
    def __init__(self, currentCity):
        self.unvisitedCities = [False] * Globals.graphSize
        self.tour = list() # Tour is graphsize at the end of each engine iteration
        
        # Set starting city
        self.visit(currentCity)

    def visit(self, i):
        self.tour.append(i)
        self.unvisitedCities[i] = True
        self.currentCity = i

    def getUnvisitedCities(self):
        return [ i for i in range(len(self.unvisitedCities)) if not self.unvisitedCities[i]]
    
    def getTour(self):
        return self.tour

    def iterate(self, scores):
        # Note that the default is 0, and we update in score only with dedicated values

        if random.random() <= Globals.q_0:
            # Explotation - equation number 3
            nextCity = np.argmax(scores)
        else:
            # Exploration - equation number 1
            scoresSum = np.sum(scores)
            print(f"sum of scores {scores} is {scoresSum}")
            weightedScores = scores / scoresSum
            nextCity = random.choices(range(Globals.graphSize), weights = weightedScores)[0]

        return nextCity