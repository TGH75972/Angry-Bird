import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds")

player_bird_image = pygame.transform.scale(pygame.image.load("player.png"), (60, 60))
enemy_bird_image = pygame.transform.scale(pygame.image.load("enemy.jpg"), (60, 60))
background_image = pygame.transform.scale(pygame.image.load("background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
quit_button_image = pygame.transform.scale(pygame.image.load("quit.jpg"), (80, 50))
refresh_button_image = pygame.transform.scale(pygame.image.load("refresh.png"), (50, 50))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, action):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

player_bird = Bird(100, SCREEN_HEIGHT // 2, player_bird_image)

enemy_birds = pygame.sprite.Group()
for _ in range(5):
    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    enemy_bird = Bird(x, y, enemy_bird_image)
    enemy_birds.add(enemy_bird)

button_margin = 10
quit_button = Button(button_margin, button_margin, quit_button_image, "quit")
refresh_button = Button(button_margin + quit_button_image.get_width() + button_margin, button_margin, refresh_button_image, "refresh")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background_image, (0, 0))
    screen.blit(player_bird.image, player_bird.rect)
    enemy_birds.draw(screen)
    screen.blit(quit_button.image, quit_button.rect)
    screen.blit(refresh_button.image, refresh_button.rect)

    pygame.display.flip()

pygame.quit()
