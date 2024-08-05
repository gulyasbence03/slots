import numpy as np
from model.symbols import FaceSymbol,WildSymbol,ScatterSymbol
from view.viewSymbol import *
from collections import Counter
from view.line import *
from sound import *

class ViewSlotMachine:
    def __init__(self,slotMachine, background,tileSize, type, speed, account):
        # LOGIC
        self.slotMachine = slotMachine
        self.account = account
        self.lines = self.setLines(26)
        self.winLines = None
        self.selectedSymbols = {}
        self.isWinCounted = False
    
        # Visual
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background,[910,600])
        self.tileSize = tileSize
        self.type = type
        self.defaultSpeed = speed
        self.currentSpeed = speed
        self.animSprite = 0
        self.currentTable = np.zeros((slotMachine.cols,slotMachine.rows), dtype=ViewSymbol)
        self.spinFinished = True

        # Sound
        self.soundPlayer = SoundPlayer(slotMachine.cols,slotMachine.rows)

        # Bonusgame
        self.bonusOn = False
        self.bonusScreen = False
        self.freeSpins = 0
        self.bonusWildSlots = []
        self.bonusWildisOut = [[False]*slotMachine.rows for _ in range(slotMachine.cols)]

    def clearScreen(self,screen):
        screen.fill('black')
        screen.blit(self.background,[45,60])

    def display(self, screen):
        self.clearScreen(screen)
        if self.bonusScreen and self.spinFinished:
            self.displayBonusScreen(screen)
            return not self.spinFinished

        for i in range(self.slotMachine.cols):
            for j in range(self.slotMachine.rows):
                currentViewSymbol = self.currentTable[self.slotMachine.cols-i-1][self.slotMachine.rows-j-1]
                if currentViewSymbol is not None and currentViewSymbol != 0:
                    currentViewSymbol.image = pygame.transform.scale(currentViewSymbol.image,[currentViewSymbol.symbolSize,currentViewSymbol.symbolSize])
                        
                    self.slideIn(screen, currentViewSymbol, self.slotMachine.cols ,self.slotMachine.rows,self.slotMachine.cols-i-1, self.slotMachine.rows-j-1)
            
            self.soundPlayer.playReelStopSound(i)

        if self.spinFinished and self.currentTable[0][0] != 0:
            self.checkWins()
            self.countWins(screen)
            self.checkBonus()
            self.displayWins(screen)

        self.displayBalance(screen)
        if self.bonusOn:
            self.displayFreeSpins(screen)
            self.displayBonusTotalWin(screen)

        return not self.spinFinished

    def checkBonus(self):
        # Bonus Game
        if not self.bonusOn:
            bonusCounter = 0
            for i in range(self.slotMachine.cols):
                for j in range(self.slotMachine.rows):
                    currentViewSymbol = self.currentTable[self.slotMachine.cols-i-1][self.slotMachine.rows-j-1]
                    if currentViewSymbol is not None and currentViewSymbol != 0:
                        if currentViewSymbol.symbol.name == "scatter":
                            bonusCounter+=1

            if bonusCounter >= 3:
                self.bonusScreen = True
                self.bonusOn = True
                self.freeSpins = bonusCounter

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
        
            # if reel stopped to play the wild sounds if there is any
            if self.soundPlayer.checkIfReelStopped(j,rows,i):
                self.soundPlayer.playWildSound(i,rows-j-1,self.bonusWildisOut[i][rows-j-1])

            if i == cols-1 and j == rows-1:
                self.spinFinished = True

        
        symbol.x -= (symbol.symbolSize-self.tileSize)  / 2
        symbol.y -= (symbol.symbolSize-self.tileSize)  / 2

        if symbol.symbol.name == "wild":
            
            self.soundPlayer.checkIfPlayedWildSound(i,rows-j-1)

            if ((i,rows-j-1)) in self.bonusWildSlots:
                if not self.bonusWildisOut[i][rows-j-1]:
                    
                    if self.spinFinished:
                        self.bonusWildisOut[i][rows-j-1] = True
                        
                        
                else:
                    symbol.x = 93 + i * self.tileSize * 1.35
                    symbol.y = 104 + (rows-j-1)*self.tileSize
                    symbol.x -= (symbol.symbolSize-self.tileSize)  / 2
                    symbol.y -= (symbol.symbolSize-self.tileSize)  / 2
                    screen.blit(symbol.image,[symbol.x,symbol.y])

                    return

        screen.blit(symbol.image,[symbol.x,symbol.y])

    def checkWins(self):
        winners = []
        for line in self.lines:
            if self.isWinner(line):
                winners.append(line)
        self.winLines = winners

    def isWinner(self,line):
        # all symbols in given line
        symbolsInLine = []
        for elem in line.line:
            symbolsInLine.append(self.currentTable[elem[1]][self.slotMachine.rows-elem[0]-1].symbol)
        symbolsInLine = Counter(symbolsInLine).most_common()
        # sort symbol types by amount, so bigger chance for
        sortedSymbols = []
        for doub in symbolsInLine:
            if doub[0].name not in ["wild","scatter"]:
                sortedSymbols.append(doub[0])
        
        for symbol in sortedSymbols:
            
            first = self.currentTable[line.line[0][1]][self.slotMachine.rows-line.line[0][0]-1]
            second = self.currentTable[line.line[1][1]][self.slotMachine.rows-line.line[1][0]-1]
            third = self.currentTable[line.line[2][1]][self.slotMachine.rows-line.line[2][0]-1]
            fourth = self.currentTable[line.line[3][1]][self.slotMachine.rows-line.line[3][0]-1]
            fifth = self.currentTable[line.line[4][1]][self.slotMachine.rows-line.line[4][0]-1]
            
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
                            
                            temp_list.append((line.line[0][1],self.slotMachine.rows-line.line[0][0]-1))
                            temp_list.append((line.line[1][1],self.slotMachine.rows-line.line[1][0]-1))
                            temp_list.append((line.line[2][1],self.slotMachine.rows-line.line[2][0]-1))
                            temp_list.append((line.line[3][1],self.slotMachine.rows-line.line[3][0]-1))
                            temp_list.append((line.line[4][1],self.slotMachine.rows-line.line[4][0]-1))   
                            self.selectedSymbols[line.name] = temp_list
                            return True
                        else:
                            #print(f"X X X X - {symbolName}")
                            temp_list.append((line.line[0][1],self.slotMachine.rows-line.line[0][0]-1))
                            temp_list.append((line.line[1][1],self.slotMachine.rows-line.line[1][0]-1))
                            temp_list.append((line.line[2][1],self.slotMachine.rows-line.line[2][0]-1))
                            temp_list.append((line.line[3][1],self.slotMachine.rows-line.line[3][0]-1)) 
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
                    temp_list.append((line.line[1][1],self.slotMachine.rows-line.line[1][0]-1))
                    temp_list.append((line.line[2][1],self.slotMachine.rows-line.line[2][0]-1))
                    temp_list.append((line.line[3][1],self.slotMachine.rows-line.line[3][0]-1))
                    temp_list.append((line.line[4][1],self.slotMachine.rows-line.line[4][0]-1))  
                    self.selectedSymbols[line.name] = temp_list
                    
                    return True
                else:
                    #print(f"- X X X - {symbolName}")
                    pass
                    

    def countWins(self,screen):
        if len(self.winLines) > 0:
            if not self.isWinCounted:
                self.account.wonAmounts = {}
                
                for line in self.winLines:
                    sum = 0
                    currLine = self.selectedSymbols[line.name]
                    for elem in currLine:       
                        symbol = self.currentTable[elem[0],elem[1]]
                        sum += symbol.symbol.value

                    sum*=self.account.betAmount

                    self.account.wonAmounts[line.name] = round(sum,2)

                if self.bonusOn:
                    self.account.addBonusTotal(self.account.wonAmounts)
                else:
                    self.account.won(self.account.wonAmounts)

                self.isWinCounted = True

        if len(self.account.wonAmounts) > 0:
            self.displayWinCount(screen, self.account.wonAmounts)

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

                    originX = 93 + elem[0] * self.tileSize * 1.35 
                    originY = 105 + (self.slotMachine.rows-elem[1]-1)*self.tileSize

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
                        pygame.draw.rect(tempSurface,pygame.Color(220,20,60),pygame.Rect(1,15,symbol.symbolSize*0.8,symbol.symbolSize*0.8))
                        x = outlineX
                        y = outlineY-20
                    else:
                        pygame.draw.circle(tempSurface,pygame.Color(220,20,60),[symbol.symbolSize*0.5,symbol.symbolSize*0.5],symbol.symbolSize*0.5)
                    screen.blit(tempSurface,(x,y))
                    screen.blit(symbol.image, [originX,originY])

                self.displayLineWin(screen,line)
            

    def displayTextToScreen(self, screen, text, x, y):
        # 1st parameter is the screen to draw on
        # 2nd parameter is the font file
        # 3rd parameter is the text to display
        screen.blit(text, (x, y))

    def displayFreeSpins(self,screen):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Free Spins: {self.freeSpins}",True,"green")
        text_width, text_height = font.size(f"{self.freeSpins} Free Spins")

        x = 780-text_width/2
        y = 700-text_height/2

        self.displayTextToScreen(screen,text,x,y) 

    def displayBonusScreen(self,screen):
        font = pygame.font.Font('freesansbold.ttf', 100)

        # Top text
        top_text = font.render(f"BONUS GAME", True,"green","black")
        text_width, text_height = font.size("Bonus Game")
        x1 = 450-text_width/2
        y1 = 300-text_height/2
        self.displayTextToScreen(screen,top_text,x1,y1)

        # Bottom text
        font = pygame.font.Font('freesansbold.ttf', 60)
        bottom_text = font.render(f"You won {self.freeSpins} free spins!",True,"green","black")
        text_width, text_height = font.size(f"You won {self.freeSpins} free spins!")
        x2 = 500-text_width/2
        y2 = 400-text_height/2

        self.displayTextToScreen(screen,bottom_text,x2,y2)
    
    def displayLineWin(self,screen,line):
        font = pygame.font.Font('freesansbold.ttf', 50)

        text = font.render(f"{self.account.wonAmounts.get(line.name)}", True,"gold","black")
        text_width, text_height = font.size(f"{self.account.wonAmounts.get(line.name)}")
        x = 93 + line.line[2][1] * self.tileSize * 1.35 + self.tileSize/2 - text_width/2
        y = 104 + line.line[2][0] * self.tileSize + self.tileSize/2

        self.displayTextToScreen(screen,text,x,y)
    
    def displayBalance(self,screen):
        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render(f"Balance: {self.account.balance}", True, "black", "gold")
        x = 100
        y = 680

        self.displayTextToScreen(screen,text,x,y)

    def displayBonusTotalWin(self,screen):
        font = pygame.font.Font('freesansbold.ttf', 28)

        if self.bonusOn:
            text = font.render(f"Total Won: {self.account.bonusTotalWin}", True,"gold")
            x = 400
            y = 710

            self.displayTextToScreen(screen,text,x,y)

    def displayWinCount(self,screen, amounts):
        font = pygame.font.Font('freesansbold.ttf', 28)
        
        amount = 0
        for elem in list(amounts.values()):
            amount += elem
        text = font.render(f"Won: {amount}", True,"gold")
        x = 420
        y = 670

        self.displayTextToScreen(screen,text,x,y)

    def spin(self):
        print("Needs to be overwriten 'spin()' ")

    def setLines(self,amount):
        print("Needs to be overwritten: 'setLines(self,amount)'")
