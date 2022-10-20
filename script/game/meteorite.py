import pygame
import random

class Meteorite():
    # cette class gere les meteorites qui tombent du ciel
    def __init__(self,x,y, screensize):
        self.screensize = screensize

        self.sprite = pygame.image.load("image/Meteor.png")
        self.sprite = pygame.transform.scale(self.sprite,(x,y))

        x = random.randint(0,screensize[0])
        y = 0 - self.sprite.get_size()[1]
        self.pos = [x,y]
        self.coef = random.randint(0, -10)


    def update_position(self):
        pass
    
    
    def afficher(self,screen):
        # affichage de la meteorite
        screen.blit(self.sprite,(self.pos[0],self.pos[1]))
    
