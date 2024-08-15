import numpy as np
from model.symbols import *
import secrets
from collections import Counter

class SlotMachine:
    def __init__(self,dimension,symbolsOnReel):
        self.symbolsOnReel = symbolsOnReel
        self.cols = dimension[0]
        self.rows = dimension[1]

        self.reels = np.empty((self.cols,symbolsOnReel),dtype=Symbol)
        self.table = np.empty(dimension,dtype=Symbol)

        self.lines = None
        self.winLines = None

        self.selectedSymbols = {}
        self.isWinCounted = False

        self.freeSpins = 0

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
    
    def checkWins(self):
        if not self.isWinCounted:
            if self.lines == None:
                print("SlotMachine lines not initialized")
            else:
                winners = []
                for line in self.lines:
                    if self.isWinner(line):
                        winners.append(line)
                self.winLines = winners

    def isWinner(self,line):
        # all symbols in given line
        symbolsInLine = []
        for elem in line.line:
            symbolsInLine.append(self.table[elem[1]][elem[0]].name)
        

        
        symbolsInLine = Counter(symbolsInLine).most_common()
        # sort symbol types by amount, so bigger chance for
        sortedSymbols = []
        for elem in symbolsInLine:
            key = elem[0]
            if key not in ["wild","scatter"]:
                sortedSymbols.append(key)


        
        for symbol in sortedSymbols:
            
            first = self.table[line.line[0][1]][line.line[0][0]].name
            second = self.table[line.line[1][1]][line.line[1][0]].name
            third = self.table[line.line[2][1]][line.line[2][0]].name
            fourth = self.table[line.line[3][1]][line.line[3][0]].name
            fifth = self.table[line.line[4][1]][line.line[4][0]].name


            # RULES

            temp_list = []
            if first in [symbol,"wild"]:
                # first 3 symbol or wild (X X X any any)
                if second in [symbol,"wild"] and third in [symbol,"wild"]:
                    # first 4 symbol or wild (X X X X any)
                    if fourth in [symbol,"wild"]:
                        # first 5 symbol or wild (X X X X X)
                        if fifth in [symbol,"wild"]:
                            #print(f"X X X X X {symbolName}")
                            
                            temp_list.append((line.line[0][1],line.line[0][0]))
                            temp_list.append((line.line[1][1],line.line[1][0]))
                            temp_list.append((line.line[2][1],line.line[2][0]))
                            temp_list.append((line.line[3][1],line.line[3][0]))
                            temp_list.append((line.line[4][1],line.line[4][0]))  

                            self.selectedSymbols[line.name] = temp_list
                            return True
                        else:
                            #print(f"X X X X - {symbolName}")
                            temp_list.append((line.line[0][1],line.line[0][0]))
                            temp_list.append((line.line[1][1],line.line[1][0]))
                            temp_list.append((line.line[2][1],line.line[2][0]))
                            temp_list.append((line.line[3][1],line.line[3][0])) 
                            self.selectedSymbols[line.name] = temp_list
                            return True
                    else:
                        #print(f"X X X - - {symbolName}")
                        pass
                    
            
            #first X next continous 3 symbol or wild (any X X X any)
            elif second in [symbol,"wild"] and third in [symbol,"wild"] and fourth in [symbol,"wild"]:
                # first 5 symbol or wild
                if fifth in [symbol,"wild"]:
                    #print(f"- X X X X {symbolName}")
                    temp_list.append((line.line[1][1],line.line[1][0]))
                    temp_list.append((line.line[2][1],line.line[2][0]))
                    temp_list.append((line.line[3][1],line.line[3][0]))
                    temp_list.append((line.line[4][1],line.line[4][0]))  
                    self.selectedSymbols[line.name] = temp_list
                    return True
                else:
                    #print(f"- X X X - {symbolName}")
                    pass
            
    def countWins(self, account, bonusOn):
        if len(self.winLines) > 0:
            if not self.isWinCounted:
                account.wonAmounts = {}
                
                for line in self.winLines:
                    sum = 0
                    currLine = self.selectedSymbols[line.name]
                    for elem in currLine:       
                        symbol = self.table[elem[0],elem[1]]
                        sum += symbol.value

                    sum*=account.betAmount

                    account.wonAmounts[line.name] = round(sum,2)
               
                if bonusOn:
                    account.addBonusTotal(account.wonAmounts)
                else:
                    account.won(account.wonAmounts)

                self.isWinCounted = True
    