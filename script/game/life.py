import pygame
import random

class Life():
    def __init__(self, life, screen_size, game, fusee):
        self.life = life
        self.game = game
        self.fusee = fusee

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

        self.fallen_heart = Fallen_Heart(self.screen_size, self, self.heart, fusee)


    def lost_life(self):
        self.life -= 1
        if self.life == 0:
            self.game.game_over()

    def add_life(self):
        if self.life < 3:
            self.life += 1
        else:
            self.fusee.score.ajout_score(3)

    def afficher(self, screen):
        taille = 0
        for i in range(self.life):
            screen.blit(self.heart, (self.pos[0] * (i+1) + self.heart_size[0] * i, self.pos[1]))
            taille = i + 1
        for j in range(3 - self.life):
            screen.blit(self.empty_heart, (self.pos[0] * (taille + j + 1) + self.empty_heart_size[0] * (taille + j), self.pos[1]))
        self.fallen_heart.afficher(screen)

class Fallen_Heart():
    def __init__(self, screen_size, life, sprite, fusee):
        # coeur qui tombe de temps en temps
        self.life = life
        self.screen_size = screen_size
        self.sprite = sprite
        self.fusee = fusee

        self.fallen_heart_rect = pygame.rect.Rect(random.randint(0, self.screen_size[0] - self.sprite.get_size()[0]), -self.sprite.get_size()[1], self.sprite.get_size()[0], self.sprite.get_size()[1])
        
        self.time = 0

        self.can_fall = False

    def update_position(self):
        self.collision()
        self.fallen_heart_rect.y += self.screen_size[1] // 60 // 5

    def hors_champ(self):
        if self.fallen_heart_rect.y > self.screen_size[1]:
            return True
        return False

    def collision(self):
        if self.fallen_heart_rect.colliderect(self.fusee.rect):
            self.fallen_heart_rect.x = random.randint(0, self.screen_size[0] - self.sprite.get_size()[0])
            self.fallen_heart_rect.y = -self.sprite.get_size()[1]
            self.life.add_life()
            self.can_fall = False

    def afficher(self, screen):
        self.time += 1
        if self.time > 1000:
            self.time = 0
            self.can_fall = True
        if self.can_fall:
            screen.blit(self.sprite, (self.fallen_heart_rect.x, self.fallen_heart_rect.y))
            # pygame.draw.rect(screen, (255, 0, 0), self.fallen_heart_rect, 1)
            self.update_position()
            if self.hors_champ():
                self.fallen_heart_rect.x = random.randint(0, self.screen_size[0] - self.sprite.get_size()[0])
                self.fallen_heart_rect.y = 0
                self.can_fall = False