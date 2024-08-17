class Line:
    def __init__(self, name, line):
        self.name = name
        self.line = line

import pygame 

class Button(object): 
    def __init__(self,position,size,filename): 

        # load image 
        self.image = pygame.image.load(filename) 

        # resize button 
        self.image = pygame.transform.scale(self.image,size) 

        # create collision box and set position 
        self.rect = self.image.get_rect(topleft=position)

    def draw(self,surface):
        surface.blit(self.image,self.rect)
     
    def check_press(self,position):
        if self.rect.collidepoint(*position):
            return True
        return False