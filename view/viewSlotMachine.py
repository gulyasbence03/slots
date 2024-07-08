import numpy as np
from model.symbols import FaceSymbol,WildSymbol,ScatterSymbol
from view.viewSymbol import *



class ViewSlotMachine:
    def __init__(self,slotMachine, background,tileSize, type, speed):
        self.slotMachine = slotMachine
        self.background = background
        self.tileSize = tileSize
        self.type = type
        self.defaultSpeed = speed
        self.currentSpeed = speed
        self.animSprite = 0
        self.currentTable = np.zeros(slotMachine.dimension, dtype=ViewSymbol)
        self.spinFinished = True

    def display(self, screen):
        screen.fill('white')
        
        cols = self.slotMachine.dimension[0]
        rows = self.slotMachine.dimension[1]
        for i in range(cols):
            for j in range(rows):
                currentViewSymbol = self.currentTable[i][j]
                if currentViewSymbol is not None and currentViewSymbol is not 0:
                    currentViewSymbol.image = pygame.transform.scale(currentViewSymbol.image,[self.tileSize,self.tileSize]).convert()
                    self.slideIn(screen, currentViewSymbol, cols ,rows, i, j)

        return not self.spinFinished
    
    def spin(self):
            self.slotMachine.spin()
            self.spinFinished = False
            cols = self.slotMachine.dimension[0]
            rows = self.slotMachine.dimension[1]
            for i in range(cols):
                for j in range(rows):
                    currentSymbol = self.slotMachine.getElement(i,j)
                    print(currentSymbol)
                    currentViewSymbol = None

                    if isinstance(currentSymbol,FaceSymbol):
                        currentViewSymbol = ViewFaceSymbol(currentSymbol,"assets/melon.png")
                    elif isinstance(currentSymbol,ScatterSymbol):
                        currentViewSymbol = ViewScatterSymbol(currentSymbol,"assets/diamond.png")
                    elif isinstance(currentSymbol,WildSymbol):
                        currentViewSymbol = ViewWildSymbol(currentSymbol,"assets/horseshoe.png")
                    self.currentTable[i][rows-j-1] = currentViewSymbol
                print()
            self.animSprite = 0

    def slideIn(self,screen, symbol, cols, rows, i ,j):
        if self.type == "reel":
            if round(self.animSprite*120*self.currentSpeed) - (rows*(j-1)*120)/rows-((i+1)*cols*120) < (rows-j-1)*120:
                symbol.x = 90 + i * 120
                symbol.y =  60 + round(self.animSprite*120*self.currentSpeed) - (rows*(j-1)*120)/rows - ((i+1)*cols*120)
            else:
                symbol.x = 90 + i * 120
                symbol.y = 60 + (rows-j-1)*120
                if i == cols-1 and j == rows-1:
                    self.spinFinished = True

        elif self.type == "piece":    
            if self.animSprite*0.8*120*self.currentSpeed - (rows*(j-1)*120)/3-((i+3)*cols*120)/3 < (rows-j-1)*120:
                symbol.x = 90 + i * 120
                symbol.y = 60 + self.animSprite*0.8*120*self.currentSpeed - (rows*(j-1)*120)/3 - ((i+3)*cols*120)/3
            else:
                symbol.x = 90 + i * 120
                symbol.y = 60 + (rows-j-1)*120
                if i == cols-1 and j == rows-1:
                    self.spinFinished = True

        screen.blit(symbol.image,[symbol.x,symbol.y])
    

    