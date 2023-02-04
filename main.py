import pygame
import os
from random import randint
pygame.init()

def file_path(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path

FPS = 40
WIN_WIDTH = 700
WIN_HEIGHT = 500
RED = (200, 0, 0)
GREEN = (0, 255, 0)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load(file_path("fon_shooter.jpg"))
background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))

class GameSprite(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
    def fire(self):
        pass

class Enemy(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)

    def update(self):
        global missed_enemies
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIN_WIDTH - self.rect.width)
            self.speed = randint(1, 3)
            missed_enemies += 1


#*   картинка, х, у, ширина, висота, швидкість
player = Player("garry_sh.png", 300, 400, 100, 70, 5)
enemies = pygame.sprite.Group()

for i in range(5):
    enemy = Enemy(file_path("dementor23.png"), randint(0, WIN_WIDTH - 70), 0, 80, 85, randint(1, 4))
    enemies.add(enemy)

pygame.mixer.music.load("shooter_music.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

missed_enemies = 0
killed_enemies = 0
font = pygame.font.SysFont("arial", 25, 0, 1)
txt_missed = font.render("Пропущено: " + str(missed_enemies), True, RED)
txt_killed = font.render("Влучено: " + str(killed_enemies), True, GREEN)

play = True
game = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if play == True:
        window.blit(background, (0, 0))

        txt_missed = font.render("Пропущено: " + str(missed_enemies), True, RED)
        txt_killed = font.render("Влучено: " + str(killed_enemies), True, GREEN)
        window.blit(txt_killed, (10, 10))
        window.blit(txt_missed, (10, 45))

        player.reset()
        player.update()

        enemies.draw(window)
        enemies.update()

    clock.tick(FPS)
    pygame.display.update()