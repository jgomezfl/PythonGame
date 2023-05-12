import pygame

width = 800
height = 800
black = (0, 0, 0)

class Marciano(pygame.sprite.Sprite):
    def __init__(self, img, posX, posY):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/"+img).convert(), (50,50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.speedx = 2
        self.speedy = 0
        
    def update(self):
        self.speedy = 0
        if self.rect.right > width:
            self.speedx = -2
            self.speedy = 30
        if self.rect.left < 0:
            self.speedx = 2
            self.speedy = 30
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if self.rect.bottom > height:
            self.rect.bottom = height
            game_over = True
