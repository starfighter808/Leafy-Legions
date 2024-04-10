import pygame
import random

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Tracker")

# Fonts
font = pygame.font.SysFont(None, 36)

# Initialize variables
score = 0

# Game loop
def game():
    global score

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if a zombie is killed (fake zombie kill by pressing something)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score += 1

        # Display the score in a box in the top right corner
        pygame.draw.rect(screen, BLACK, (WIDTH - 150, 10, 140, 50))
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (WIDTH - 140, 20))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

game()