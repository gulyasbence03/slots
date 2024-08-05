import numpy as np
from model.symbols import *
import secrets


class SlotMachine:
    def __init__(self,dimension,symbolsOnReel):
        self.symbolsOnReel = symbolsOnReel
        self.cols = dimension[0]
        self.rows = dimension[1]

        self.reels = np.empty((self.cols,symbolsOnReel),dtype=Symbol)
        self.table = np.empty(dimension,dtype=Symbol)

    def setReels(self, listOfReels):
        if len(listOfReels) != self.cols or self.symbolsOnReel != len(listOfReels[0]):
            print("Insufficient reel value, due to size difference")
        else:
            for col in range(self.cols):
                self.reels[col] = listOfReels[col]
                
    
    def spin(self):
        for col in range(self.cols):
            randomNumber = secrets.randbelow(self.symbolsOnReel-self.rows)
            secrets._sysrand.shuffle(self.reels[col])
            self.table[col] = self.reels[col][randomNumber:randomNumber+self.rows]
    
    def getElement(self,i,j):
        return self.table[i][j]
    
    def setElement(self,i,j,elem):
        self.table[i][j] = elem
    
    def checkBonus(self, bonusOn):
        # Bonus Game
        if not bonusOn:
            bonusCounter = 0
            for i in range(self.cols):
                for j in range(self.rows):
                    currentSymbol = self.table[i][j]
                    if currentSymbol is not None and currentSymbol != 0:
                        if currentSymbol.name == "scatter":
                            bonusCounter+=1
                    
            if bonusCounter >= 3:
                return bonusCounter
        return 0