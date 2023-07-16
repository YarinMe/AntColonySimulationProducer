from globals import Globals
from ant import Ant
from engine import Engine
from logger import Logger

import numpy as np

def main():
    logger = Logger()
    engine = Engine(logger)

    for i in range(Globals.numOfIterations):
        print(f"in iteration number {i}")
        engine.resetAnts()
        engine.tour()

    logger.dumpTours()
    logger.dumpBestTours()