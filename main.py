import pygame, threading, random
from bullet import Bullet
from player import Player
from marciano import Marciano

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

def main() -> None:

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
        hits = pygame.sprite.groupcollide(bullets, marcianos_list, True, True)
        for hit in hits:
            explosion_sound.play()
            marciano = Marciano("marciano3.png", hit.rect.x, hit.rect.y)
            all_sprites.add(marciano)
            marcianos_list.add(marciano)

        hits = pygame.sprite.spritecollide(player, marcianos_list, False)
        if hits:
            game_over = True

        screen.fill(black)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':

    main()