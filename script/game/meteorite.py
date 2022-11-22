import pygame
import random
import math

class Meteorite(pygame.sprite.Sprite):
    # cette class gere les meteorites qui tombent du ciel
    def __init__(self,vitesse, screen_size):
        super().__init__()
        self.screen_size = screen_size
        self.vitesse = vitesse
        self.coef_decallage = random.uniform(-self.vitesse,self.vitesse)

        x_2 = self.coef_decallage
        y_2 = self.vitesse

        self.alpha = math.atan(x_2/y_2) * 180/math.pi

        self.image = pygame.image.load("image/Meteor.png")
        self.image = pygame.transform.scale(self.image,(self.screen_size[0] * 0.085, self.screen_size[0] * 0.085 * self.image.get_size()[1]/self.image.get_size()[0]))
        self.size = (self.image.get_size()[0], self.image.get_size()[1])
        self.image = pygame.transform.rotate(self.image, self.alpha)

        self.rect = self.image.get_rect()

        x = random.randint(0,screen_size[0])
        y = 0 - self.image.get_size()[1]
        self.rect.x = x - self.size[0]
        self.rect.y = y - self.size[0]

        if self.alpha < 0:
            self.collide_rect = pygame.rect.Rect(0,0,0,0)
            self.collide_rect.y = self.rect.y + self.size[1]//2
            self.collide_rect.x = self.rect.x
            self.collide_rect.height = self.size[1]//2
            self.collide_rect.width = self.size[0]
        elif self.alpha == 0:
            self.collide_rect = pygame.rect.Rect(0,0,0,0)
            self.collide_rect.y = self.rect.y + self.size[1]//2
            self.collide_rect.x = self.rect.x
            self.collide_rect.height = self.size[1]//2
            self.collide_rect.width = self.size[0]
        else:
            self.collide_rect = pygame.rect.Rect(0,0,0,0)
            self.collide_rect.y = self.rect.y + self.size[1]//2
            self.collide_rect.x = self.rect.x + self.rect.width - self.size[0]
            self.collide_rect.height = self.size[1]//2
            self.collide_rect.width = self.size[0]

        self.delete = False

    def position(self):
        self.rect.x += self.coef_decallage
        self.rect.y += self.vitesse

        self.collide_rect.x += self.coef_decallage
        self.collide_rect.y += self.vitesse

    def collision(self):
        if self.rect.x > self.screen_size[0] or self.rect.y > self.screen_size[1] or self.rect.x + self.size[0] < 0:
            self.delete = True
        
    def update(self):
        self.position()
        self.collision()


class Pluie_Meteorite():
    def __init__(self, screen_size, fusee, score):
        self.all_meteor = pygame.sprite.Group()
        self.screen_size = screen_size
        self.fusee = fusee
        self.score = score
        self.vitesse_minimum = 2
        self.vitesse_maximum = 3

        for i in range(2):
            self.spawn_meteor()
        
        self.time = pygame.time.get_ticks()
        self.time_2 = pygame.time.get_ticks()


    def spawn_meteor(self):
        meteor = Meteorite(self.screen_size[1] // 60 // random.uniform(self.vitesse_minimum,self.vitesse_maximum), self.screen_size)
        self.all_meteor.add(meteor)

    def afficher(self, screen):
        self.all_meteor.draw(screen)

        for meteor in self.all_meteor:
            meteor.update()
            if meteor.delete:
                self.all_meteor.remove(meteor)
                new_meteor = Meteorite(self.screen_size[1] // 60 // random.uniform(self.vitesse_minimum,self.vitesse_maximum), self.screen_size)
                self.all_meteor.add(new_meteor)

        time = pygame.time.get_ticks()
        if time - self.time > 2000:
            if self.vitesse_minimum > 0.5:
                self.vitesse_minimum -= 0.05
            if self.vitesse_maximum - self.vitesse_minimum > 1:
                self.vitesse_maximum -= 0.05
            self.time = pygame.time.get_ticks()

        if self.all_meteor.__len__() < 5:
            if time - self.time_2 > 2000:
                new_meteor = Meteorite(self.screen_size[1] // 60 // random.uniform(self.vitesse_minimum,self.vitesse_maximum), self.screen_size)
                self.all_meteor.add(new_meteor)
                self.time_2 = pygame.time.get_ticks()