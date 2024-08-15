from model.slotMachine import *
from model.symbols import *
from view.viewSlotMachine import *
from account import *


class GG(ViewSlotMachine):
    def __init__(self):
        machine = SlotMachine((5,4),34+2)
        account = Account(balance=1000,baseBet=1)
        ViewSlotMachine.__init__(self,machine,128,"reel",0.38,account)
        self.loadReels()
        self.slotMachine.setReels(self.reels)
        self.slotMachine.lines = self.setLines(26)
        self.lines = self.setLines(26)

        self.tableBackground = pygame.image.load('assets/background.png')
        self.tableBackground = pygame.transform.scale(self.tableBackground,[910,600])

        self.storyBackground = pygame.image.load('assets/palace.png')
        self.storyBackground = pygame.transform.scale(self.storyBackground,[1500,870])

        self.plusIcon = pygame.image.load('assets/plus.png')
        self.plusIcon = pygame.transform.scale(self.plusIcon,[40,35])

        self.minusIcon = pygame.image.load('assets/minus.png')
        self.minusIcon = pygame.transform.scale(self.minusIcon,[40,35])

        self.spinIcon =  pygame.image.load('assets/spin.png')
        self.spinIcon = pygame.transform.scale(self.spinIcon,[100,100])

        self.soundPlayer.setReelStopSound(pygame.mixer.Sound("assets/reelstop.wav"))
        self.soundPlayer.setWildSound(pygame.mixer.Sound("assets/wild.wav"))

    # - - - - - - - - - - - - - - - - - - I N I T I A L I Z E - - - - - - - - - - - - - - - -

    def setCurrentTable(self):
        for i in range(self.slotMachine.cols):
            for j in range(self.slotMachine.rows):
                
                currentViewSymbol = None
                if ((i,j)) in  self.bonusWildSlots:
                    self.slotMachine.setElement(i,j,self.wild.symbol)
                currentSymbol = self.slotMachine.getElement(i,j)

                if currentSymbol is not None:
                    if isinstance(currentSymbol,FaceSymbol):
                        if currentSymbol.name == "swords":
                            currentViewSymbol = self.swords
                        elif currentSymbol.name == "helmet":
                            currentViewSymbol = self.helmet
                        elif currentSymbol.name == "crown":
                            currentViewSymbol = self.crown
                        elif currentSymbol.name == "ace":
                            currentViewSymbol = self.ace
                        elif currentSymbol.name == "king":
                            currentViewSymbol = self.king
                        elif currentSymbol.name == "queen":
                            currentViewSymbol = self.queen
                        elif currentSymbol.name == "jack":
                            currentViewSymbol = self.jack
                        elif currentSymbol.name == "ten":
                            currentViewSymbol = self.ten
                        

                    if isinstance(currentSymbol,WildSymbol):
                        if currentSymbol.name == "wild":
                            
                            currentViewSymbol = self.wild

                            if (i,j) in self.bonusWildisOut:
                                self.soundPlayer.hasPlayedSoundWILD[i][j] = True   

                            if self.bonusOn and (i,j) not in self.bonusWildSlots:
                                self.bonusWildSlots.append((i,j))
                                self.freeSpins+=1
                                

                    if isinstance(currentSymbol, ScatterSymbol):
                        if currentSymbol.name == "scatter":
                            currentViewSymbol = self.scatter

                self.currentTable[i][self.slotMachine.rows-j-1] = currentViewSymbol

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

    def loadReels(self):
        self.ten = ViewFaceSymbol(FaceSymbol("ten",0.2),"assets/10.png",self.tileSize)
        self.jack = ViewFaceSymbol(FaceSymbol("jack",0.4),"assets/j.png",self.tileSize)
        self.queen = ViewFaceSymbol(FaceSymbol("queen",0.6),"assets/q.png",self.tileSize)
        self.king = ViewFaceSymbol(FaceSymbol("king",0.8),"assets/k.png",self.tileSize)
        self.ace = ViewFaceSymbol(FaceSymbol("ace",1.0),"assets/a.png",self.tileSize)
        self.crown = ViewFaceSymbol(FaceSymbol("crown",1.5),"assets/crown.png",self.tileSize*1.1)
        self.helmet = ViewFaceSymbol(FaceSymbol("helmet",2.0),"assets/helmet.png",self.tileSize*1.1)
        self.swords = ViewFaceSymbol(FaceSymbol("swords",4.0),"assets/swords.png",self.tileSize*1.2)

        self.wild = ViewWildSymbol(WildSymbol("wild",5.0),"assets/wild.png",self.tileSize*1.7)

        self.scatter = ViewScatterSymbol(ScatterSymbol("scatter",100,None),"assets/throne.png",self.tileSize*1.5)

        reel1 = self.createReel(tens=4,jacks=5,queens=4,kings=5,aces=4,crowns=4,helmets=3,swords_s=3,wilds=1,scatters=1)
        reel2 = self.createReel(tens=3,jacks=5,queens=4,kings=5,aces=4,crowns=4,helmets=4,swords_s=3,wilds=1,scatters=1)
        reel3 = self.createReel(tens=4,jacks=5,queens=4,kings=5,aces=4,crowns=3,helmets=3,swords_s=3,wilds=2,scatters=1)
        reel4 = self.createReel(tens=4,jacks=5,queens=4,kings=5,aces=4,crowns=3,helmets=3,swords_s=4,wilds=1,scatters=1)
        reel5 = self.createReel(tens=3,jacks=5,queens=4,kings=5,aces=4,crowns=4,helmets=3,swords_s=3,wilds=2,scatters=1)

        # TEST REELS ---------------------------------
        test_reel1= (reel1).copy()
        test_reel2= (reel2).copy()
        test_reel3= (reel3).copy()
        test_reel4= (reel4).copy()
        test_reel5= (reel5).copy()

        for _ in range(2):
            test_reel1.append(self.scatter.symbol)
            test_reel2.append(self.scatter.symbol)
            test_reel3.append(self.scatter.symbol)
            test_reel4.append(self.scatter.symbol)
            test_reel5.append(self.scatter.symbol)
        
        self.reels = [test_reel1,test_reel2,test_reel3,test_reel4,test_reel5]
        # --------------------------------------------
        # self.reels = [reel1,reel2,reel3,reel4,reel5]

    def createReel(self,tens,jacks,queens,kings,aces,crowns,helmets,swords_s,wilds, scatters):
        reel = []
        reel += [self.ten.symbol] * tens
        reel += [self.jack.symbol] * jacks
        reel += [self.queen.symbol] * queens
        reel += [self.king.symbol] * kings
        reel += [self.ace.symbol] * aces
        reel += [self.crown.symbol] * crowns
        reel += [self.helmet.symbol] * helmets
        reel += [self.swords.symbol] * swords_s
        reel += [self.wild.symbol] * wilds
        reel += [self.scatter.symbol] * scatters
        
        return reel
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


    # - - - - - - - - - - S P I N   L O G I C - - - - - - - - - - 

    def spin(self):
        if self.account.balance < self.account.betAmount:
            print("Insufficient balance to bet")
            return
        
        if self.freeSpins <= 0:
            self.resetBonusValues()
            self.account.addBonusToBalance()
            self.account.bet(self.account.betAmount)
        else:
            self.freeSpins-=1

        self.resetValuesWithSpin()
        self.slotMachine.spin()
        self.setCurrentTable()

        self.account.won(self.account.wonAmount)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


    # - - - - - - - - - - - R E S E T I N G   V A L U E S - - - - - - - - - - -
    def resetValuesWithSpin(self):
        # LOGIC
        self.spinFinished = False
        self.account.wonAmounts = {}

        self.slotMachine.isWinCounted = False
        self.slotMachine.selectedSymbols = {}
        # VISUAL
        self.animSprite = 0
        self.bonusScreen = False
        # SOUND
        self.soundPlayer.resetReelSounds(self.slotMachine.cols,self.slotMachine.rows)
    
    def resetBonusValues(self):
        self.freeSpins = 0
        self.bonusOn = False
        self.bonusWildisOut = [[False]*self.slotMachine.rows for _ in range(self.slotMachine.cols)]
        self.bonusWildSlots = []
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    

    # - - - - - - - - - - - - - - - - - - - V I S U A L - - - - - - - - - - - - - - - - - - - - 

    def slideIn(self,screen, symbol, cols, rows, i ,j):
        if self.type == "reel":
            movingValue = round(self.animSprite*self.tileSize*self.currentSpeed) - (rows*(j-1)*self.tileSize)/rows -((i+1)*cols*self.tileSize)*(4/5)
        elif self.type == "piece":    
            movingValue = self.animSprite*0.8*self.tileSize*self.currentSpeed - (rows*(j-1)*self.tileSize)*(2/5)-((i+3)*cols*self.tileSize)/3


        if  movingValue < (rows-j-1)*self.tileSize:
            symbol.x = self.baseX + i * self.tileSize * 1.35
            symbol.y = self.baseY + movingValue
        else:
            symbol.x = self.baseX + i * self.tileSize * 1.35
            symbol.y = self.baseY + (rows-j-1)*self.tileSize
        
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
                    symbol.x = self.baseX + i * self.tileSize * 1.35
                    symbol.y = self.baseY + (rows-j-1)*self.tileSize
                    symbol.x -= (symbol.symbolSize-self.tileSize)  / 2
                    symbol.y -= (symbol.symbolSize-self.tileSize)  / 2
                    screen.blit(symbol.image,[symbol.x,symbol.y])

                    return

        screen.blit(symbol.image,[symbol.x,symbol.y])
    
    def displayWins(self, screen):
        # DRAW LINES
        if len(self.slotMachine.winLines) > 0:

            line = self.slotMachine.winLines[int((self.animSprite/30) % len(self.slotMachine.winLines))]
            for i in range(len(line.line)-1):
                start = (self.baseX + line.line[i][1] * self.tileSize * 1.35 + self.tileSize/2,
                            self.baseY + line.line[i][0] * self.tileSize + self.tileSize/2)  
                end = (self.baseX + line.line[i+1][1] * self.tileSize * 1.35 + self.tileSize/2,
                            self.baseY + line.line[i+1][0] * self.tileSize + self.tileSize/2)

                pygame.draw.line(screen,"gold",start,end,7)

                # ANIMATE SYMBOLS
                currLine = self.slotMachine.selectedSymbols[line.name]
                for elem in currLine:       
                    symbol = self.currentTable[elem[0],self.slotMachine.rows - elem[1] -1]

                    originX = self.baseX + elem[0] * self.tileSize * 1.35 
                    originY = self.baseY+1 + (elem[1])*self.tileSize

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
    
    def displayBalance(self,screen):
        tempSurface = pygame.Surface((1500,80),pygame.SRCALPHA)
        tempSurface.set_alpha(140)
        pygame.draw.rect(tempSurface,pygame.Color(0,0,0),pygame.Rect(0,0,1500,80))
        screen.blit(tempSurface,(0,870-80))

        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render("BALANCE",False, "white")
        x = self.baseX - 150
        y = 800
        self.displayTextToScreen(screen,text,x,y)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(f"${format(self.account.balance, '.1f')}",False, "gold")
        x = self.baseX - 160
        y = 825
        self.displayTextToScreen(screen,text,x,y)

        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render("BET",False, "white")
        x = self.baseX + 100
        y = 800
        self.displayTextToScreen(screen,text,x,y)

        screen.blit(self.minusIcon,(self.baseX + 30,820))
        screen.blit(self.plusIcon,(self.baseX + 170,820))

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(f"${format(self.account.betAmount, '.1f')}",False, "gold")
        x = self.baseX + 90
        y = 825
        self.displayTextToScreen(screen,text,x,y)
        
        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render("WIN",False, "white")
        x = self.baseX + 800
        y = 800
        self.displayTextToScreen(screen,text,x,y)

        screen.blit(self.spinIcon,(705,760))

    def displayWinCount(self,screen, amounts):
        amount = 0
        for elem in list(amounts.values()):
            amount += elem

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(f"${format(amount, '.1f')}",False, "gold")
        x = self.baseX +790
        y = 825
        self.displayTextToScreen(screen,text,x,y)

    def displayBonusTotalWin(self,screen):

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(f"${format(self.account.bonusTotalWin, '.1f')}",False, "gold")
        x = self.baseX +790
        y = 825
        self.displayTextToScreen(screen,text,x,y)
    
    def displayLineWin(self,screen,line):
        font = pygame.font.Font('freesansbold.ttf', 50)

        text = font.render(f"{format(self.account.wonAmounts.get(line.name),'.1f')}", True,"gold","black")
        text_width, text_height = font.size(f"{format(self.account.wonAmounts.get(line.name),'.1f')}")
        x = self.baseX + line.line[2][1] * self.tileSize * 1.35 + self.tileSize/2 - text_width/2
        y = self.baseY + line.line[2][0] * self.tileSize + self.tileSize/2

        self.displayTextToScreen(screen,text,x,y)

    def displayBonusScreen(self,screen):
        font = pygame.font.Font('freesansbold.ttf', 100)

        # Top text
        top_text = font.render(f"BONUS GAME", True,"green","black")
        text_width, text_height = font.size("Bonus Game")
        x1 = self.baseX + 450-text_width/2
        y1 = 300-text_height/2
        self.displayTextToScreen(screen,top_text,x1,y1)

        # Bottom text
        font = pygame.font.Font('freesansbold.ttf', 60)
        bottom_text = font.render(f"You won {self.freeSpins} free spins!",True,"green","black")
        text_width, text_height = font.size(f"You won {self.freeSpins} free spins!")
        x2 = self.baseX + 500-text_width/2
        y2 = 400-text_height/2

        self.displayTextToScreen(screen,bottom_text,x2,y2)
    
    def displayFreeSpins(self,screen):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Free Spins: {self.freeSpins}",True,"green")
        text_width, text_height = font.size(f"{self.freeSpins} Free Spins")

        x = self.baseX + 780-text_width/2
        y = 700-text_height/2

        self.displayTextToScreen(screen,text,x,y) 
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
