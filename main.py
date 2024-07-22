from model.slotMachine import *
from model.symbols import *
from view.viewSlotMachine import *
import sys
import pygame

from games.gg import *

class Game:
    def __init__(self, slot, fps):
        self.slot = slot
        self.spinLock = False
        self.fps = fps
        pygame.init()
        self.screen = pygame.display.set_mode((1000,900))
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
                    if event.key == pygame.K_m:
                        if self.slot.mute == False:
                            self.slot.mute = True
                        else:
                            self.slot.mute = False
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
            
slot = GG()
Game(slot,60).run()