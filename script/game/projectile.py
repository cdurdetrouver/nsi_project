import pygame


class Projectile(pygame.sprite.Sprite):
    # cette class gere le projectile
    def __init__(self, fusee, screen_size, pluie):
        super().__init__()
        self.fusee = fusee
        self.pluie = pluie
        self.image = pygame.image.load("image/projectile.png")
        self.image = pygame.transform.scale(self.image, (self.fusee.sprite.get_size(
        )[1] * 0.3 * self.image.get_size()[0]/self.image.get_size()[1], self.fusee.sprite.get_size()[1] * 0.3))
        self.launch = False

        self.speed = screen_size[1] / 60

        self.rect = self.image.get_rect()

        self.rect.x = self.fusee.pos[0] + \
            self.fusee.sprite.get_size()[0] / 2 - self.image.get_size()[0] / 2
        self.rect.y = self.fusee.pos[1] + \
            self.fusee.sprite.get_size()[1] / 2 - self.image.get_size()[1]

        self.son = pygame.mixer.Sound("musique/explode.wav")
        self.son.set_volume(0.3)

    def launch_y(self):
        self.launch = True
        self.rect.y -= self.speed

    def collision(self):
        for meteor in self.pluie.all_meteor:
            if pygame.Rect.colliderect(self.rect, meteor.collide_rect):
                self.fusee.score.ajout_score(1)
                self.launch = False
                meteor.delete = True
                self.son.play()

    def update(self):
        if self.rect.y < - self.image.get_size()[1]:
            self.launch = False

        if self.launch:
            self.launch_y()
            self.collision()
        else:
            self.rect.x = self.fusee.pos[0] + self.fusee.sprite.get_size()[
                0] / 2 - self.image.get_size()[0] / 2
            self.rect.y = self.fusee.pos[1] + \
                self.fusee.sprite.get_size()[1] / 2 - self.image.get_size()[1]
