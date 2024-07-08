from PIL import Image,ImageTk

class Symbol:
    def __init__(self, value):
        self.value = value

class FaceSymbol(Symbol):
    def __init__(self,value):
        Symbol.__init__(self,value)

class ScatterSymbol(Symbol):
    def __init__(self,value, bonusGame):
        Symbol.__init__(self,value)
        self.bonusGame = bonusGame

class WildSymbol(Symbol):
    def __init__(self,value):
        Symbol.__init__(self,value)
