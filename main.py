"""
Leafy Legions Main Module

This module defines the main structure and functionality of the Leafy Legions game. It includes
constants, game initialization, entity management, and the game loop.

@author RELLIS Developments
"""
# System Imports
import sys
import random
import math
from types import ModuleType

# Library Imports
import pygame

# Local Imports
from entities import Plant, Zombie, SpeedyZombie, Projectile #, RosePlant, HulkZombie  
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
BACKGROUND_MUSIC_PATH: str = 'assets/sounds/backgroundmusic.mp3'
PLANT_COST = 15

# Initialize Pygame
pygame.init()

# Set up the game window
screen: pygame.Surface = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
pygame.display.set_caption("Leafy Legions")

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


def load_and_scale_entity_images(entities_module: ModuleType) -> dict[type, list[pygame.Surface]]:
    """
    Load and scale images for each entity class defined in the entities' module.

    Args:
        entities_module (ModuleType): The module containing entity classes.

    Returns:
        dict[type, list[pygame.Surface]]: A dictionary mapping entity classes to their scaled images.
    """
    scaled_images: dict[type, list[pygame.Surface]] = {}
    for entity_name in all_entities:
        entity_class: type = getattr(entities_module, entity_name)  # Get Class from modules

        # Create an instance of the entity's Class for access to the image attrib
        entity_instance = entity_class(game_controller, 0, 0)

        image_paths: list = entity_instance.image
        if image_paths:
            images = []
            for image_path in image_paths:
                try:
                    image_size = entity_instance.image_size
                    images.append(pygame.transform.scale(pygame.image.load(image_path), image_size))
                except AttributeError:
                    images.append(pygame.transform.scale(pygame.image.load(image_path), (GRID_SIZE, GRID_SIZE)))
            scaled_images[entity_class] = images

    return scaled_images


# Load and scale images for each entity class
entity_images: dict[type, list[pygame.Surface]] = load_and_scale_entity_images(sys.modules['entities'])
game_controller.set_game_status(True)


def begin_wave() -> None:
    """
    Start the wave
    """

    # Remove all projectiles on the board after each wave
    game_controller.clear_entities(Projectile)
    wave = game_controller.get_wave()

    # For Waves 1-3, number of zombies = wave number
    if wave <= 3:
        num_zombies = wave
    else:
        # For Wave 4+, exponentially increase zombie count
        num_zombies = wave + math.ceil(3 + math.log(wave, 4))

    zombie_roles = []

    # For Wave 5+, start adding SpeedyZombies
    if wave >= 5:
        weight_speedy = min((wave - 4) * 0.1, 1.0)  # Weight SpeedyZombies into the mix
        zombie_roles.extend([SpeedyZombie] * int(num_zombies * weight_speedy))
    
    # For Wave 10+, start adding Hulking Zombies
    #if wave >= 10:
        #weight_Hulking = min((wave - 9) * 0.1, 1.0)  # Weight HulkingZombies into the mix
        #zombie_roles.extend([HulkZombie] * int(num_zombies * weight_Hulking))

    # For any room left in the array, fill with regular Zombies
    remaining_zombies = num_zombies - len(zombie_roles)
    zombie_roles.extend([Zombie] * remaining_zombies)

    for _ in range(num_zombies):
        # Choose a random zombie based on choices available
        role = random.choice(zombie_roles)

        # Create a zombie spawn position with a random row
        x = ((GRID_WIDTH - 1) * GRID_SIZE) + 75 + random.choice(list(range(-50, 126, 20)))
        y = random.randint(0, 4) * GRID_SIZE

        new_zombie = role(game_controller, x, y)
        game_controller.add(new_zombie)


