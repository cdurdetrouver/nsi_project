from turtle import speed
import pygame

from script.game.projectile import Projectile 

class Fusee():
    # cette class gere la fusee
    def __init__(self, pos, screen_size, game):
        self.screen_size = screen_size
        self.sprite = pygame.image.load("image/fusee.png") # charger l'image de la fusee 
        self.image_size = self.sprite.get_size() # taille de l'image 
        self.sprite = pygame.transform.scale(self.sprite, (self.screen_size[0] * 0.085, self.screen_size[0] * 0.085 * self.image_size[1]/self.image_size[0]))
        self.image_size = self.sprite.get_size() # taille de l'image final
        self.pos = [pos[0] - (self.image_size[0]/2), pos[1]] # position de la fusee

        self.speed = screen_size[0] / 60 / 2

        self.proj = Projectile(self, screen_size)

        self.life = Life(3, self.screen_size, game)


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
        # affichage de la fusee
        self.collision()
        self.proj.afficher(screen)
        screen.blit(self.sprite,(self.pos[0],self.pos[1]))


class Life():
    def __init__(self, life, screen_size, game):
        self.life = life
        self.game = game

        self.screen_size = screen_size
        self.heart = pygame.image.load("image/heart.png") # charger l'image du boutton

        self.heart_size = self.heart.get_size() # taille de l'image pour la reduction
        self.heart = pygame.transform.scale(self.heart, (self.screen_size[0] * 0.05, self.screen_size[0] * 0.05))
        self.heart_size = self.heart.get_size() # taille de l'image final

        self.empty_heart = pygame.image.load("image/empty_heart.png")

        self.empty_heart_size = self.empty_heart.get_size() # taille de l'image pour la reduction
        self.empty_heart = pygame.transform.scale(self.empty_heart, (self.screen_size[0] * 0.05, self.screen_size[0] * 0.05))
        self.empty_heart_size = self.empty_heart.get_size() # taille de l'image final

        self.pos = [self.screen_size[0] * 3 / 100 - (self.heart_size[0]/2), self.screen_size[0] * 3 / 100 - (self.heart_size[1]/2)]

    def lost_life(self):
        self.life -= 1
        if self.life == 0:
            self.game.game_over()

    def afficher(self, screen):
        taille = 0
        for i in range(self.life):
            screen.blit(self.heart, (self.pos[0] * (i+1) + self.heart_size[0] * i, self.pos[1]))
            taille = i + 1
        for j in range(3 - self.life):
            screen.blit(self.empty_heart, (self.pos[0] * (taille + j + 1) + self.empty_heart_size[0] * (taille + j), self.pos[1]))
        