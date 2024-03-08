"""
Leafy Legions Main Module

This module defines the main structure and functionality of the Leafy Legions game. It includes
constants, game initialization, entity management, and the game loop.

@author RELLIS Developments
"""

# System Imports
import sys
from types import ModuleType

# Library Imports
import pygame

# Local Imports
from entities import Plant, Zombie, SpeedyZombie
from entities import __all__ as all_entities
from managers import GameController

# Constants defining the grid dimensions, zombie properties, and game settings
GRID_WIDTH: int = 9
GRID_HEIGHT: int = 5
GRID_SIZE: int = 125
DAMAGE_PER_HIT: int = 25
DELAY_MS: int = 50
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
RED: tuple[int, int, int] = (255, 0, 0)
BACKGROUND_IMAGE_PATH: str = 'assets/images/background.jpg'
BACKGROUND_MUSIC_PATH: str = 'assets/sounds/backgroundMusic.wav'

# Initialize Pygame
pygame.init()

# Set up the game window
screen: pygame.Surface = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
pygame.display.set_caption("Leafy Legions Test Display")

# Load images and scale them to match the grid size
background_image: pygame.Surface = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))

# Initialize Pygame mixer and load background music
pygame.mixer.init()
pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play()

# Game Management
game_controller = GameController()


def load_and_scale_entity_images(entities_module: ModuleType) -> dict[type, pygame.Surface]:
    """
    Load and scale images for each entity class defined in the entities' module.

    Args:
        entities_module (ModuleType): The module containing entity classes.

    Returns:
        dict[type, pygame.Surface]: A dictionary mapping entity classes to their scaled images.
    """
    scaled_images: dict[type, pygame.Surface] = {}
    for entity_name in all_entities:
        entity_class: type = getattr(entities_module, entity_name)  # Get Class from modules

        # Create an instance of the entity's Class for access to the image attrib
        entity_instance = entity_class(game_controller, 0, 0)

        image_path: str = entity_instance.image
        if image_path:
            scaled_images[entity_class] = pygame.transform.scale(pygame.image.load(image_path), (GRID_SIZE, GRID_SIZE))
    return scaled_images


# Load and scale images for each entity class
entity_images: dict[type, pygame.Surface] = load_and_scale_entity_images(sys.modules['entities'])


def initialize_zombies() -> None:
    """
    Initialize a list of zombies based on predefined positions.
    """
    for i in range(GRID_HEIGHT):
        if i == 1:
            game_controller.add(SpeedyZombie(game_controller, (GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE))
        else:
            game_controller.add(Zombie(game_controller, (GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE))


# Create lists of plants and zombies
initialize_zombies()
zombies: list[Zombie] = game_controller.get_entities(Zombie)
plants: list[Plant] = game_controller.get_entities(Plant)


def draw_grid_and_entities(objs: list[Zombie | Plant]) -> None:
    """
    Draw the grid lines, background, and entities on the game screen.

    Args:
        objs (list): A list of entities to be drawn.
    """
    screen.blit(background_image, (0, 0))
    for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, GRID_HEIGHT * GRID_SIZE))
    for y in range(0, GRID_HEIGHT * GRID_SIZE, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (GRID_WIDTH * GRID_SIZE, y))

    # Sort entities by type: Plant, then Zombie, so that zombies always appear "on top"
    objs.sort(key=lambda objName: isinstance(objName, Zombie))

    for obj in objs:
        image = entity_images.get(type(obj))
        if image:
            screen.blit(image, (obj.x, obj.y))


def display_message(display_surface: pygame.Surface, message: str, font_color: tuple[int, int, int]) -> None:
    """
    Display a message on the game screen.

    Args:
        display_surface (pygame.Surface): The surface to display the message on.
        message (str): The message to be displayed on the screen.
        font_color (tuple[int, int, int]): The color of the font.
    """
    font = pygame.font.Font(None, 36)
    text: pygame.Surface = font.render(message, True, font_color)
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    display_surface.blit(text, text_rect)
    draw_button(display_surface, "Play Again", RED)
    pygame.display.flip()


def draw_button(display_surface: pygame.Surface, message: str, button_color: tuple[int, int, int]) -> None:
    """
    Draws a button on the game screen

    Args:
        display_surface (pygame.Surface): The surface to display the button on.
        message (str): The message to be displayed on the button.
        button_color (tuple[int, int, int]): The color of the button background.
    """
    font = pygame.font.Font(None, 36)
    button_text: pygame.Surface = font.render(message, True, WHITE)
    button_rect = button_text.get_rect(center=(display_surface.get_width() / 2, display_surface.get_height() / 2 + 50))
    pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
    display_surface.blit(button_text, button_rect)


# While pygame is open
while game_controller.get_status('app'):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_controller.set_app_status(False)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # If mouse press while game is not running (play again menu)
            if not game_controller.get_status('game'):
                mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
                play_again_button_rect = pygame.Rect(screen.get_width() / 2 - 54, screen.get_height() / 2 + 36, 110, 26)
                if play_again_button_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.play()
                    initialize_zombies()  # Temporary pre-set zombies until waves are set up
                    zombies: list[Zombie] = game_controller.get_entities(Zombie)
                    plants: list[Plant] = game_controller.get_entities(Plant)
                    game_controller.set_game_status(True)

            # If mouse press while game is running (planting)
            else:
                # Plant a plant at the clicked position if the game is not over
                mouse_x: int
                mouse_y: int
                mouse_x, mouse_y = pygame.mouse.get_pos()

                grid_x: int = mouse_x // GRID_SIZE
                grid_y: int = mouse_y // GRID_SIZE
                existing_plant: bool = any(plant.x == grid_x * GRID_SIZE
                                           and plant.y == grid_y * GRID_SIZE for plant in plants)
                if not existing_plant and (0 <= grid_x < GRID_WIDTH) and (0 <= grid_y < GRID_HEIGHT):
                    # Plant a plant at the clicked position if it's within the grid
                    new_plant = Plant(game_controller, grid_x * GRID_SIZE, grid_y * GRID_SIZE)
                    game_controller.add(new_plant)
                    print(f"New Plant {new_plant.x, new_plant.y}. Health: {new_plant.health}")

    # While the game is running, draw entities, handle zombie movement, and allow zombies to attack
    if game_controller.get_status('game'):
        draw_grid_and_entities(game_controller.get_entities())

        for plant in plants:
            for zombie in zombies:
                if zombie.y == plant.y and zombie.x <= plant.x <= zombie.x + GRID_SIZE:
                    zombie.attack_plant(plant)

        for zombie in zombies:
            zombie.update_position()

        # Check if any zombie go outside the screen
        if any(zombie.x <= -125 for zombie in zombies):
            print("Game Lost")
            game_controller.set_game_status(False)

            # Add a fade-to-black effect when the game is over
            fade_surface = pygame.Surface((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
            for alpha in range(0, 255, 5):
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                pygame.mixer.music.fadeout(500)
                display_message(screen, "Your Legion was defeated", WHITE)
                pygame.display.flip()
                pygame.time.delay(30)

        pygame.display.flip()
        pygame.time.delay(DELAY_MS)

# If the game is not running, quit pygame and close the application
pygame.quit()
sys.exit()
