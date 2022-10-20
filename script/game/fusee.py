import pygame 

class Fusee():
    # cette class gere la fusee
    def __init__(self, pos, screen_size):
        self.screen_size = screen_size
        self.sprite = pygame.image.load("image/fusee.png") # charger l'image de la fusee 
        self.image_size = self.sprite.get_size() # taille de l'image 
        self.sprite = pygame.transform.scale(self.sprite, (self.screen_size[0] * 0.1, self.screen_size[0] * 0.1 * self.image_size[1]/self.image_size[0]))
        self.image_size = self.sprite.get_size() # taille de l'image final
        self.pos = [pos[0] - (self.image_size[0]/2), pos[1]] # position de la fusee

        
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
    def up(self, nb):
        # deplacement de la fusee vers le haut
        self.pos[1] -= nb
    
    def down(self, nb):
        # deplacement de la fusee vers le bas
        self.pos[1] += nb
    
    def right(self, nb):
        # deplacement de la fusee vers la droite
        self.pos[0] += nb
    
    def left(self, nb):
        # deplacement de la fusee vers la gauche
        self.pos[0] -= nb

    # fonctions d'affichage
    def afficher(self,screen):
        # affichage de la fusee
        self.collision()
        screen.blit(self.sprite,(self.pos[0],self.pos[1]))