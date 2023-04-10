import pygame, threading, random

width = 800
height = 800
black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
# screen.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, white)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/rocket.png").convert(), (50,50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed_x = 0
        self.speed_y = 0
        
    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()
        

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
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/proyectil.png").convert(), (30,30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -3
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
    
def show_go_screen():
    draw_text(screen, "Space Invaders", 65, width // 2, height // 4)
    draw_text(screen, "Presiona cualquier tecla para iniciar", 27, width // 2, height // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

laser_sound = pygame.mixer.Sound("assets/LaserSound.ogg")
explosion_sound = pygame.mixer.Sound("assets/ExplosionSound.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

game_over = True
running = True
while running:
    if game_over:
        game_over = False
        
        show_go_screen()
        
        all_sprites = pygame.sprite.Group()
        marcianos_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()

        all_sprites.add(player)

        MarcX = 60
        MarcY = 0

        for i in range(0,5):
            for j in range(0,11):
                if i == 0:
                    marciano = Marciano("marciano2.png", MarcX, MarcY)
                    all_sprites.add(marciano)
                    marcianos_list.add(marciano)
                elif i == 1 or i == 2:
                    marciano = Marciano("marciano1.png", MarcX, MarcY)
                    all_sprites.add(marciano)
                    marcianos_list.add(marciano)
                else:
                    marciano = Marciano("marciano3.png", MarcX, MarcY)
                    all_sprites.add(marciano)
                    marcianos_list.add(marciano)
                MarcX += 60
            MarcX = 60
            MarcY += 60

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.shoot()
    
    all_sprites.update()
    hits = pygame.sprite.groupcollide(marcianos_list, bullets, True, True)
    for hit in hits:
        explosion_sound.play()
    
    hits = pygame.sprite.spritecollide(player, marcianos_list, True)
    if(hits):
        game_over = True
        
    if(len(marcianos_list.sprites()) == 0):
        game_over = True
        
    screen.fill(black)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
