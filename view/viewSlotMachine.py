import numpy as np
from model.symbols import FaceSymbol,WildSymbol,ScatterSymbol
from view.viewSymbol import *
from collections import Counter


class ViewSlotMachine:
    def __init__(self,slotMachine, background,tileSize, type, speed):
        self.slotMachine = slotMachine
        self.lines = self.setLines(20)
        self.winLines = None

        # Visual
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background,[910,600])
        self.tileSize = tileSize
        self.type = type
        self.defaultSpeed = speed
        self.currentSpeed = speed
        self.animSprite = 0
        self.currentTable = np.zeros(slotMachine.dimension, dtype=ViewSymbol)
        self.spinFinished = True

        # Sound
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

        if self.spinFinished and self.currentTable[0][0] is not 0:
            self.checkWins()
            self.displayWins(screen)

        return not self.spinFinished

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

    def checkWins(self):
        winners = []
        for line in self.lines:
            if self.isWinner(line):
                winners.append(line)
        self.winLines = winners

    def isWinner(self,line):
        rows = self.slotMachine.dimension[1]
        # all symbols in given line
        symbolsInLine = []
        for elem in line:
            symbolsInLine.append(self.currentTable[elem[1]][rows-elem[0]-1].symbol)
        symbolsInLine = Counter(symbolsInLine).most_common()
        # sort symbol types by amount, so bigger chance for
        sortedSymbols = []
        for doub in symbolsInLine:
            if doub[0].name not in ["wild","scatter"]:
                sortedSymbols.append(doub[0])
        
        
        
        for symbol in sortedSymbols:
            
            first = self.currentTable[line[0][1]][rows-line[0][0]-1].symbol
            second = self.currentTable[line[1][1]][rows-line[1][0]-1].symbol
            third = self.currentTable[line[2][1]][rows-line[2][0]-1].symbol
            fourth = self.currentTable[line[3][1]][rows-line[3][0]-1].symbol
            fifth = self.currentTable[line[4][1]][rows-line[4][0]-1].symbol
            
            symbolName = symbol.name

            """ RULES """

            if first.name in [symbolName,"wild"]:
                # first 3 symbol or wild (X X X any any)
                if second.name in [symbolName,"wild"] and third.name in [symbolName,"wild"]:
                    # first 4 symbol or wild (X X X X any)
                    if fourth.name in [symbolName,"wild"]:
                        # first 5 symbol or wild (X X X X X)
                        if fifth.name in [symbolName,"wild"]:
                            print(f"X X X X X {symbolName}")
                            return True
                        else:
                            print(f"X X X X - {symbolName}")
                            return True
                    else:
                        #print(f"X X X - - {symbolName}")
                        pass
                    
            
            #first X next continous 3 symbol or wild (any X X X any)
            elif second.name in [symbolName,"wild"] and third.name in [symbolName,"wild"] and fourth.name in [symbolName,"wild"]:
                # first 5 symbol or wild
                if fifth.name in [symbolName,"wild"]:
                    print(f"- X X X X {symbolName}")
                    return True
                else:
                    #print(f"- X X X - {symbolName}")
                    pass
                

            



    def setLines(self,amount):
        line1 = [(0,0),(0,1),(0,2),(0,3),(0,4)]
        line2 = [(1,0),(1,1),(1,2),(1,3),(1,4)]
        line3 = [(2,0),(2,1),(2,2),(2,3),(2,4)]
        line4 = [(3,0),(3,1),(3,2),(3,3),(3,4)]

        line5 = [(0,0),(1,1),(2,2),(1,3),(0,4)]
        line6 = [(1,0),(2,1),(3,2),(2,3),(1,4)]
        line7 = [(3,0),(2,1),(1,2),(2,3),(3,4)]
        line8 = [(2,0),(1,1),(0,2),(1,3),(2,4)]

        line9 = [(0,0),(1,1),(0,2),(1,3),(0,4)]
        line10= [(3,0),(2,1),(3,2),(2,3),(3,4)]
        line11= [(1,0),(0,1),(1,2),(0,3),(1,4)]
        line12= [(2,0),(3,1),(2,2),(3,3),(2,4)]
        line13= [(1,0),(2,1),(1,2),(2,3),(1,4)]
        line14= [(2,0),(1,1),(2,2),(1,3),(2,4)]

        line15= [(0,0),(1,1),(1,2),(1,3),(0,4)]
        line16= [(3,0),(2,1),(2,2),(2,3),(3,4)]
        line17= [(1,0),(0,1),(0,2),(0,3),(1,4)]
        line18= [(2,0),(3,1),(3,2),(3,3),(2,4)]
        line19= [(1,0),(2,1),(2,2),(2,3),(1,4)]
        line20= [(2,0),(1,1),(1,2),(1,3),(2,4)]

        lines = [line1,line2,line3,line4,line5,
                 line6,line7,line8,line9,line10,
                 line11,line12,line13,line14,line15,
                 line16,line17,line18,line19,line20
                 ]
        
        return lines[:amount]

    def displayWins(self, screen):
        #for line in winingLines: or lines = winningLines
        if len(self.winLines) > 0:
            line = self.winLines[int((self.animSprite/30) % len(self.winLines))]
            for i in range(len(line)-1):
                start = (93 + line[i][1] * self.tileSize * 1.35 + self.tileSize/2,
                            104 + line[i][0] * self.tileSize + self.tileSize/2)  
                end = (93 + line[i+1][1] * self.tileSize * 1.35 + self.tileSize/2,
                            104 + line[i+1][0] * self.tileSize + self.tileSize/2)
                pygame.draw.line(screen,"gold",start,end,7)

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

    def spin(self):
        print("Needs to be overwriten 'spin()' ")


