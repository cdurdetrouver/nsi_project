from script.UI.score import Score
from script.UI.menu import Menu
import pygame

class UI():
    def __init__(self, size, game, life, score = None):
        self.size = size
        if score:
            self.score = score
        else:
            self.score = Score((size[0] - size[0]/40, size[1]/20), size)
        
        self.life = life
        self.button_start = ButtonStart((self.size[0]//2, self.size[1]//2), self.size)
        self.button_parameter = ButtonParameter(self.size)
        self.button_high_score = ButtonHighScore((self.size[0]//2, self.size[1]*0.75), self.size)

        self.menu = Menu(self.size, game)

    def menu_click_button(self):
        return self.menu.click_on_button()

    def get_score(self):
        return self.score

    def get_button_start(self):
        return self.button_start

    def get_button_high_score(self):
        return self.button_high_score

    def get_button_parameter(self):
        return self.button_parameter

    def afficher(self, window, screen):
        if screen == "menu" :
            self.score.afficher(window)
            self.button_start.afficher(window)
            self.button_parameter.afficher(window)
            self.button_high_score.afficher(window)
        elif screen == "highscore" :
            self.score.afficher(window)
            self.menu.afficher(window, "highscore")
        elif screen == "parameter":
            self.menu.afficher(window, "parameter")
        elif screen == "gameover":
            self.menu.afficher(window, "gameover")
        else:
            self.score.afficher(window)
            self.life.afficher(window)

class ButtonParameter():
    # gere le menu
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.image = pygame.image.load("image/parameter.png") # charger l'image du boutton
        self.image_size = self.image.get_size() # taille de l'image pour la reduction
        self.image = pygame.transform.scale(self.image, (self.screen_size[0] * 0.08, self.screen_size[0] * 0.08))
        self.image_size = self.image.get_size() # taille de l'image final

        self.pos = [self.screen_size[0] * 5 / 100 - (self.image_size[0]/2), self.screen_size[0] * 5 / 100 - (self.image_size[1]/2)]

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.screen_size[0] * 0.08, self.screen_size[0] * 0.08)

        self.image_copy = self.image.copy() # charger l'image du boutton
        self.image_copy = pygame.transform.scale(self.image_copy, (self.image_size[0] * 1.2, self.image_size[1] * 1.2))
        self.image_copy_size = self.image_copy.get_size() # taille de l'image final

        self.pos_copy = [self.screen_size[0] * 5 / 100 - (self.image_copy_size[0]/2), self.screen_size[0] * 5 / 100 - (self.image_copy_size[1]/2)]

    def on(self):
        return pygame.Rect.collidepoint(self.rect, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    def afficher(self, screen):
        # affichage du score
        if self.on():
            screen.blit(self.image_copy,(self.pos_copy[0], self.pos_copy[1]))
        else:
            screen.blit(self.image,(self.pos[0], self.pos[1]))

class ButtonStart():
    # gere le menu
    def __init__(self,pos, screen_size):
        self.screen_size = screen_size
        self.pos = [pos[0], pos[1]] # position du boutton
        self.image = pygame.image.load("image/button_start.png") # charger l'image du boutton
        self.image_size = self.image.get_size() # taille de l'image pour la reduction
        self.image = pygame.transform.scale(self.image, (self.screen_size[0] * 0.4, self.screen_size[0] * 0.4 * self.image_size[1]/self.image_size[0]))
        self.image_size = self.image.get_size() # taille de l'image final

        self.pos = [pos[0] - (self.image_size[0]/2), pos[1] - (self.image_size[1]/2)]

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.screen_size[0] * 0.4, self.screen_size[0] * 0.4 * self.image_size[1]/self.image_size[0])

        self.image_copy = self.image.copy() # charger l'image du boutton
        self.image_copy = pygame.transform.scale(self.image_copy, (self.image_size[0] * 1.2, self.image_size[1] * 1.2))
        self.image_copy_size = self.image_copy.get_size() # taille de l'image final

        self.pos_copy = [pos[0] - (self.image_copy_size[0]/2), pos[1] - (self.image_copy_size[1]/2)]

    def on(self):
        return pygame.Rect.collidepoint(self.rect, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    def afficher(self, screen):
        # affichage du score
        if self.on():
            screen.blit(self.image_copy,(self.pos_copy[0], self.pos_copy[1]))
        else:
            screen.blit(self.image,(self.pos[0], self.pos[1]))


class ButtonHighScore():
    # gere le menu
    def __init__(self,pos, screen_size):
        self.screen_size = screen_size
        self.pos = [pos[0], pos[1]] # position du boutton
        self.image = pygame.image.load("image/button_start.png") # charger l'image du boutton
        self.image_size = self.image.get_size() # taille de l'image pour la reduction
        self.image = pygame.transform.scale(self.image, (self.screen_size[0] * 0.4, self.screen_size[0] * 0.4 * self.image_size[1]/self.image_size[0]))
        self.image_size = self.image.get_size() # taille de l'image final

        self.pos = [pos[0] - (self.image_size[0]/2), pos[1] - (self.image_size[1]/2)]

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.screen_size[0] * 0.4, self.screen_size[0] * 0.4 * self.image_size[1]/self.image_size[0])

        self.image_copy = self.image.copy() # charger l'image du boutton
        self.image_copy = pygame.transform.scale(self.image_copy, (self.image_size[0] * 1.2, self.image_size[1] * 1.2))
        self.image_copy_size = self.image_copy.get_size() # taille de l'image final

        self.pos_copy = [pos[0] - (self.image_copy_size[0]/2), pos[1] - (self.image_copy_size[1]/2)]

    def on(self):
        return pygame.Rect.collidepoint(self.rect, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    def afficher(self, screen):
        # affichage du score
        if self.on():
            screen.blit(self.image_copy,(self.pos_copy[0], self.pos_copy[1]))
        else:
            screen.blit(self.image,(self.pos[0], self.pos[1]))