from turtle import Screen
import pygame
from pygame.locals import *
from script.score import Score
from script.fusee import Fusee

class Game():
    # cette class correspond à la celle qui gere tout le jeux
    def __init__(self, size, title, FPS):

        self.size = (size[0], size[1])
        self.window = pygame.display.set_mode(self.size) # creer la fenetre avec des dimensions donnees
        pygame.display.set_caption(title) # definir le titre
        self.fps = FPS
        self.running = True

        # appel des objets
        self.fusee = Fusee((0,0))
        self.score = Score((690,10))

        # affichage du background
        self.background = pygame.image.load("image/background.jpg")
        self.background = pygame.transform.scale(self.background,(720,480))

        # preparer au fps
        self.clock = pygame.time.Clock() 
       

    def handle_input(self):
        # recuperer les touches pressees 
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.destroy()
        elif pressed[pygame.K_UP]:
            self.fusee.up(3)
        elif pressed[pygame.K_DOWN]:
            self.fusee.down(3)
        elif pressed[pygame.K_RIGHT]:
            self.fusee.right(3)
        elif pressed[pygame.K_LEFT]:
            self.fusee.left(3)

    def update(self):
        # update d'affichage
        self.window.blit(self.background,(0,0)) # afficher le background
        self.fusee.afficher(self.window) # afficher la fusee
        self.score.afficher(self.window) # afficher le score

    def run(self):
        # boucle qui gere le jeu
        while self.running:

            self.handle_input() # gere entre de touche

            self.update() # gere l'affichage des objets

            pygame.display.flip() # actualiser l'ecran

            for event in pygame.event.get(): # regarder si la fenetre se ferme
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(self.fps) # gere les fps
        pygame.quit() # arreter pygame

    def destroy(self):
        # fermeture de la fenetre 
        print("bye") # afficher bye parce que c'est marrant
        pygame.quit() # arreter pygame
        exit() # arrreter tous les programmes en cours