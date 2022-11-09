import pygame
import ctypes 
user32 = ctypes.windll.user32
screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

class Menu():
    # gere le menu
    def __init__(self, screen_size, game):
        self.screen_size = screen_size
        self.game = game
    
        # texte du score
        pygame.font.init()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        self.police = pygame.font.SysFont("font/font.ttf", 256) # police d'ecriture

        
        self.image = self.police.render("Menu", True, (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (self.screen_size[0] * 0.2, self.screen_size[0] * 0.2 * self.image.get_size()[1]/self.image.get_size()[0]))

        #differente taille d'ecran a afficher dans le menu
        self.taille = [(640,480),
                        (1028,768),
                        (1366,768),
                        (1280,1024),       
                        (1600,900),
                        (1920,1080)]

        self.buttons = []

        self.new_taille = []

        # est-ce que les tailles proposees sont plus grandes que l'ecran
        for i in range(len(self.taille)):
            if screensize[0] * screensize[1] >= self.taille[i][0] * self.taille[i][1]:
                self.new_taille.append(self.taille[i])

        coef = (self.screen_size[1] - self.screen_size[1]/2) / len(self.new_taille)

        for i in range(len(self.new_taille)):
            self.buttons.append(Button((self.new_taille[i][0], self.new_taille[i][1]), (self.screen_size[0] / 2, self.screen_size[1]/40 + self.screen_size[0] * 0.2 * self.image.get_size()[1]/self.image.get_size()[0] + coef * (i+1)), game, self.screen_size))

        self.button_back = ButtonBack(self.screen_size, game)

    def click_on_button(self):
        if self.game.parameter:
            for button in self.buttons:
                if button.on():
                    button.click()
        
        if self.button_back.on():
            self.button_back.click()

    def click_back(self):
        return self.button_back.click()

    def afficher(self, screen, ecran):
        if ecran == "parameter":
            screen.blit(self.image,(self.screen_size[0] / 2  - self.image.get_size()[0]/2, self.screen_size[1]/40))
            for button in self.buttons:
                button.afficher(screen)
        self.button_back.afficher(screen)

class ButtonBack():
    # gere le retour a l'ecran principal
    def __init__(self, screen_size, game):
        self.screen_size = screen_size
        self.game = game

        self.image = pygame.image.load("image/button_back.png") # charger l'image du boutton
        self.image_size = self.image.get_size() # taille de l'image pour la reduction
        self.image = pygame.transform.scale(self.image, (self.screen_size[0] * 0.2, self.screen_size[0] * 0.2 * self.image_size[1]/self.image_size[0]))
        self.image_size = self.image.get_size() # taille de l'image final

        self.pos = [self.screen_size[0] * 5 / 100, self.screen_size[1] - self.screen_size[1] * 5 / 100 - self.image_size[1]] # position de l'image

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image_size[0], self.image_size[0])

        self.image_copy = self.image.copy() # charger l'image du boutton
        self.image_copy = pygame.transform.scale(self.image_copy, (self.image_size[0] * 1.2, self.image_size[1] * 1.2))
        self.image_copy_size = self.image_copy.get_size() # taille de l'image final

        self.pos_copy = [self.screen_size[0] * 5 / 100 - (self.image_copy_size[0] - self.image_size[0]) / 2, self.screen_size[1] - self.screen_size[1] * 5 / 100 - self.image_size[1] - (self.image_copy_size[1] - self.image_size[1]) / 2] # position de l'image

    def on(self):
        return pygame.Rect.collidepoint(self.rect, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    def click(self):
        self.game.gameOver = False
        self.game.highscore = False
        self.game.parameter = False
        self.game.menu = True
        pygame.mouse.set_cursor(pygame.cursors.Cursor((24, 24), (0, 0), *pygame.cursors.compile(pygame.cursors.thickarrow_strings))) # cursor non-transparent

    def afficher(self, screen):
        # affichage du score
        if self.on():
            screen.blit(self.image_copy,(self.pos_copy[0], self.pos_copy[1]))
        else:
            screen.blit(self.image,(self.pos[0], self.pos[1]))

class Button():
    def __init__(self, taille, pos, game, screen_size):
        self.game = game
        self.pos = pos
        self.screen_size = screen_size
        self.taille = taille

        # police d'ecriture
        pygame.font.init()
        self.police = pygame.font.SysFont("font/font.ttf", 256)

        if screensize[0] == self.taille[0] and screensize[1] == self.taille[1]:
            self.image_text = self.police.render( f"Fullscreen", True , (255,255,255) ) # image du score ("texte a afficher", couleur?, couleur)
        else: 
            self.image_text = self.police.render( f"{self.taille[0]} X {self.taille[1]}", True , (255,255,255) ) # image du score ("texte a afficher", couleur?, couleur)
        
        self.image_text = pygame.transform.scale(self.image_text, (self.screen_size[0] * 0.2, self.screen_size[0] * 0.2 * self.image_text.get_size()[1]/self.image_text.get_size()[0]))
        self.image_text_size = self.image_text.get_size()

        self.box = pygame.image.load("image/score_box.png")
        self.box = pygame.transform.scale(self.box, (self.image_text_size[0] * 1.2, self.image_text_size[1] * 2))
        self.box_size = (self.box.get_size()[0], self.box.get_size()[1])

        self.rect = pygame.Rect(self.pos[0] - self.box_size[0]/2, self.pos[1] - self.box_size[1]/2, self.box_size[0], self.box_size[1])

        self.image_text_copy = self.image_text.copy()
        self.image_text_copy = pygame.transform.scale(self.image_text_copy, (self.image_text_size[0] * 1.2, self.image_text_size[0] * (self.image_text_size[1]/self.image_text_size[0]) * 1.2))
        self.image_text_copy_size = self.image_text_copy.get_size()

        self.box_copy = self.box.copy()
        self.box_copy = pygame.transform.scale(self.box_copy, (self.image_text_copy_size[0] * 1.2, self.image_text_copy_size[1] * 2))
        self.box_copy_size = (self.box_copy.get_size()[0], self.box_copy.get_size()[1])

        self.pos_copy = [self.pos[0] - self.box_copy_size[0]/2, self.pos[1] - self.box_copy_size[1]/2]

    def on(self):
        return pygame.Rect.collidepoint(self.rect, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    def click(self):
        if self.screen_size[0] != self.taille[0]:
            self.game.new_screen(self.taille)

    def afficher(self, screen):
        if self.on():
            screen.blit(self.box_copy,(self.pos_copy[0], self.pos_copy[1]))
            screen.blit(self.image_text_copy,(self.pos_copy[0] + self.box_copy_size[0]/2 - self.image_text_copy_size[0]/2, self.pos_copy[1] + self.box_copy_size[1]/2 - self.image_text_copy_size[1]/2))
        else:
            screen.blit(self.box, (self.pos[0] - self.box_size[0]/2, self.pos[1] - self.box_size[1]/2))
            screen.blit(self.image_text,(self.pos[0] - self.image_text_size[0]/2, self.pos[1] - self.image_text_size[1]/2))