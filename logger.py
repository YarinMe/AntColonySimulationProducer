import numpy as np
import json

class Logger:

    def __init__(self):
        self.iterationNuber = 0
        self.tours = dict()
        self.bestTours = dict()

    def logPharamons(self, index, pharamons):
        np.save(f"data/{self.iterationNuber}_{index}", pharamons)
        
    def newIteration(self):
        self.iterationNuber += 1

    def logTour(self, tour):
        self.tours[self.iterationNuber] = [ int(i) for i in tour ]
    
    def logBestTour(self, bestTour):
        self.bestTours[self.iterationNuber] = [ int(i) for i in bestTour ]
    
    def logAdjacencies(self, adjacencies):
        np.save(f"data/adjacencies", adjacencies)

    def dumpTours(self):
        with open("data/tours.json", "w") as outfile:
            json.dump(self.tours, outfile, indent = 4)

    def dumpBestTours(self):
        print(f"best tours are: {self.bestTours}")
        with open("data/best_tours.json", "w") as outfile:
            json.dump(self.bestTours, outfile, indent = 4)