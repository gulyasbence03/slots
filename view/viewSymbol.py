from abc import ABC, abstractmethod
import pygame

class ViewSymbol:
    def __init__(self, symbol, imagePath):
        self.symbol = symbol
        self.image = pygame.image.load(imagePath).convert()
        self.isSelected = False
        self.x = 0
        self.y = 0

class AnimatedSymbol(ABC):
    @abstractmethod
    def animation():
        pass

class ViewFaceSymbol(ViewSymbol):
    def __init__(self,symbol,imagePath):
        ViewSymbol.__init__(self,symbol,imagePath)

class ViewScatterSymbol(ViewSymbol):
    def __init__(self,symbol, imagePath):
        ViewSymbol.__init__(self,symbol, imagePath)

class ViewWildSymbol(ViewSymbol):
    def __init__(self,symbol,imagePath):
        ViewSymbol.__init__(self,symbol,imagePath)
