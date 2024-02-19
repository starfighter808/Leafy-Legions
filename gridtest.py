import pygame
import sys

GRID_WIDTH = 9
GRID_HEIGHT = 5
GRID_SIZE = 125
ZOMBIE_HEALTH = 100
ZOMBIE_SPEED = 1
SPEEDY_ZOMBIE_SPEED = 3
DAMAGE_PER_HIT = 25
DELAY_MS = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ZOMBIE_IMAGE_PATH = 'creeper.png'
SPEEDY_ZOMBIE_IMAGE_PATH = 'speedyZombie.png'
BACKGROUND_IMAGE_PATH = 'Background.jpg'
BACKGROUND_MUSIC_PATH = 'backgroundMusic.wav'

pygame.init()

screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
pygame.display.set_caption("Leafy Legions Test Display")

zombie_image = pygame.image.load(ZOMBIE_IMAGE_PATH)
zombie_image = pygame.transform.scale(zombie_image, (GRID_SIZE, GRID_SIZE))
speedy_zombie_image = pygame.image.load(SPEEDY_ZOMBIE_IMAGE_PATH)
speedy_zombie_image = pygame.transform.scale(speedy_zombie_image, (GRID_SIZE, GRID_SIZE))
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))

pygame.mixer.init()

pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
pygame.mixer.music.play(-1)

class Zombie:
    def __init__(self, x, y, health, speed, image):
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.image = image

    def update_position(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.reset_position()

    def reset_position(self):
        self.x = (GRID_WIDTH - 1) * GRID_SIZE

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class SpeedyZombie(Zombie):
    def __init__(self, x, y, health):
        super().__init__(x, y, health, SPEEDY_ZOMBIE_SPEED, speedy_zombie_image)

zombies = []
speedy_zombies = []

for i in range(GRID_HEIGHT):
    if i == 1:
        speedy_zombies.append(SpeedyZombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH))
    else:
        zombies.append(Zombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH, ZOMBIE_SPEED, zombie_image))

def draw_grid(background_image):
    screen.blit(background_image, (0, 0))
    for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, GRID_HEIGHT * GRID_SIZE))
    for y in range(0, GRID_HEIGHT * GRID_SIZE, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (GRID_WIDTH * GRID_SIZE, y))

def damage_zombies(zombies, damage):
    for zombie in zombies:
        zombie.take_damage(damage)

def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(text, text_rect)
    draw_button()
    pygame.display.flip()

def draw_button():
    font = pygame.font.Font(None, 36)
    button_text = font.render("Try Again", True, WHITE)
    button_rect = button_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
    pygame.draw.rect(screen, BLACK, button_rect, border_radius=5)
    screen.blit(button_text, button_rect)

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2, 200, 50)
                if button_rect.collidepoint(mouse_pos):

                    zombies = []
                    speedy_zombies = []
                    for i in range(GRID_HEIGHT):
                        if i == 1:
                            speedy_zombies.append(SpeedyZombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH))
                        else:
                            zombies.append(Zombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH, ZOMBIE_SPEED, zombie_image))
                    game_over = False

    if not game_over:
        draw_grid(background_image)

        for zombie in zombies:
            zombie.update_position()
        for zombie in speedy_zombies:
            zombie.update_position()

        for zombie in zombies:
            zombie.draw(screen)
        for zombie in speedy_zombies:
            zombie.draw(screen)

        if any(zombie.x <= 0 for zombie in zombies) or any(zombie.x <= 0 for zombie in speedy_zombies):
            game_over = True
            display_message("Your Legion was defeated")

        pygame.display.flip()
        pygame.time.delay(DELAY_MS)

pygame.quit()
sys.exit()



