class Account:
    def __init__(self,balance):
        self.balance = balance
        self.wonAmount = 0
        self.betAmount = 10
        self.bonusTotalWin = 0
    
    def changeBetAmount(self,bet):
        if bet > 0:
            self.betAmount = bet

    def bet(self,amount):
        if self.balance-amount < 0:
            print("Insufficient balance to bet")
        else:
            self.balance-=amount
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
            self.balance += self.bonusTotalWin
        self.bonusTotalWin = 0

    def deposit(amount):
        pass