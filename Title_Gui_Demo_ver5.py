import pygame
import sys
import os
#Music allower
import pygame.mixer

# Initializes Pygame
pygame.init()

# Sets up the window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Western game? I thought you said Wheat earn Game!")

#Music Set up
pygame.mixer.init()
pygame.mixer.music.load('G_Valley.mp3')
pygame.mixer.music.play(-1)  # -1 plays the music on loop

# Defines colors
RED = (255, 0, 0)
BROWN = (150, 75, 0)
ORANGE = (255, 165, 0)

screen.fill(BROWN)

#Learn where to place the image
temp_image = pygame.image.load('Temp.png')
temp_rect = temp_image.get_rect(center=(400, 200))  # Adjust after being able to see the title running
screen.blit(temp_image, temp_rect)

# Sets up fonts, will have to decide on which one later
font = pygame.font.Font(None, 36)

# Create texts objects for the options
#Remember how to put an image for the title up, picture with words on it
title_text = font.render("What are you looking at?", True, RED)
start_text = font.render("Start", True, ORANGE)
options_text = font.render("Options", True, ORANGE)
credits_text = font.render("Credits", True, ORANGE)
quit_text = font.render("Quit", True, ORANGE)

# Positioning the text objects
start_rect = start_text.get_rect(center=(400, 300))
options_rect = options_text.get_rect(center=(400, 350))#
credits_rect = credits_text.get_rect(center=(400, 400))
quit_rect = quit_text.get_rect(center=(400, 450))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                print("Start selected")
                # Add code to open the game file when its ready
            elif options_rect.collidepoint(event.pos):
                print("Options selected")
                os.system("open options")  # Opens the options file
            elif credits_rect.collidepoint(event.pos):
                print("Credits Selected")
                os.system("open Credits")  # Opens the Credits file
            elif quit_rect.collidepoint(event.pos):
                print("Quit selected")
                pygame.quit()
                sys.exit()

    #moved before the temp image screen.fill(BROWN)
    screen.blit(start_text, start_rect)
    screen.blit(options_text, options_rect)
    screen.blit(credits_text, credits_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()