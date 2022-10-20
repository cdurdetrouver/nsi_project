import pygame

class Score():
    # gere le score du jeu
    def __init__(self,pos, screen_size):
        self.pos = [pos[0], pos[1]]
        self.score = 0
        self.size = screen_size

        # texte du score
        pygame.font.init()
        self.police = pygame.font.SysFont("font/font.ttf", 32) # police d'ecriture



    def ajout_score(self,nb):
        # ajouter le nombre de point en argument au score actuel
        self.score += nb

    def reset(self):
        self.score = 0

    def afficher(self, screen):
        self.image_text = self.police.render( f"score : {self.score}", True , (0,0,0) ) # image du score ("texte a afficher", couleur?, couleur)
        self.image_text = pygame.transform.scale(self.image_text, (self.size[0] * 0.15, self.size[0] * 0.15 * self.image_text.get_size()[1]/self.image_text.get_size()[0]))
        
        self.box = pygame.image.load("image/score_box.png")
        self.box = pygame.transform.scale(self.box, (self.image_text.get_size()[0] * 1.2, self.image_text.get_size()[1] * 2))

        # affichage du score
        screen.blit(self.box, (self.pos[0]- self.image_text.get_size()[0] - (self.box.get_size()[0] - self.image_text.get_size()[0])/2, self.pos[1] - self.image_text.get_size()[1]/2))
        screen.blit(self.image_text,(self.pos[0] - self.image_text.get_size()[0], self.pos[1]))