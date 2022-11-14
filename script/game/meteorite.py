import pygame
import random
import math

class Meteorite(pygame.sprite.Sprite):
    # cette class gere les meteorites qui tombent du ciel
    def __init__(self,vitesse, screen_size, fusee, score):
        self.score = score
        self.fusee = fusee
        self.screen_size = screen_size
        self.vitesse = vitesse
        self.coef_decallage = random.randint(-int(self.vitesse), int(self.vitesse))

        x_2 = self.coef_decallage
        y_2 = self.vitesse

        alpha = math.atan(x_2/y_2) *180/math.pi

        self.sprite = pygame.image.load("image/Meteor.png")
        self.sprite = pygame.transform.scale(self.sprite,(self.screen_size[0] * 0.085, self.screen_size[0] * 0.085 * self.sprite.get_size()[1]/self.sprite.get_size()[0]))
        self.rect = self.sprite.get_rect()
        self.sprite = pygame.transform.rotate(self.sprite, alpha)

        x = random.randint(0,screen_size[0])
        y = 0 - self.sprite.get_size()[1]
        self.pos = [x,y]

        self.already = False

    def collision(self):
        return pygame.Rect.colliderect(self.rect, self.fusee.rect)

    def collision_proj(self):
        return pygame.Rect.colliderect(self.rect, self.fusee.proj.rect)

    def update_position(self):
        self.pos[1] += self.vitesse
        self.pos[0] += self.coef_decallage
        
    def afficher(self,screen):
        #update du rect
        self.rect = pygame.Rect.fit(self.rect, (self.pos[0],self.pos[1], self.rect.width, self.rect.height))

        # update position
        self.update_position()
        if self.collision() and not self.already:
            self.fusee.life.lost_life()
            self.already = True
        if self.collision_proj() and not self.already:
            self.score.ajout_score(1)
            self.fusee.proj.reset()
            self.already = True
        # affichage de la meteorite
        if not self.already : 
            screen.blit(self.sprite,(self.pos[0],self.pos[1]))
            pygame.draw.rect(screen, (255,0,0), self.rect, 1)

    def hors_champ(self):
        if self.pos[1] > self.screen_size[1] or self.pos[0] > self.screen_size[0] or self.pos[0]< -self.sprite.get_size()[0] or self.already:
            return True

class Pluie_Meteorite():
    def __init__(self, screen_size, fusee, score):
        self.screen_size = screen_size
        self.fusee = fusee
        self.score = score
        self.meteorites = []
        self.time = 0
        self.time_add = 0
        self.vitesse_minimum = 2
        self.vitesse_maximum = 3
        for i in range(1):
            self.meteorites.append(Meteorite(screen_size[1] // 60 // random.uniform(self.vitesse_minimum,self.vitesse_maximum), self.screen_size, self.fusee, self.score))

    def afficher(self, screen):
        for i in range(len(self.meteorites)):
            self.meteorites[i].afficher(screen)
            if self.meteorites[i].hors_champ():
                self.meteorites[i] = Meteorite(self.screen_size[1] // 60 // random.uniform(self.vitesse_minimum,self.vitesse_maximum), self.screen_size, self.fusee, self.score)
            time = pygame.time.get_ticks()
            if time - self.time > 750:
                self.time = time
                if self.vitesse_minimum != self.vitesse_maximum:
                    self.vitesse_minimum -= 0.01
                    self.vitesse_maximum -= 0.01
                    if self.vitesse_minimum < 0.05:
                        self.vitesse_minimum = 0.05
                    if self.vitesse_maximum < 0.05:
                        self.vitesse_maximum = 0.05
            if len(self.meteorites)< 5 and time - self.time_add > 1500:
                self.meteorites.append(Meteorite(self.screen_size[1] // 60 // random.uniform(self.vitesse_minimum,self.vitesse_maximum), self.screen_size, self.fusee, self.score))
                self.time_add = time