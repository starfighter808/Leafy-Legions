#Pressing the 'p' key will toggle between pausing and unpausing the game.
#Pressing the 'q' key will quit the game.
#The game logic and drawing are only executed when the game is not paused.
import pygame
import sys

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pause, Unpause, Quit Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game loop variables
clock = pygame.time.Clock()
is_paused = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pause/unpause the game
                is_paused = not is_paused
            if event.key == pygame.K_q:  # Quit the game
                running = False

    screen.fill(WHITE)

    if not is_paused:
        # Game logic and drawing here
        pygame.draw.rect(screen, BLACK, (300, 200, 200, 200))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()


