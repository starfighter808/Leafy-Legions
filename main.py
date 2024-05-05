"""
Leafy Legions Main Module

This module defines the main structure and functionality of the Leafy Legions game. It includes
constants, game initialization, entity management, and the game loop.

@author RELLIS Developments
"""
# Standard Imports
import os
import sys

# Library Imports
import pygame

# Local Imports
from src.managers import ScreenManager, SoundManager

# Initialize Pygame
pygame.init()

# Set up the game window, scaled if needed
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Using common aspect ratio (1124x768)
display: pygame.Surface = pygame.display.set_mode((1120, 720), pygame.SCALED)
pygame.display.set_caption("Leafy Legions")

# Create an instance of ScreenManager
screen_manager = ScreenManager(display)
sound_manager = SoundManager()

# Set the default screen to the Main Menu
screen_manager.set_screen("MainMenuScreen")

# Main game loop
while screen_manager.is_running():

    # Handle Events
    for event in pygame.event.get():

        # If QUIT Event:
        if event.type == pygame.QUIT:
            # Quit current screen, ending the program
            screen_manager.quit()

        # If CLICK Event:
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Send mouse clicks to the current screen to get handled
            if screen_manager.current_screen:
                mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
                screen_manager.current_screen.handle_click_events(mouse_pos)

        # If KEYBOARD Event
        elif event.type == pygame.KEYDOWN:
            key_pressed: int = event.key
            unicode_char: str = event.unicode
            screen_manager.current_screen.handle_key_events(key_pressed, unicode_char)

    # If a screen is running, render the current screen
    if screen_manager.current_screen:
        screen_manager.run_current_screen()

    pygame.display.flip()

    # Use 60 FPS
    # Divide by the game speed (for 2x support)
    pygame.time.delay(60 // screen_manager.game_speed)

# If no screens are being displayed, close pygame and app
pygame.quit()
sys.exit()
