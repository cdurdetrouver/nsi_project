from turtle import speed
import pygame

from script.game.projectile import Projectile 
from script.game.meteorite import Pluie_Meteorite
from script.game.life import Life

class Fusee():
    # cette class gere la fusee
    def __init__(self, pos, screen_size, game, score):
        self.screen_size = screen_size
        self.sprite = pygame.image.load("image/fusee.png") # charger l'image de la fusee 
        self.image_size = self.sprite.get_size() # taille de l'image 
        self.sprite = pygame.transform.scale(self.sprite, (self.screen_size[0] * 0.085, self.screen_size[0] * 0.085 * self.image_size[1]/self.image_size[0]))
        self.rect = self.sprite.get_rect()
        self.image_size = self.sprite.get_size() # taille de l'image final
        self.pos = [pos[0] - (self.image_size[0]/2), pos[1]] # position de la fusee

        self.speed = screen_size[0] / 60 / 2 # pour déplacer la fusee en 2 secondes sur la taille x de l'écran

        self.proj = Projectile(self, screen_size)

        self.life = Life(3, self.screen_size, game, self)

        self.pluie = Pluie_Meteorite(self.screen_size, self, score)


    def get_life(self):
        return self.life

    #fonctions de collisions
    def collision(self):
        if self.pos[1] > self.screen_size[1]  - self.image_size[1]:
            self.pos[1] = self.screen_size[1] - self.image_size[1]
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[0] > self.screen_size[0] - self.image_size[0]:
            self.pos[0] = self.screen_size[0] - self.image_size[0]
        if self.pos[0] < 0:
            self.pos[0] = 0

    #fonctions de deplacements
    def up(self):
        # deplacement de la fusee vers le haut
        self.pos[1] -= self.speed
    
    def down(self):
        # deplacement de la fusee vers le bas
        self.pos[1] += self.speed
    
    def right(self):
        # deplacement de la fusee vers la droite
        self.pos[0] += self.speed
    
    def left(self):
        # deplacement de la fusee vers la gauche
        self.pos[0] -= self.speed

    # fonctions d'affichage
    def afficher(self,screen):
        # update du rect
        self.rect = pygame.Rect.fit(self.rect, (self.pos[0],self.pos[1], self.rect.width, self.rect.height))

        #affichage des météorites
        self.pluie.afficher(screen)

        # affichage de la fusee
        self.collision()
        self.proj.afficher(screen)
        screen.blit(self.sprite,(self.pos[0],self.pos[1]))
        pygame.draw.rect(screen, (255,0,0), self.rect, 1)

  