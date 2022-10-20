import pygame

class Score():
    # gere le score du jeu
    def __init__(self,pos):
        self.pos = [pos[0], pos[1]]
        self.score = 0

        # texte du score
        pygame.font.init()
        self.police = pygame.font.SysFont("Comic Sans MS" ,18) # police d'ecriture
    
    def ajout_score(self,nb):
        # ajouter le nombre de point en argument au score actuel
        self.score += nb

    def afficher(self, screen):

        self.image_texte = self.police.render( f"{self.score}", True , (0,0,0) ) # texte du score ("texte a afficher", couleur?, couleur)
        
        # affichage du score
        screen.blit(self.image_texte,(self.pos[0],self.pos[1]))