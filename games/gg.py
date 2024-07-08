from model.slotMachine import *
from model.symbols import *
from view.viewSlotMachine import *



class GG(ViewSlotMachine):
    def __init__(self):
        machine = SlotMachine((5,4),8)
        ViewSlotMachine.__init__(self,machine,'assets/background.png',128,"reel",0.38)
        self.loadReels()
        self.slotMachine.setReels(self.reels)

    def loadReels(self):
        
        clubs = ViewFaceSymbol(FaceSymbol("clubs",10),"assets/clubs.png")
        hearts = ViewFaceSymbol(FaceSymbol("hearts",10),"assets/hearts.png")
        diamonds = ViewFaceSymbol(FaceSymbol("diamonds",10),"assets/diamonds.png")
        spades = ViewFaceSymbol(FaceSymbol("spades",10),"assets/spades.png")

        reel1 = [clubs.symbol,
                 clubs.symbol,
                 clubs.symbol,
                 clubs.symbol,
                 hearts.symbol,
                 hearts.symbol,
                 hearts.symbol,
                 hearts.symbol]
        
        reel2 = [diamonds.symbol,
                 diamonds.symbol,
                 diamonds.symbol,
                 diamonds.symbol,
                 spades.symbol,
                 spades.symbol,
                 spades.symbol,
                 spades.symbol]

        self.reels = [reel1,reel2,reel1,reel2,reel2]
        self.clubs = clubs
        self.hearts = hearts
        self.diamonds = diamonds
        self.spades = spades
    
    def spin(self):
        self.slotMachine.spin()
        self.spinFinished = False
        cols = self.slotMachine.dimension[0]
        rows = self.slotMachine.dimension[1]
        for i in range(cols):
            for j in range(rows):
                currentSymbol = self.slotMachine.getElement(i,j)
                currentViewSymbol = None
                print(currentSymbol.name)
                if isinstance(currentSymbol,FaceSymbol):
                    if currentSymbol.name == "clubs":
                        currentViewSymbol = self.clubs
                    elif currentSymbol.name == "hearts":
                        currentViewSymbol = self.hearts
                    elif currentSymbol.name == "diamonds":
                        currentViewSymbol = self.diamonds
                    elif currentSymbol.name == "spades":
                        currentViewSymbol = self.spades

                self.currentTable[i][rows-j-1] = currentViewSymbol
            print()
        self.animSprite = 0