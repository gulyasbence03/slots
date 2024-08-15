import numpy as np
from model.symbols import FaceSymbol,WildSymbol,ScatterSymbol
from view.viewSymbol import *
from collections import Counter
from view.line import *
from sound import *

class ViewSlotMachine:
    def __init__(self,slotMachine,tileSize, type, speed, account):
        # LOGIC
        self.slotMachine = slotMachine
        self.account = account
        self.lines = None
    
        # Visual
        self.tileSize = tileSize
        self.type = type
        self.defaultSpeed = speed
        self.currentSpeed = speed
        self.animSprite = 0
        self.currentTable = np.zeros((slotMachine.cols,slotMachine.rows), dtype=ViewSymbol)
        self.spinFinished = True
        self.baseX = (1500 - 910) / 2 + 48
        self.baseY = 150
        self.tableBackground = None
        self.storyBackground = None

        # Sound
        self.soundPlayer = SoundPlayer(slotMachine.cols,slotMachine.rows)

        # Bonusgame
        self.bonusOn = False
        self.bonusScreen = False
        self.freeSpins = 0
        self.bonusWildSlots = []
        self.bonusWildisOut = [[False]*slotMachine.rows for _ in range(slotMachine.cols)]

    def clearScreen(self,screen):
        screen.blit(self.storyBackground,[0,0])
        screen.blit(self.tableBackground,[self.baseX - 47,self.baseY - 40])

    def display(self, screen):
        self.clearScreen(screen)
        self.displayBalance(screen)
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
            self.slotMachine.checkWins()
            self.slotMachine.countWins(self.account, self.bonusOn)
            
            numberOfScatters = self.slotMachine.checkBonus(self.bonusOn)
            if numberOfScatters >= 3:
                self.bonusScreen = True
                self.bonusOn = True
                self.freeSpins = numberOfScatters

            self.displayWins(screen)

            if not self.bonusOn:
                self.displayWinCount(screen, self.account.wonAmounts)
        
        if self.bonusOn:
            self.displayFreeSpins(screen)
            self.displayBonusTotalWin(screen)
        

        return not self.spinFinished

    def spin(self):
        # The logic behind what should happen at each spin, reseting values etc.
        raise NotImplementedError("Subclasses should implement this method: 'spin(self)'")
    
    def displayTextToScreen(self, screen, text, x, y):
        # 1st parameter is the screen to draw on
        # 2nd parameter is the text to display
        # x and y coordinates to draw to on screen
        screen.blit(text, (x, y))

    def displayFreeSpins(self,screen):
        # Display number of free spins left in the bonus
        raise NotImplementedError("Subclasses should implement this method: 'displayFreeSpins(self,screen)'")

    def displayBonusScreen(self,screen):
        # Display bonus screen before bonus starts, bonus starts next spin
        raise NotImplementedError("Subclasses should implement this method: 'displayBonusScreen(self,screen)'")
    
    def displayLineWin(self,screen,line):
        # Display a line showing which line is winning
        raise NotImplementedError("Subclasses should implement this method: 'displayLineWin(self,screen,line)'")

    def displayBonusTotalWin(self,screen):
        # Display how much total win is collected in the bonus game
        raise NotImplementedError("Subclasses should implement this method: 'displayBonusTotalWin(self,screen)'")

    def displayWinCount(self,screen, amounts):
        # Display how much the current spin has won
        raise NotImplementedError("Subclasses should implement this method: 'displayWinCount(self,screen, amounts)'")

    def setLines(self,amount):
        raise NotImplementedError("Subclasses should implement this method: 'setLines(self,amount)'")

    def slideIn(self,screen, symbol, cols, rows, i ,j):
        raise NotImplementedError("Subclasses should implement this method: 'slideIn(self,screen, symbol, cols, rows, i ,j)'")

    def displayWins(self, screen):
        raise NotImplementedError("Subclasses should implement this method: 'displayWins(self, screen)'")

    def displayBalance(self,screen):
        raise NotImplementedError("Subclasses should implement this method: 'displayBalance(self,screen)'")
    