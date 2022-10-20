import pygame
from pygame.locals import *
from script.game.fusee import Fusee
from script.UI.ui import UI

class Game():
    # cette class correspond à la celle qui gere tout le jeux
    def __init__(self, size, title):
        self.size = size
        self.window = pygame.display.set_mode(self.size, pygame.FULLSCREEN) # creer la fenetre avec des dimensions donnees
        pygame.display.set_caption(title) # definir le titre
        self.fps = 60
        self.running = True

        surf = pygame.Surface((40,40),pygame.SRCALPHA)
        self.cursors = [
            pygame.cursors.Cursor((24, 24), (0, 0), *pygame.cursors.compile(pygame.cursors.thickarrow_strings)),
            pygame.cursors.Cursor((24, 24), surf)
        ] # liste des diff&rents cursor
        pygame.mouse.set_cursor(self.cursors[0])

        self.already = False # est-ce que la barre espace est enfonce

        # affichage du background
        self.new_screen(self.size)

        # preparer au fps
        self.clock = pygame.time.Clock()

        # menu de jeux
        self.menu = True

        # menu parametre
        self.parameter = False

        # police d'ecriture
        pygame.font.init()
        self.police = pygame.font.SysFont("font/font.ttf", 256) # police d'ecriture

        self.UI = UI(self.size, self) # creation de l'interface utilisateur
        self.score = self.UI.get_score()
        self.button_start = self.UI.get_button_start()
        self.button_parameter = self.UI.get_button_parameter()


    def new_screen(self, screen_size):
        
        self.screen = pygame.display.set_mode(screen_size)

        self.size = screen_size

        # appel des images de background 
        self.background = pygame.image.load("image/background.jpg")
        self.background_blur = pygame.image.load("image/background_blur.jpg")

        # calcul de la taille de l'image de fond en fonction de la taille de l'ecran
        self.background_size = self.background.get_size() # taille du fond d'ecran
        aug = screen_size[1] / self.background_size[1] # taux d'augmentation
        self.background = pygame.transform.scale(self.background,(self.background_size[0] * aug, screen_size[1])) #redimension
        self.background_blur = pygame.transform.scale(self.background_blur,(self.background_size[0] * aug, screen_size[1])) #redimension
        self.background_size = self.background.get_size() # taille du fond d'ecran apres redimensionnement

        # appel des objets
        self.UI = UI(self.size, self) # creation de l'interface utilisateur
        self.score = self.UI.get_score()
        self.button_start = self.UI.get_button_start()
        self.button_parameter = self.UI.get_button_parameter()

    def handle_input(self, pressed):

        if pressed[pygame.K_ESCAPE]: 
            self.destroy() # arreter le jeu
        if pressed[pygame.K_DELETE]:
            self.menu = True # retourner au menu d'acceuil
            pygame.mouse.set_cursor(self.cursors[0]) # cursor non-transparent

        if pressed[pygame.K_p]:
            self.new_screen((1000,500))

        # pas d'autre touche si on est sur le menu
        if self.menu:
            return

        if pressed[pygame.K_UP]:
            self.fusee.up(8) # deplacer la fusee en haut
        if pressed[pygame.K_DOWN]:
            self.fusee.down(8) # deplacer la fusee en bas
        if pressed[pygame.K_RIGHT]:
            self.fusee.right(8) # deplacer la fusee sur la droite
        if pressed[pygame.K_LEFT]:
            self.fusee.left(8) # deplacer la fusee sur la gauche
        
        if pressed[pygame.K_SPACE]:
            if not self.already:
                return
            else: 
                self.fusee.proj.launch_x()
                self.already = False
        else:
            self.already = True
        

    def update(self):
        # update d'affichage
        if self.menu :
            self.window.blit(self.background_blur,(0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.UI.afficher(self.window, "menu") # afficher le score + le boutton jouer
        elif self.parameter:
            self.window.blit(self.background_blur,(0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.UI.afficher(self.window, "parameter") # afficher le menu parametre
        else :
            self.window.blit(self.background,(0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.fusee.afficher(self.window) # afficher la fusee
            self.UI.afficher(self.window, "game") # afficher le score

    def start_game(self):
        pygame.mouse.set_cursor(self.cursors[1]) # cursor transparent

        # transision entre l'ecran de menu et de jeux 
        for i in range(3, 0, -1):
            self.image_text = self.police.render( f"{i}", True , (255,255,255) ) # image du decompte ("texte a afficher", couleur?, couleur)
            self.window.blit(self.background, (0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.window.blit(self.image_text, (self.size[0]/2 - self.image_text.get_size()[0]/2, self.size[1]/2 - self.image_text.get_size()[1]/2))
            pygame.display.flip()
            pygame.time.wait(1000)

        self.fusee = Fusee((self.size[0]/2,self.size[1]), self.size) # appel la fusee
        self.score.reset()
       
    def run(self):
        # boucle qui gere le jeu
        while self.running:
            # recuperer les touches pressees 
            pressed = pygame.key.get_pressed()

            self.handle_input(pressed) # gere entre de touche

            self.update() # gere l'affichage des objets

            pygame.display.flip() # actualiser l'ecran

            for event in pygame.event.get(): # regarder si la fenetre se ferme
                if event.type == pygame.QUIT:
                    self.running = False
                
                if not(self.menu) and not(self.parameter):
                    break

                if event.type == MOUSEBUTTONDOWN:
                    if self.menu:
                        if self.button_start.on():
                            self.start_game()
                            self.menu = False; self.parameter = False
                        if self.button_parameter.on():
                            self.menu = False; self.parameter = True
                    else:
                            self.UI.menu_click_button()

            self.clock.tick(self.fps) # gere les fps
        pygame.quit() # arreter pygame

    def destroy(self):
        # fermeture de la fenetre 
        print("bye") # afficher bye parce que c'est marrant
        pygame.quit() # arreter pygame
        exit() # arrreter tous les programmes en cours