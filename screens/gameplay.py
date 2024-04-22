"""
Leafy Legions: GameplayScreen

This module contains the GameplayScreen class
for managing the game itself when running
"""
# Standard Imports
import math
import random
import sys
from types import ModuleType
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from entities import Plant, Projectile, SpeedyZombie, Zombie
from entities import __all__ as all_entities
from managers import ColorManager, GameManager
from screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import ScreenManager

# CONSTANTS
GRID_WIDTH: int = 9
GRID_HEIGHT: int = 5
GRID_SIZE: int = 114
PLANT_COST: int = 15


def scale_background(img: str) -> pygame.Surface:
    """
    Scales the image provided to fit the application

    Args:
        img (str): The name of the image file in "/assets/images/"

    Returns:
         pygame.Surface: The scaled image as a pygame Surface
    """
    scaled_img: pygame.Surface = pygame.image.load(f"./assets/images/{img}")
    scaled_img = pygame.transform.scale(scaled_img, (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    return scaled_img


class GameplayScreen(BaseScreen):
    """
    The GameplayScreen renders the game itself
    """

    def __init__(self, screen_manager: 'ScreenManager', display: pygame.Surface) -> None:
        """
        Initialize the Gameplay screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (pygame.Surface): The pygame display
        """
        super().__init__(screen_manager, display, title="Leafy Legions: Gameplay")

        # Setup GameManager, entity management attributes, & ColorManager
        self.game_manager = GameManager()
        self.zombies = self.game_manager.get_entities(Zombie)
        self.plants = self.game_manager.get_entities(Plant)
        self.projectiles = self.game_manager.get_entities(Projectile)
        self.colors = ColorManager()

        # Load all images
        self.background_img = scale_background('background.jpg')
        self.entity_imgs = self.load_and_scale_entity_images(sys.modules['entities'])

        # When all assets are loaded, start the game
        self.game_manager.set_game_status(True)

        pygame.mixer.music.load('./assets/music/gameplay.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.05)

    def load_and_scale_entity_images(self, entities_module: ModuleType) -> dict[type, list[pygame.Surface]]:
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
            entity_instance = entity_class(self.game_manager, 0, 0)

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

    def begin_wave(self) -> None:
        """
        Start a new wave of zombies after
        the current one has ended
        """

        # Remove all projectiles
        self.game_manager.clear_entities(Projectile)

        wave = self.game_manager.get_wave()

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

        # For any room left in the list, fill with regular Zombies
        remaining_zombies = num_zombies - len(zombie_roles)
        zombie_roles.extend([Zombie] * remaining_zombies)
        for _ in range(num_zombies):
            # Choose a random zombie based on choices available
            role = random.choice(zombie_roles)
            # Create a zombie spawn position with a random row
            x = ((GRID_WIDTH - 1) * GRID_SIZE) + 75 + random.choice(list(range(-50, 126, 20)))
            y = random.randint(0, 4) * GRID_SIZE
            new_zombie = role(self.game_manager, x, y)
            self.game_manager.add(new_zombie)
            print((y) // GRID_SIZE)

    def draw_grid_and_entities(self, objs: list[Zombie | Plant | Projectile]) -> None:
        """
        Draw the grid lines, background, and entities on the game screen.

        Args:
            objs (List): A list of entities to be drawn.
        """
        # Draw background
        self.display.blit(self.background_img, (0, 100))

        # Draw grid
        for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(self.display, self.colors.BLACK, (x, 100), (x, GRID_HEIGHT * GRID_SIZE + 100))
        for y in range(100, GRID_HEIGHT * GRID_SIZE + 100, GRID_SIZE):
            pygame.draw.line(self.display, self.colors.BLACK, (0, y), (GRID_WIDTH * GRID_SIZE, y))

        # Sort entities by type: Plant, then Zombie, so that zombies always appear "on top"
        objs.sort(key=lambda objName: isinstance(objName, Zombie))
        current_time = pygame.time.get_ticks()
        for obj in objs:
            images = self.entity_imgs.get(type(obj))
            if images:
                try:
                    cell_center_x = obj.x + (GRID_SIZE - obj.image_size[0]) / 2
                    cell_center_y = obj.y + 100 + (GRID_SIZE - obj.image_size[1]) / 2

                    # Assign a random animation offset to each entity
                    if not hasattr(obj, 'animation_offset'):
                        obj.animation_offset = random.randint(0, 10000)

                    # Calculate index of the image to display based on time
                    image_index = ((current_time + obj.animation_offset) // 500) % len(images)
                    self.display.blit(images[image_index], (cell_center_x, cell_center_y))
                except (AttributeError, IndexError):
                    self.display.blit(images[0], (obj.x, obj.y + 100))

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        mouse_x: int = mouse_pos[0]
        mouse_y: int = mouse_pos[1]
        grid_x: int = mouse_x // GRID_SIZE
        grid_y: int = (mouse_y - 100) // GRID_SIZE

        existing_plant: bool = any(plant.x == grid_x * GRID_SIZE
                                   and plant.y == grid_y * GRID_SIZE for plant in self.plants)

        if not existing_plant and (0 <= grid_x < GRID_WIDTH) and (0 <= grid_y < GRID_HEIGHT):
            # Plant a plant at the clicked position if it's within the grid
            if self.game_manager.get_coins() >= PLANT_COST:
                self.game_manager.remove_coins(PLANT_COST)
                new_plant = Plant(self.game_manager, grid_x * GRID_SIZE, grid_y * GRID_SIZE)
                self.game_manager.add(new_plant)
                print(f"New Plant {new_plant.x, new_plant.y}. Health: {new_plant.health}")
            else:
                self.game_manager.play_sound('error.mp3', 0.15)
        else:
            self.game_manager.play_sound('error.mp3', 0.15)

    def render(self) -> None:
        self.display.fill(self.colors.BROWN)
        self.draw_grid_and_entities(self.game_manager.get_entities())
        self.display_message(message=f"Coins: {self.game_manager.get_coins()}",
                             font_color=self.colors.WHITE,
                             text_position=(15, 20),
                             text_align="topleft"
                             )
        self.display_message(message=f"Wave: {self.game_manager.get_wave() - 1}",
                             font_color=self.colors.WHITE,
                             text_position=(15, 50),
                             text_align="topleft"
                             )

        # If no zombies are on the board, spawn new ones + update wave
        if not self.game_manager.get_entities(Zombie):
            self.begin_wave()
            self.game_manager.update_wave()

        for plant in self.plants:
            for zombie in self.zombies:
                if zombie.y == plant.y:
                    # If a Zombie is inside the Plant's cell
                    if zombie.x <= plant.x <= zombie.x + GRID_SIZE:
                        zombie.attack_plant(plant)

                    # Ensure the zombie is visible on the board, in front of the plant
                    if plant.x <= zombie.x <= self.display.get_width() - 30:
                        plant.shoot_projectile()

        for zombie in self.zombies:
            zombie.update_position()
            for projectile in self.projectiles:
                if zombie.y == projectile.y and zombie.x <= projectile.x <= zombie.x + GRID_SIZE:
                    projectile.attack_zombie(zombie)
        for projectile in self.projectiles:
            projectile.update_position()

        # Check if any zombie go outside the screen
        if any(zombie.x <= -GRID_SIZE for zombie in self.zombies):
            self.game_manager.set_game_status(False)

            # Add a fade-to-black effect when the game is over
            fade_surface = pygame.Surface(self.display.get_size())
            fade_surface.fill(self.colors.BROWN)
            fade_surface.set_alpha(0)
            for alpha in range(0, 150, 5):
                fade_surface.set_alpha(alpha)
                self.display.blit(fade_surface, (0, 0))
                pygame.mixer.music.fadeout(500)
                pygame.display.flip()
                pygame.time.delay(15)

            self.screen_manager.set_screen("YouLostScreen")