def draw_grid_and_entities(objs: list[Zombie | Plant | Projectile]) -> None:
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

    current_time = pygame.time.get_ticks()

    for obj in objs:
        images = entity_images.get(type(obj))
        if images:
            try:
                cell_center_x = obj.x + (GRID_SIZE - obj.image_size[0]) / 2
                cell_center_y = obj.y + (GRID_SIZE - obj.image_size[1]) / 2

                # Assign a random animation offset to each entity
                if not hasattr(obj, 'animation_offset'):
                    obj.animation_offset = random.randint(0, 10000)

                # Calculate index of the image to display based on time
                image_index = ((current_time + obj.animation_offset) // 500) % len(images)
                screen.blit(images[image_index], (cell_center_x, cell_center_y))

            except (AttributeError, IndexError):
                screen.blit(images[0], (obj.x, obj.y))


def display_message(message: str, font_color: tuple[int, int, int],
                    text_position: tuple[float, float]) -> None:
    """
    Display a message on the game screen.

    Args:
        message (str): The message to be displayed on the screen.
        font_color (tuple[int, int, int]): The color of the font.
        text_position (tuple[float, float]): The position of the text (x, y).
    """
    font = pygame.font.Font(None, 36)
    text: pygame.Surface = font.render(message, True, font_color)
    text_rect = text.get_rect(center=text_position)
    screen.blit(text, text_rect)


def draw_button(message: str, button_color: tuple[int, int, int],
                button_position: tuple[float, float]) -> None:
    """
    Draws a button on the game screen

    Args:
        message (str): The message to be displayed on the button.
        button_color (tuple[int, int, int]): The color of the button background.
        button_position (tuple[float, float]): The position of the button (x, y).
    """
    font = pygame.font.Font(None, 36)
    button_text: pygame.Surface = font.render(message, True, WHITE)
    button_rect = button_text.get_rect(center=button_position)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
    screen.blit(button_text, button_rect)


# While pygame is open
while game_controller.get_status('app'):
    zombies: list[Zombie] = game_controller.get_entities(Zombie)
    plants: list[Plant] = game_controller.get_entities(Plant)
    projectiles: list[Projectile] = game_controller.get_entities(Projectile)
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
                    begin_wave()
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
                    if game_controller.get_coins() >= PLANT_COST:
                        game_controller.remove_coins(PLANT_COST)
                        new_plant = Plant(game_controller, grid_x * GRID_SIZE, grid_y * GRID_SIZE)
                        game_controller.add(new_plant)
                        print(f"New Plant {new_plant.x, new_plant.y}. Health: {new_plant.health}")
                    else:
                        game_controller.play_sound('error.mp3', 0.15)
                else:
                    game_controller.play_sound('error.mp3', 0.15)

    # While the game is running, draw entities, handle zombie movement, and allow zombies to attack
    if game_controller.get_status('game'):
        draw_grid_and_entities(game_controller.get_entities())
        display_message(f"Coins: {game_controller.get_coins()}", WHITE, (60, 25))
        display_message(f"Wave: {game_controller.get_wave() - 1}", WHITE, (60, 55))

        if not game_controller.get_entities(Zombie):
            begin_wave()
            game_controller.update_wave()

        for plant in plants:
            for zombie in zombies:
                if zombie.y == plant.y:
                    if zombie.x <= plant.x <= zombie.x + GRID_SIZE:
                        zombie.attack_plant(plant)

                    # Ensure the zombie is visible on the board, in front of the plant
                    if plant.x <= zombie.x <= 1100:
                        plant.shoot_projectile()

        for zombie in zombies:
            zombie.update_position()

            for projectile in projectiles:
                if zombie.y == projectile.y and zombie.x <= projectile.x <= zombie.x + GRID_SIZE:
                    projectile.attack_zombie(zombie)

        for projectile in projectiles:
            projectile.update_position()

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
                display_message("Your Legion was defeated", WHITE, (screen.get_width() / 2, screen.get_height() / 2))
                draw_button("Play Again", RED, (screen.get_width() / 2, screen.get_height() / 2 + 50))
                pygame.display.flip()
                pygame.time.delay(30)

        pygame.display.flip()
        pygame.time.delay(DELAY_MS)

# If the game is not running, quit pygame and close the application
pygame.quit()
sys.exit()
