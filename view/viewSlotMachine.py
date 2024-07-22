import numpy as np
from model.symbols import FaceSymbol,WildSymbol,ScatterSymbol
from view.viewSymbol import *
from collections import Counter
from view.line import *


class ViewSlotMachine:
    def __init__(self,slotMachine, background,tileSize, type, speed):
        self.slotMachine = slotMachine
        self.lines = self.setLines(26)
        self.winLines = None
        self.selectedSymbols = {}

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

    def clear(self,screen):
        screen.fill('black')
        screen.blit(self.background,[45,60])
    def display(self, screen):
        self.clear(screen)
        cols = self.slotMachine.dimension[0]
        rows = self.slotMachine.dimension[1]
        for i in range(cols):
            for j in range(rows):
                currentViewSymbol = self.currentTable[cols-i-1][rows-j-1]
                if currentViewSymbol is not None and currentViewSymbol is not 0:
                    currentViewSymbol.image = pygame.transform.scale(currentViewSymbol.image,[currentViewSymbol.symbolSize,currentViewSymbol.symbolSize])
                        
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


        if symbol.symbol.name == "wild":
            if not self.hasPlayedSoundWILD[i]:
                self.readyToPlaySoundWILD[i] = True

        symbol.x -= (symbol.symbolSize-self.tileSize)  / 2
        symbol.y -= (symbol.symbolSize-self.tileSize)  / 2

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
        for elem in line.line:
            symbolsInLine.append(self.currentTable[elem[1]][rows-elem[0]-1].symbol)
        symbolsInLine = Counter(symbolsInLine).most_common()
        # sort symbol types by amount, so bigger chance for
        sortedSymbols = []
        for doub in symbolsInLine:
            if doub[0].name not in ["wild","scatter"]:
                sortedSymbols.append(doub[0])
        
        
        
        for symbol in sortedSymbols:
            
            first = self.currentTable[line.line[0][1]][rows-line.line[0][0]-1]
            second = self.currentTable[line.line[1][1]][rows-line.line[1][0]-1]
            third = self.currentTable[line.line[2][1]][rows-line.line[2][0]-1]
            fourth = self.currentTable[line.line[3][1]][rows-line.line[3][0]-1]
            fifth = self.currentTable[line.line[4][1]][rows-line.line[4][0]-1]
            
            symbolName = symbol.name

            """ RULES """

            temp_list = []
            if first.symbol.name in [symbolName,"wild"]:
                # first 3 symbol or wild (X X X any any)
                if second.symbol.name in [symbolName,"wild"] and third.symbol.name in [symbolName,"wild"]:
                    # first 4 symbol or wild (X X X X any)
                    if fourth.symbol.name in [symbolName,"wild"]:
                        # first 5 symbol or wild (X X X X X)
                        if fifth.symbol.name in [symbolName,"wild"]:
                            #print(f"X X X X X {symbolName}")
                            
                            temp_list.append((line.line[0][1],rows-line.line[0][0]-1))
                            temp_list.append((line.line[1][1],rows-line.line[1][0]-1))
                            temp_list.append((line.line[2][1],rows-line.line[2][0]-1))
                            temp_list.append((line.line[3][1],rows-line.line[3][0]-1))
                            temp_list.append((line.line[4][1],rows-line.line[4][0]-1))   
                            self.selectedSymbols[line.name] = temp_list
                            return True
                        else:
                            #print(f"X X X X - {symbolName}")
                            temp_list.append((line.line[0][1],rows-line.line[0][0]-1))
                            temp_list.append((line.line[1][1],rows-line.line[1][0]-1))
                            temp_list.append((line.line[2][1],rows-line.line[2][0]-1))
                            temp_list.append((line.line[3][1],rows-line.line[3][0]-1)) 
                            self.selectedSymbols[line.name] = temp_list
                            
                            return True
                    else:
                        #print(f"X X X - - {symbolName}")
                        pass
                    
            
            #first X next continous 3 symbol or wild (any X X X any)
            elif second.symbol.name in [symbolName,"wild"] and third.symbol.name in [symbolName,"wild"] and fourth.symbol.name in [symbolName,"wild"]:
                # first 5 symbol or wild
                if fifth.symbol.name in [symbolName,"wild"]:
                    #print(f"- X X X X {symbolName}")
                    temp_list.append((line.line[1][1],rows-line.line[1][0]-1))
                    temp_list.append((line.line[2][1],rows-line.line[2][0]-1))
                    temp_list.append((line.line[3][1],rows-line.line[3][0]-1))
                    temp_list.append((line.line[4][1],rows-line.line[4][0]-1))  
                    self.selectedSymbols[line.name] = temp_list
                    
                    return True
                else:
                    #print(f"- X X X - {symbolName}")
                    pass
            
                
    def setLines(self,amount):
        line1 = Line("line1", [(0,0),(0,1),(0,2),(0,3),(0,4)])
        line2 = Line("line2",[(1,0),(1,1),(1,2),(1,3),(1,4)])
        line3 = Line("line3",[(2,0),(2,1),(2,2),(2,3),(2,4)])
        line4 = Line("line4",[(3,0),(3,1),(3,2),(3,3),(3,4)])

        line5 = Line("line5",[(0,0),(1,1),(2,2),(1,3),(0,4)])
        line6 = Line("line6",[(1,0),(2,1),(3,2),(2,3),(1,4)])
        line7 = Line("line7",[(3,0),(2,1),(1,2),(2,3),(3,4)])
        line8 = Line("line8",[(2,0),(1,1),(0,2),(1,3),(2,4)])

        line9 = Line("line9",[(0,0),(1,1),(0,2),(1,3),(0,4)])
        line10= Line("line10",[(3,0),(2,1),(3,2),(2,3),(3,4)])
        line11= Line("line11",[(1,0),(0,1),(1,2),(0,3),(1,4)])
        line12= Line("line12",[(2,0),(3,1),(2,2),(3,3),(2,4)])
        line13= Line("line13",[(1,0),(2,1),(1,2),(2,3),(1,4)])
        line14= Line("line14",[(2,0),(1,1),(2,2),(1,3),(2,4)])

        line15= Line("line15",[(0,0),(1,1),(1,2),(1,3),(0,4)])
        line16= Line("line16",[(3,0),(2,1),(2,2),(2,3),(3,4)])
        line17= Line("line17",[(1,0),(0,1),(0,2),(0,3),(1,4)])
        line18= Line("line18",[(2,0),(3,1),(3,2),(3,3),(2,4)])
        line19= Line("line19",[(1,0),(2,1),(2,2),(2,3),(1,4)])
        line20= Line("line20",[(2,0),(1,1),(1,2),(1,3),(2,4)])

        line21= Line("line21",[(1,0),(1,1),(0,2),(1,3),(1,4)])
        line22= Line("line22",[(2,0),(2,1),(1,2),(2,3),(2,4)])
        line23= Line("line23",[(3,0),(3,1),(2,2),(3,3),(3,4)])
        line24= Line("line24",[(0,0),(0,1),(1,2),(0,3),(0,4)])
        line25= Line("line25",[(1,0),(1,1),(2,2),(1,3),(1,4)])
        line26= Line("line26",[(2,0),(2,1),(3,2),(2,3),(2,4)])


        lines = [line1,line2,line3,line4,line5,
                 line6,line7,line8,line9,line10,
                 line11,line12,line13,line14,line15,
                 line16,line17,line18,line19,line20,
                 line21,line22,line23,line24,line25,
                 line26]
        
        return lines[:amount]

    def displayWins(self, screen):
        # DRAW LINES
        if len(self.winLines) > 0:
            line = self.winLines[int((self.animSprite/30) % len(self.winLines))]
            for i in range(len(line.line)-1):
                start = (93 + line.line[i][1] * self.tileSize * 1.35 + self.tileSize/2,
                            104 + line.line[i][0] * self.tileSize + self.tileSize/2)  
                end = (93 + line.line[i+1][1] * self.tileSize * 1.35 + self.tileSize/2,
                            104 + line.line[i+1][0] * self.tileSize + self.tileSize/2)
                

                pygame.draw.line(screen,"gold",start,end,7)

                # ANIMATE SYMBOLS
                currLine = self.selectedSymbols[line.name]
                for elem in currLine:       
                    symbol = self.currentTable[elem[0],elem[1]]
                    #print(f"({elem[1]},{elem[0]}) {symbol.symbol.name}",end="")
                    originX = 93 + elem[0] * self.tileSize * 1.35 
                    originY = 105 + (self.slotMachine.dimension[1]-elem[1]-1)*self.tileSize

                    outlineX = originX - (symbol.symbolSize*0.8-self.tileSize)  / 2
                    outlineY = originY - (symbol.symbolSize*0.8-self.tileSize)  / 2

                    originX -= (symbol.symbolSize-self.tileSize)  / 2
                    originY -= (symbol.symbolSize-self.tileSize)  / 2

                    

                    tempSurface = pygame.Surface((symbol.symbolSize,symbol.symbolSize),pygame.SRCALPHA)
                    tempSurface.set_alpha(35) 

                    x = originX
                    y = originY
                    if symbol.symbol.name == "wild":
                        tempSurface.set_alpha(75) 
                        pygame.draw.rect(tempSurface,pygame.Color(220,20,60),pygame.Rect(0,0,symbol.symbolSize*0.8,symbol.symbolSize*0.8))
                        x = outlineX+1
                        y = outlineY-4
                    else:
                        pygame.draw.circle(tempSurface,pygame.Color(220,20,60),[symbol.symbolSize*0.5,symbol.symbolSize*0.5],symbol.symbolSize*0.5)
                    screen.blit(tempSurface,(x,y))
                    screen.blit(symbol.image, [originX,originY])
                    #print()   

        

    
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


