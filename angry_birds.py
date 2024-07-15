import pygame
import sys
import random
import math

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds")

player_bird_image = pygame.transform.scale(pygame.image.load("player.png"), (60, 60))
enemy_bird_image = pygame.transform.scale(pygame.image.load("enemy.jpg"), (60, 60))
background_image = pygame.transform.scale(pygame.image.load("background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]
        self.dragging = False
        self.drag_start_pos = (0, 0)

    def update(self):
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.centerx = mouse_pos[0]
            self.rect.centery = mouse_pos[1]
        else:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

    def start_drag(self):
        self.dragging = True
        self.drag_start_pos = self.rect.center

    def end_drag(self):
        self.dragging = False
        mouse_pos = pygame.mouse.get_pos()
        direction = math.atan2(self.drag_start_pos[1] - mouse_pos[1], self.drag_start_pos[0] - mouse_pos[0])
        speed = 15
        self.velocity = [speed * math.cos(direction), speed * math.sin(direction)]

    def hit_enemy(self):
        global score
        score += 100

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
score_position = (1260, 80)
score = 0

quit_button_image = pygame.transform.scale(pygame.image.load("quit.jpg"), (80, 50))
refresh_button_image = pygame.transform.scale(pygame.image.load("refresh.png"), (50, 50))

quit_button = Button(button_margin, button_margin, quit_button_image, "quit")
refresh_button = Button(button_margin + quit_button_image.get_width() + button_margin, button_margin, refresh_button_image, "refresh")

clock = pygame.time.Clock()
try_again_counter = 0
max_try_again = 3
level_cleared = False
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif refresh_button.rect.collidepoint(event.pos):
                player_bird.rect.center = (100, SCREEN_HEIGHT // 2)
                player_bird.velocity = [0, 0]
                enemy_birds.empty()
                for _ in range(5):
                    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
                    y = random.randint(50, SCREEN_HEIGHT - 50)
                    enemy_bird = Bird(x, y, enemy_bird_image)
                    enemy_birds.add(enemy_bird)
                level_cleared = False
                game_over = False
                try_again_counter = 0
                score = 0
            elif player_bird.rect.collidepoint(event.pos):
                player_bird.start_drag()

        elif event.type == pygame.MOUSEBUTTONUP:
            if player_bird.dragging:
                player_bird.end_drag()
                if not hits:
                    try_again_counter += 1

    hits = pygame.sprite.spritecollide(player_bird, enemy_birds, True)
    if hits:
        for hit_enemy in hits:
            hit_enemy.hit_enemy()

    for enemy_bird in enemy_birds:
        if enemy_bird.rect.right < 0:
            enemy_bird.rect.left = SCREEN_WIDTH
            enemy_bird.rect.top = random.randint(50, SCREEN_HEIGHT - 50)

    if player_bird.rect.left > SCREEN_WIDTH or player_bird.rect.right < 0 or \
            player_bird.rect.top > SCREEN_HEIGHT or player_bird.rect.bottom < 0:
        player_bird.rect.center = (100, SCREEN_HEIGHT // 2)
        player_bird.velocity = [0, 0]

    screen.blit(background_image, (0, 0))
    player_bird.update()
    screen.blit(player_bird.image, player_bird.rect)
    enemy_birds.update()
    enemy_birds.draw(screen)

    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, score_position)

    screen.blit(quit_button.image, quit_button.rect)
    screen.blit(refresh_button.image, refresh_button.rect)

    if score >= 500:
        level_cleared_text = pygame.font.Font(None, 50).render("LEVEL CLEARED", True, (0, 0, 0))
        text_rect = level_cleared_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(level_cleared_text, text_rect)
        level_cleared = True

    if score == 0 and try_again_counter >= max_try_again:
        game_over_text = pygame.font.Font(None, 50).render("GAME OVER - REPLAY", True, (0, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        game_over = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
