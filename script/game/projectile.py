from operator import truediv
import pygame

class Projectile():
    # cette class gere le projectile
    def __init__(self, fusee, screen_size):
        self.fusee = fusee
        self.sprite = pygame.image.load("image/projectile.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.fusee.sprite.get_size()[1] * 0.3 * self.sprite.get_size()[0]/self.sprite.get_size()[1], self.fusee.sprite.get_size()[1] * 0.3))
        self.launch = False

        self.pos = [self.fusee.pos[0] + self.fusee.sprite.get_size()[0] / 2 - self.sprite.get_size()[0] / 2, self.fusee.pos[1] + self.fusee.sprite.get_size()[1] / 2 - self.sprite.get_size()[1]]

        self.speed = screen_size[1] / 60
        
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.sprite.get_size()[0], self.sprite.get_size()[1])

    def launch_y(self):
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.sprite.get_size()[0], self.sprite.get_size()[1])
        self.launch = True
        self.pos[1] -= self.speed

    def reset(self):
        self.launch = False
        self.pos[0] = self.fusee.pos[0] + self.fusee.sprite.get_size()[0] / 2 - self.sprite.get_size()[0] / 2
        self.pos[1] = self.fusee.pos[1] + self.fusee.sprite.get_size()[1] / 2 - self.sprite.get_size()[1] / 2
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.sprite.get_size()[0], self.sprite.get_size()[1])

    def afficher(self, screen):
        if self.pos[1] < - self.sprite.get_size()[1]:
            self.reset()

        if self.launch: 
            self.launch_y()
            
            screen.blit(self.sprite, self.pos)
            pygame.draw.rect(screen, (255,0,0), self.rect, 1)
        else:
            self.pos[0] = self.fusee.pos[0] + self.fusee.sprite.get_size()[0] / 2 - self.sprite.get_size()[0] / 2
            self.pos[1] = self.fusee.pos[1] + self.fusee.sprite.get_size()[1] / 2 - self.sprite.get_size()[1] / 2
            self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.sprite.get_size()[0], self.sprite.get_size()[1])
