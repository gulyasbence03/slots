import numpy as np
from model.symbols import *
import secrets


class SlotMachine:
    def __init__(self,dimension,symbolsOnReel):
        self.reels = np.empty((dimension[0],symbolsOnReel),dtype=Symbol)
        self.table = np.empty(dimension,dtype=Symbol)

        self.symbolsOnReel = symbolsOnReel
        self.dimension = dimension

    def setReels(self, listOfReels):
        if len(listOfReels) != self.dimension[0] or self.symbolsOnReel != len(listOfReels[0]):
            print("Insufficient reel value, due to size difference")
        else:
            for col in range(self.dimension[0]):
                    self.reels[col] = listOfReels[col]
                
    
    def spin(self):
        for col in range(self.dimension[0]):
            randomNumber = secrets.randbelow(self.symbolsOnReel-self.dimension[1])
            secrets._sysrand.shuffle(self.reels[col])
            self.table[col] = self.reels[col][randomNumber:randomNumber+self.dimension[1]]
    
    def getElement(self,i,j):
        return self.table[i][j]