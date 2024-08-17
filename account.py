class Account:
    def __init__(self,balance, baseBet):
        self.balance = balance
        self.wonAmount = 0
        self.betSizes = [0.25,0.5,1,2,5,10,25,50,100,250,500,1000]
        self.betIdx = baseBet
        self.betAmount = self.betSizes[self.betIdx]
        self.bonusTotalWin = 0

    
    def increaseBet(self):
        if self.betIdx + 1 > len(self.betSizes) - 1:
            return
        self.betIdx+=1
        self.betAmount = self.betSizes[self.betIdx]

    def lowerBet(self):
        if self.betIdx - 1 < 0:
            return
        self.betIdx-=1
        self.betAmount = self.betSizes[self.betIdx]

    def bet(self,amount):
        if self.balance-amount < 0:
            print("Insufficient balance to bet")
        else:
            self.balance -= amount
            self.balance = round(self.balance,2)

    def won(self,wonAmount):
        if bool(wonAmount):
            for elem in list(wonAmount.values()):
                self.balance += round(elem,2)

    def addBonusTotal(self,wonAmount):
        if bool(wonAmount):
            for elem in list(wonAmount.values()):
                self.bonusTotalWin += round(elem,2)

    def addBonusToBalance(self):
        if self.bonusTotalWin > 0:
            self.balance += round(self.bonusTotalWin,2)
        self.bonusTotalWin = 0

    def deposit(amount):
        pass