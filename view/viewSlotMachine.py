import numpy as np
from model.symbols import FaceSymbol,WildSymbol,ScatterSymbol
from view.viewSymbol import *



class ViewSlotMachine:
    def __init__(self,slotMachine, background,tileSize, type, speed):
        self.slotMachine = slotMachine
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background,[920,600])
        self.tileSize = tileSize
        self.type = type
        self.defaultSpeed = speed
        self.currentSpeed = speed
        self.animSprite = 0
        self.currentTable = np.zeros(slotMachine.dimension, dtype=ViewSymbol)
        self.spinFinished = True

    def display(self, screen):
        screen.fill('black')
        screen.blit(self.background,[45,60])
        cols = self.slotMachine.dimension[0]
        rows = self.slotMachine.dimension[1]
        for i in range(cols):
            for j in range(rows):
                currentViewSymbol = self.currentTable[i][j]
                if currentViewSymbol is not None and currentViewSymbol is not 0:
                    currentViewSymbol.image = pygame.transform.scale(currentViewSymbol.image,[self.tileSize,self.tileSize])
                    self.slideIn(screen, currentViewSymbol, cols ,rows, i, j)

        return not self.spinFinished
    
    def spin(self):
        print("Needs to be overwriten 'spin()' ")

    def slideIn(self,screen, symbol, cols, rows, i ,j):
        if self.type == "reel":
            movingValue = round(self.animSprite*self.tileSize*self.currentSpeed) - (rows*(j-1)*self.tileSize)/rows-((i+1)*cols*self.tileSize)*(4/5)
        elif self.type == "piece":    
            movingValue = self.animSprite*0.8*self.tileSize*self.currentSpeed - (rows*(j-1)*self.tileSize)/3-((i+3)*cols*self.tileSize)/3

        if  movingValue < (rows-j-1)*self.tileSize:
            symbol.x = 95 + i * self.tileSize * 1.35
            symbol.y = 100 + movingValue
        else:
            symbol.x = 95 + i * self.tileSize * 1.35
            symbol.y = 100 + (rows-j-1)*self.tileSize
            if i == cols-1 and j == rows-1:
                self.spinFinished = True

        screen.blit(symbol.image,[symbol.x,symbol.y])

    

    