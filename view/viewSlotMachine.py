import numpy as np
from model.symbols import FaceSymbol,WildSymbol,ScatterSymbol
from view.viewSymbol import *



class ViewSlotMachine:
    def __init__(self,slotMachine, background,tileSize, type, speed):
        self.slotMachine = slotMachine
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background,[910,600])
        self.tileSize = tileSize
        self.type = type
        self.defaultSpeed = speed
        self.currentSpeed = speed
        self.animSprite = 0
        self.currentTable = np.zeros(slotMachine.dimension, dtype=ViewSymbol)
        self.spinFinished = True
        self.mute = False
        pygame.mixer.init()
        self.reelStopSound = pygame.mixer.Sound("assets/reelstop.wav")
        self.reelWildSound = pygame.mixer.Sound("assets/wild.wav")


        self.readyToPlaySoundREEL = [False for _ in range(slotMachine.dimension[0])]
        self.hasPlayedSoundREEL = [False for _ in range(slotMachine.dimension[0])]

        self.readyToPlaySoundWILD = [False for _ in range(slotMachine.dimension[0])]
        self.hasPlayedSoundWILD = [False for _ in range(slotMachine.dimension[0])]

    def display(self, screen):
        screen.fill('black')
        screen.blit(self.background,[45,60])
        cols = self.slotMachine.dimension[0]
        rows = self.slotMachine.dimension[1]
        for i in range(cols):
            for j in range(rows):
                currentViewSymbol = self.currentTable[cols-i-1][rows-j-1]
                if currentViewSymbol is not None and currentViewSymbol is not 0:
                    if currentViewSymbol.symbol.name == "wild" or currentViewSymbol.symbol.name == "scatter" :
                        currentViewSymbol.image = pygame.transform.scale(currentViewSymbol.image,[self.tileSize*1.7,self.tileSize*1.7])

                    elif currentViewSymbol.symbol.name == "swords":
                        currentViewSymbol.image = pygame.transform.scale(currentViewSymbol.image,[self.tileSize*1.7,self.tileSize*1.7])
                    else:
                        currentViewSymbol.image = pygame.transform.scale(currentViewSymbol.image,[self.tileSize,self.tileSize])
                        
                    self.slideIn(screen, currentViewSymbol, cols ,rows,cols-i-1, rows-j-1)
            self.playReelStopSound(i)

        if self.spinFinished:
            self.displayWins(screen)

        return not self.spinFinished
    
    def spin(self):
        print("Needs to be overwriten 'spin()' ")

    def slideIn(self,screen, symbol, cols, rows, i ,j):
        if self.type == "reel":
            movingValue = round(self.animSprite*self.tileSize*self.currentSpeed) - (rows*(j-1)*self.tileSize)/rows -((i+1)*cols*self.tileSize)*(4/5)
        elif self.type == "piece":    
            movingValue = self.animSprite*0.8*self.tileSize*self.currentSpeed - (rows*(j-1)*self.tileSize)*(2/5)-((i+3)*cols*self.tileSize)/3

        if  movingValue < (rows-j-1)*self.tileSize:
            symbol.x = 93 + i * self.tileSize * 1.35
            symbol.y = 104 + movingValue
        else:
            symbol.x = 93 + i * self.tileSize * 1.35
            symbol.y = 104 + (rows-j-1)*self.tileSize
            if j == rows-1:
                if not self.hasPlayedSoundREEL[i]:
                    self.readyToPlaySoundREEL[i] = True
                    
                self.playWildSound(i)
            if i == cols-1 and j == rows-1:
                self.spinFinished = True

        if symbol.symbol.name =="swords" or symbol.symbol.name == "wild" or symbol.symbol.name =="scatter":
            symbol.x -= (self.tileSize*1.7 - self.tileSize) / 2
            symbol.y -= (self.tileSize*1.7 - self.tileSize) / 2

        if symbol.symbol.name == "wild":
            if not self.hasPlayedSoundWILD[i]:
                self.readyToPlaySoundWILD[i] = True
            
        screen.blit(symbol.image,[symbol.x,symbol.y])

    def displayWins(self, screen):
        pass
    
    def playReelStopSound(self, i):
        
        if self.readyToPlaySoundREEL[i] and not self.mute:
            self.reelStopSound.play()
            self.readyToPlaySoundREEL[i] = False
            self.hasPlayedSoundREEL[i] = True
    
    def playWildSound(self,i):
        if self.readyToPlaySoundWILD[i] and not self.mute:
            self.reelWildSound.play()
            self.readyToPlaySoundWILD[i] = False
            self.hasPlayedSoundWILD[i] = True

