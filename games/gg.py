from model.slotMachine import *
from model.symbols import *
from view.viewSlotMachine import *



class GG(ViewSlotMachine):
    def __init__(self):
        machine = SlotMachine((5,4),34)
        ViewSlotMachine.__init__(self,machine,'assets/background.png',128,"reel",0.38)
        self.loadReels()
        self.slotMachine.setReels(self.reels)

    def spin(self):
        self.slotMachine.spin()

        self.readyToPlaySoundREEL = [False for _ in range(self.slotMachine.dimension[0])]
        self.hasPlayedSoundREEL = [False for _ in range(self.slotMachine.dimension[0])]
        self.readyToPlaySoundWILD = [False for _ in range(self.slotMachine.dimension[0])]
        self.hasPlayedSoundWILD = [False for _ in range(self.slotMachine.dimension[0])]

        self.spinFinished = False
        cols = self.slotMachine.dimension[0]
        rows = self.slotMachine.dimension[1]
        for i in range(cols):
            for j in range(rows):
                currentSymbol = self.slotMachine.getElement(i,j)
                currentViewSymbol = None
                print(currentSymbol.name)
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

                if isinstance(currentSymbol, ScatterSymbol):
                    if currentSymbol.name == "scatter":
                        currentViewSymbol = self.scatter

                self.currentTable[i][rows-j-1] = currentViewSymbol
            print()
        self.animSprite = 0

    def loadReels(self):
    
        ace = ViewFaceSymbol(FaceSymbol("ace",10),"assets/a.png")
        king = ViewFaceSymbol(FaceSymbol("king",10),"assets/k.png")
        queen = ViewFaceSymbol(FaceSymbol("queen",10),"assets/q.png")
        jack = ViewFaceSymbol(FaceSymbol("jack",10),"assets/j.png")
        ten = ViewFaceSymbol(FaceSymbol("ten",10),"assets/10.png")
        crown = ViewFaceSymbol(FaceSymbol("crown",10),"assets/crown.png")
        helmet = ViewFaceSymbol(FaceSymbol("helmet",10),"assets/helmet.png")
        swords = ViewFaceSymbol(FaceSymbol("swords",10),"assets/swords.png")
        wild = ViewWildSymbol(WildSymbol("wild",10),"assets/wild.png")
        scatter = ViewScatterSymbol(ScatterSymbol("scatter",100,None),"assets/throne.png")

        reel1 = [
            ten.symbol,
            ten.symbol,
            ace.symbol,
            queen.symbol,
            jack.symbol,
            king.symbol,
            crown.symbol,
            ten.symbol,
            scatter.symbol,
            ace.symbol,
            helmet.symbol,
            crown.symbol,
            king.symbol,
            crown.symbol,
            helmet.symbol,
            jack.symbol,
            swords.symbol,
            crown.symbol,
            jack.symbol,
            ace.symbol,
            king.symbol,
            wild.symbol,
            ten.symbol,
            helmet.symbol,
            ace.symbol,
            swords.symbol,
            queen.symbol,
            jack.symbol,
            queen.symbol,
            queen.symbol,
            king.symbol,
            swords.symbol,
            king.symbol,
            jack.symbol
        ]
        
        reel2 = [
            queen.symbol,
            jack.symbol,
            king.symbol,
            scatter.symbol,
            jack.symbol,
            ace.symbol,
            ace.symbol,
            ten.symbol,
            swords.symbol,
            crown.symbol,
            swords.symbol,
            wild.symbol,
            crown.symbol,
            wild.symbol,
            wild.symbol,
            crown.symbol,
            king.symbol,
            helmet.symbol,
            helmet.symbol,
            king.symbol,
            ace.symbol,
            ten.symbol,
            ace.symbol,
            queen.symbol,
            queen.symbol,
            king.symbol,
            ten.symbol,
            queen.symbol,
            jack.symbol,
            helmet.symbol,
            swords.symbol,
            jack.symbol,
            jack.symbol,
            king.symbol
        ]

        reel3 = [
            king.symbol,
            jack.symbol,
            queen.symbol,
            queen.symbol,
            jack.symbol,
            ace.symbol,
            ten.symbol,
            crown.symbol,
            queen.symbol,
            crown.symbol,
            jack.symbol,
            ace.symbol,
            jack.symbol,
            helmet.symbol,
            ten.symbol,
            ace.symbol,
            king.symbol,
            crown.symbol,
            helmet.symbol,
            king.symbol,
            ace.symbol,
            queen.symbol,
            ten.symbol,
            helmet.symbol,
            wild.symbol,
            king.symbol,
            swords.symbol,
            scatter.symbol,
            ten.symbol,
            swords.symbol,
            swords.symbol,
            wild.symbol,
            king.symbol,
            jack.symbol
        ]

        reel4 = [
            jack.symbol,
            jack.symbol,
            ten.symbol,
            queen.symbol,
            crown.symbol,
            queen.symbol,
            crown.symbol,
            ace.symbol,
            helmet.symbol,
            ten.symbol,
            helmet.symbol,
            wild.symbol,
            swords.symbol,
            helmet.symbol,
            crown.symbol,
            king.symbol,
            ten.symbol,
            swords.symbol,
            ace.symbol,
            ace.symbol,
            swords.symbol,
            wild.symbol,
            jack.symbol,
            jack.symbol,
            ten.symbol,
            king.symbol,
            king.symbol,
            king.symbol,
            ace.symbol,
            scatter.symbol,
            queen.symbol,
            queen.symbol,
            king.symbol,
            jack.symbol
        ]

        reel5 = [
            wild.symbol,
            wild.symbol,
            jack.symbol,
            queen.symbol,
            jack.symbol,
            crown.symbol,
            crown.symbol,
            crown.symbol,
            ace.symbol,
            ten.symbol,
            king.symbol,
            jack.symbol,
            ten.symbol,
            king.symbol,
            ace.symbol,
            jack.symbol,
            helmet.symbol,
            swords.symbol,
            crown.symbol,
            queen.symbol,
            queen.symbol,
            swords.symbol,
            swords.symbol,
            king.symbol,
            scatter.symbol,
            queen.symbol,
            wild.symbol,
            helmet.symbol,
            helmet.symbol,
            ace.symbol,
            ace.symbol,
            king.symbol,
            jack.symbol,
            king.symbol
        ]

        self.reels = [reel1,reel2,reel3,reel4,reel5]
        self.ace = ace
        self.king = king
        self.queen = queen
        self.jack = jack
        self.ten = ten
        self.wild = wild
        self.scatter = scatter
        self.crown = crown
        self.helmet = helmet
        self.swords = swords