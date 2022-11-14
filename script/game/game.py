import pygame
import unidecode
import sqlite3
from pygame.locals import *
from script.game.fusee import Fusee
from script.UI.ui import UI
from script.game.classement import Classement


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
        self.already2 = False # est-ce que la touche p est enfonce

        # police d'ecriture
        pygame.font.init()
        self.police = pygame.font.SysFont("font/font.ttf", 256) # police d'ecriture

        self.classement = Classement(self.size, self)
        self.classement.connect()
        self.internet_connexion = self.classement.get_connexion()

        # affichage du background
        self.new_screen(self.size)

        # preparer au fps
        self.clock = pygame.time.Clock()

        # menu de jeux
        self.menu = True

        # menu parametre
        self.parameter = False

        # fenetre de score
        self.highscore = False

        self.gameOver = False

        self.name = "Test"



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

        self.game_over_image = pygame.image.load("image/game_over.png") # image de game over
        self.game_over_image = pygame.transform.scale(self.game_over_image,(self.size[0] * 50/100, self.size[0] * 50/100 * self.game_over_image.get_size()[1]/self.game_over_image.get_size()[0])) #redimension

        self.window.blit(self.background,(0 - (self.background_size[0] - screen_size[0]), 0))
        connexion = self.police.render("Please Wait ...", True , (255,255,255))
        connexion = pygame.transform.scale(connexion, (screen_size[1] * 30/100 * connexion.get_size()[0] / connexion.get_size()[1],screen_size[1] * 30/100))
        self.window.blit(connexion, (screen_size[0]/2 - connexion.get_size()[0]/2, screen_size[1]/2 - connexion.get_size()[1]/2))

        self.input_rect = pygame.Rect((self.size[0] * 5 / 100, self.size[1]//2), (self.size[0] * 9 / 100, self.size[0] * 3 / 100))
        self.text_pseudo = self.police.render("Pseudo :", True, (255,255,255))
        self.text_pseudo = pygame.transform.scale(self.text_pseudo, (self.size[1] * 5 / 100 * self.text_pseudo.get_size()[0] / self.text_pseudo.get_size()[1], self.size[1] * 5 / 100))
        self.text_wrong = self.police.render("Pseudo interdit", True, (255,0,0))
        self.text_wrong = pygame.transform.scale(self.text_wrong, (self.size[1] * 5 / 100 * self.text_wrong.get_size()[0] / self.text_wrong.get_size()[1], self.size[1] * 5 / 100))

        # appel des objets
        self.UI = UI(self.size, self, None) # creation de l'interface utilisateur
        self.score = self.UI.get_score()
        self.button_start = self.UI.get_button_start()
        self.button_high_score = self.UI.get_button_high_score()
        self.button_parameter = self.UI.get_button_parameter()
        self.classement.new_res(self.size)

    def game_over(self):
        # quand la vie est a 0
        self.gameOver = True
        pygame.mouse.set_cursor(self.cursors[0]) # cursor non-transparent
        self.classement.update_classement(self.user_name, self.score.get()) # mettre a jour le classement

    def handle_input(self, pressed):

        if pressed[pygame.K_ESCAPE]: 
            self.destroy() # arreter le jeux

        # pas d'autre touche si on est sur le menu
        if self.menu or self.highscore or self.parameter or self.gameOver:
            return

        if pressed[pygame.K_p]:
            if not self.already2:
                return
            else: 
                self.life.lost_life()
                self.already2 = False
        else:
            self.already2 = True

        if pressed[pygame.K_UP] or pressed[pygame.K_z]:
            self.fusee.up() # deplacer la fusee en haut
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.fusee.down() # deplacer la fusee en bas
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.fusee.right() # deplacer la fusee sur la droite
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.fusee.left() # deplacer la fusee sur la gauche
        
        if pressed[pygame.K_SPACE]:
            if not self.already:
                return
            else: 
                self.fusee.proj.launch = True
                self.already = False
        else:
            self.already = True
        

    def update(self):
        # update d'affichage
        if self.menu :
            self.window.blit(self.background_blur,(0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.UI.afficher(self.window, "menu") # afficher le score + le boutton jouer
            # draw rectangle and argument passed which should
            # be on screen
            pygame.draw.rect(self.window, self.color, self.input_rect)
            # render at position stated in arguments
            self.window.blit(self.text_surface, (self.size[0] * 5 / 100, self.size[1]//2))
            self.window.blit(self.text_pseudo, (self.size[0] * 5 / 100, self.size[1]//2 - 1.5 * self.text_surface.get_size()[1]))
            if self.wrong_pseudo:
                self.window.blit(self.text_wrong, (self.size[0] * 5 / 100, self.size[1]//2 + 1.5 * self.text_surface.get_size()[1]))
        elif self.parameter:
            self.window.blit(self.background_blur,(0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.UI.afficher(self.window, "parameter") # afficher le menu parametre
        elif self.gameOver:
            self.window.fill((0,0,0))
            self.window.blit(self.game_over_image, (self.size[0] * 25/100, self.size[1] * 25/100))
            self.UI.afficher(self.window, "gameover") # afficher le score
        elif self.highscore:
            self.window.blit(self.background_blur,(0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.UI.afficher(self.window, "highscore")
            self.classement.afficher(self.window)
        else :
            self.window.blit(self.background,(0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.fusee.afficher(self.window) # afficher la fusee
            self.UI.afficher(self.window, "game") # afficher le score

    def start_game(self):
        pygame.mouse.set_cursor(self.cursors[1]) # cursor transparent

        # transision entre l'ecran de menu et de jeux 
        for i in range(3, 0, -1):
            self.image_text = self.police.render( f"{i}", True , (255,255,255) ) # image du decompte ("texte a afficher", couleur?, couleur)
            self.image_text = pygame.transform.scale(self.image_text, (self.size[1] * 40/100 * self.image_text.get_size()[0] / self.image_text.get_size()[1],self.size[1] * 40/100)) # redimensionner l'image
            self.window.blit(self.background, (0 - (self.background_size[0] - self.size[0]), 0)) # afficher le background
            self.window.blit(self.image_text, (self.size[0]/2 - self.image_text.get_size()[0]/2, self.size[1]/2 - self.image_text.get_size()[1]/2))
            pygame.display.flip()
            pygame.time.wait(1000)

        self.fusee = Fusee((self.size[0]/2,self.size[1]), self.size, self, self.score) # appel la fusee
        self.life = self.fusee.get_life()
        self.UI = UI(self.size, self, self.life, self.score) # appel l'interface utilisateur
        self.score.reset() # remettre le score a 0

    def run(self):

        self.user_name = ''

        self.wrong_pseudo = False

        symbols = [" " ,"-" ,"_","~" ,"/" ,"\\" ,"." ,"," ,";" ,":" ,"?" ,"!" ,"@" ,"#" ,"$" ,"%" ,"^" ,"&" ,"*" ,"(" ,")" ,"[" ,"]" ,"{" ,"}" ,"<" ,">" ,"=" ,"+" ,"`" ,"'" ,"\"" ,"1" ,"2" ,"3" ,"4" ,"5" ,"6" ,"7" ,"8" ,"9","0"]
        
        # color_active stores color(lightskyblue3) which
        # gets active when input box is clicked by user
        color_active = pygame.Color('lightskyblue3')
        
        # color_passive store color(chartreuse4) which is
        # color of input box.
        color_passive = pygame.Color('chartreuse4')
        self.color = color_passive
        
        active = False

        connexion = sqlite3.connect("base_de_donee/grots_mots.db")
        cursor = connexion.cursor()
        injures = cursor.execute("""SELECT * FROM injures""")
        bad_words = []
        for elem in injures:
            bad_words.append(unidecode.unidecode(elem[0]).upper())

        # boucle qui gere le jeu
        while self.running:
            # recuperer les touches pressees 
            pressed = pygame.key.get_pressed()

            self.handle_input(pressed) # gere entre de touche

            if active:
                self.color = color_active
            else:
                self.color = color_passive

    
            self.text_surface = self.police.render(self.user_name, True, (255, 255, 255))
            self.text_surface = pygame.transform.scale(self.text_surface, (self.input_rect.h * self.text_surface.get_size()[0]/self.text_surface.get_size()[1], self.input_rect.h))
        
            # set width of textfield so that text cannot get
            # outside of user's text input
            self.input_rect.w = max(self.size[0] * 6 /100, self.text_surface.get_width() + 10)
            
            self.update() # gere l'affichage des objets

            pygame.display.flip() # actualiser l'ecran

            for event in pygame.event.get(): # regarder si la fenetre se ferme
                if event.type == pygame.QUIT:
                    self.running = False
                
                if not(self.menu) and not(self.parameter) and not(self.gameOver) and not(self.highscore):
                    break

                if event.type == pygame.KEYDOWN:
                    if active:
                        
                        self.wrong_pseudo = False
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:
        
                            # get text input from 0 to -1 i.e. end.
                            self.user_name = self.user_name[:-1]

                        # Unicode standard is used for string
                        # formation
                        else:
                            if len(self.user_name) < 13:
                                self.user_name += event.unicode

                            self.user_name_2 = unidecode.unidecode(self.user_name).upper()

                            self.user_name_final = ""

                            for j in self.user_name_2:
                                    if j != ' ' and j != '-' and j != '_'and j != '~' and j != '/' and j != '\\' and j != '.' and j != 'and j != ' and j != ';' and j != ':' and j != '?' and j != '!' and j != '@' and j != '#' and j != '$' and j != '%' and j != '^' and j != '&' and j != '*' and j != '(' and j != ')' and j != '[' and j != ']' and j != '{' and j != '}' and j != '<' and j != '>' and j != '=' and j != '+' and j != '`' and j != "'" and j != "\"" and j != '1' and j != '2' and j != '3' and j != '4' and j != '5' and j != '6' and j != '7' and j != '8' and j != '9'and j != '0' and j != '\n' and j != '"' and j != '¨' and j != 'µ' and j != "²":
                                        self.user_name_final += j

                            for word in bad_words:
                                if word == self.user_name_final:
                                    self.wrong_pseudo = True
                                    self.user_name = ""

                if event.type == MOUSEBUTTONDOWN:
                    if self.menu:
                        if self.input_rect.collidepoint(event.pos):
                            active = True
                        else:
                            active = False

                        if self.button_start.on():
                            self.start_game()
                            self.menu = False; self.parameter = False; self.highscore = False; self.gameOver = False
                        if self.button_parameter.on():
                            self.menu = False; self.parameter = True; self.highscore = False; self.gameOver = False
                        if self.button_high_score.on():
                            self.menu = False; self.parameter = False; self.highscore = True; self.gameOver = False
                    else:
                        self.UI.menu_click_button()

            self.clock.tick(self.fps) # gere les fps


        pygame.quit() # arreter pygame

    def destroy(self):
        # fermeture de la fenetre 
        print("bye") # afficher bye parce que c'est marrant
        pygame.quit() # arreter pygame
        exit() # arrreter tous les programmes en cours