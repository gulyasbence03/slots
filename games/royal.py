from model.slotMachine import *
from model.symbols import *
from view.viewSlotMachine import *
from account import *


class GG(ViewSlotMachine):
    def __init__(self):
        machine = SlotMachine((5,4),34+2)
        account = Account(1000)
        ViewSlotMachine.__init__(self,machine,'assets/background.png',128,"reel",0.38,account)
        self.loadReels()
        self.slotMachine.setReels(self.reels)

        self.soundPlayer.setReelStopSound(pygame.mixer.Sound("assets/reelstop.wav"))
        self.soundPlayer.setWildSound(pygame.mixer.Sound("assets/wild.wav"))

    def resetValuesWithSpin(self):
        # LOGIC
        self.spinFinished = False
        self.account.wonAmounts = {}
        self.isWinCounted = False
        self.selectedSymbols = {}
        # VISUAL
        self.animSprite = 0
        self.bonusScreen = False
        # SOUND
        self.soundPlayer.resetReelSounds(self.slotMachine.dimension[0],self.slotMachine.dimension[1])
    
    def resetBonusValues(self):
        self.freeSpins = 0
        self.bonusOn = False
        self.bonusWildisOut = [[False]*self.slotMachine.dimension[1] for _ in range(self.slotMachine.dimension[0])]
        self.bonusWildSlots = []

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

    def setCurrentTable(self):
        cols = self.slotMachine.dimension[0]
        rows = self.slotMachine.dimension[1]
        for i in range(cols):
            for j in range(rows):
                
                currentViewSymbol = None
                if ((i,j)) in  self.bonusWildSlots:
                    currentSymbol = self.wild.symbol
                else:
                    currentSymbol = self.slotMachine.getElement(i,j)

                if currentSymbol is not None:
                    #print(currentSymbol.name)
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

                self.currentTable[i][rows-j-1] = currentViewSymbol

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
        # --------------------------------------------
        self.reels = [test_reel1,test_reel2,test_reel3,test_reel4,test_reel5]

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
    