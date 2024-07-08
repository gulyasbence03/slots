from model.slotMachine import *
from model.symbols import *
from view.viewSlotMachine import *
import sys
import pygame

class Game:
    def __init__(self, slot, fps):
        self.slot = slot
        self.spinLock = False
        self.fps = fps
        pygame.init()
        self.screen = pygame.display.set_mode((800,900))
        pygame.display.set_caption("CrazySlot")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.setSpinLock()
                        if not self.spinLock:
                            self.slot.spin()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.setSpinLock()
                    if not self.spinLock:
                        self.slot.spin()
                            
                            

            self.spinLock = self.slot.display(self.screen)
            self.slot.animSprite+= self.slot.slotMachine.dimension[0]/8
            pygame.display.update()

    def setSpinLock(self):
        if self.spinLock == True:
            self.slot.currentSpeed = self.slot.defaultSpeed *2
        else:
            self.slot.currentSpeed = self.slot.defaultSpeed
            

machine = SlotMachine((5,5),20)
reel1 = [FaceSymbol(10),FaceSymbol(10),FaceSymbol(10),FaceSymbol(10),FaceSymbol(10),
         FaceSymbol(10),WildSymbol(10),WildSymbol(10),WildSymbol(10),FaceSymbol(10),
         FaceSymbol(10),FaceSymbol(10),FaceSymbol(10),FaceSymbol(10),FaceSymbol(10),
         ScatterSymbol(10,None),ScatterSymbol(10,None),ScatterSymbol(10,None),FaceSymbol(10),WildSymbol(10)]

reels = [reel1 for _ in range(5)]
machine.setReels(reels)
viewSlotMachine = ViewSlotMachine(machine,'white',120, "reel",0.4)

Game(viewSlotMachine,60).run()