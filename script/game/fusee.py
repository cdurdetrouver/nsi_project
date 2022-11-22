import pygame

from script.game.projectile import Projectile 
from script.game.meteorite import Pluie_Meteorite
from script.game.life import Life

class Fusee():
    # cette class gere la fusee
    def __init__(self, pos, screen_size, game, score):
        self.screen_size = screen_size
        self.score = score

        self.sprite = pygame.image.load("image/fusee.png") # charger l'image de la fusee 
        self.image_size = self.sprite.get_size() # taille de l'image 
        self.sprite = pygame.transform.scale(self.sprite, (self.screen_size[0] * 0.085, self.screen_size[0] * 0.085 * self.image_size[1]/self.image_size[0]))
        
        self.red_sprite = pygame.image.load("image/fusee - Copie.png")
        self.red_sprite = pygame.transform.scale(self.red_sprite, (self.screen_size[0] * 0.085, self.screen_size[0] * 0.085 * self.image_size[1]/self.image_size[0]))

        self.sprite_copy = self.sprite.copy()

        self.image_size = self.sprite.get_size() # taille de l'image final
        self.pos = [pos[0] - (self.image_size[0]/2), pos[1]] # position de la fusee

        self.speed = screen_size[0] / 60 / 2 # pour déplacer la fusee en 2 secondes sur la taille x de l'écran

        self.life = Life(3, self.screen_size, game, self)

        self.pluie = Pluie_Meteorite(self.screen_size, self, score)

        self.proj = pygame.sprite.Group()
        self.proj.add(Projectile(self, screen_size, self.pluie))

        self.rect = pygame.rect.Rect(self.pos[0] + self.sprite.get_size()[0]/5, self.pos[1], self.sprite.get_size()[0] * 3/5, self.sprite.get_size()[1]* 3/4)

        self.invincible = False

        self.n = 0

        self.time = pygame.time.get_ticks()


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

        for meteor in self.pluie.all_meteor:
            if pygame.Rect.colliderect(self.rect, meteor.collide_rect) and not meteor.delete:
                meteor.delete = True
                if not self.invincible:
                    self.invincible = True
                    self.life.lost_life()

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

    def clignottement(self):
        if self.n%2 == 0:
            self.sprite = self.sprite_copy
        else:
            self.sprite = self.red_sprite

    # fonctions d'affichage
    def afficher(self,screen):
        # update du rect
        self.rect = pygame.Rect.fit(self.rect, (self.pos[0]+ self.sprite.get_size()[0]/5,self.pos[1], self.rect.width, self.rect.height))

        #affichage des météorites
        self.pluie.afficher(screen)

        # affichage de la fusee
        self.collision()
        self.proj.draw(screen)
        for proj in self.proj:
            proj.update()
        screen.blit(self.sprite,(self.pos[0],self.pos[1]))

        time = pygame.time.get_ticks()
        if self.invincible:
            self.clignottement()
            if time - self.time > 250:
                self.n +=1
                self.time = pygame.time.get_ticks()
                if self.n >= 6:
                    self.invincible = False
                    self.n = 0
                    self.sprite = self.sprite_copy