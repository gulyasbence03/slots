class Symbol:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class FaceSymbol(Symbol):
    def __init__(self,name, value):
        Symbol.__init__(self,name, value)

class ScatterSymbol(Symbol):
    def __init__(self,name, value, bonusGame):
        Symbol.__init__(self,name, value)
        self.bonusGame = bonusGame

class WildSymbol(Symbol):
    def __init__(self,name, value):
        Symbol.__init__(self,name, value)
