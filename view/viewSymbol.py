from abc import ABC, abstractmethod
import pygame

class ViewSymbol:
    def __init__(self, symbol, imagePath, symbolSize):
        self.symbol = symbol
        self.image = pygame.image.load(imagePath)
        self.isSelected = False
        self.symbolSize = symbolSize
        self.x = 0
        self.y = 0

class AnimatedSymbol(ABC):
    @abstractmethod
    def animation():
        pass

class ViewFaceSymbol(ViewSymbol):
    def __init__(self,symbol,imagePath, symbolSize):
        ViewSymbol.__init__(self,symbol,imagePath, symbolSize)

class ViewScatterSymbol(ViewSymbol):
    def __init__(self,symbol, imagePath, symbolSize):
        ViewSymbol.__init__(self,symbol, imagePath, symbolSize)

class ViewWildSymbol(ViewSymbol):
    def __init__(self,symbol,imagePath, symbolSize):
        ViewSymbol.__init__(self,symbol,imagePath, symbolSize)

