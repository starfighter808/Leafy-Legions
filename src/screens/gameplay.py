"""
Leafy Legions: GameplayScreen

This module contains the GameplayScreen class
for managing the game itself when running
"""
# Standard Imports
import inspect
from enum import Enum
import random
import os
import sys
from types import ModuleType
from typing import TYPE_CHECKING

# Library Imports
import pygame
from pygame import Surface, SurfaceType

# Local Imports
from src import entities
from src.constants import GRID_WIDTH, GRID_SIZE, GRID_HEIGHT, GRID_OFFSET
from src.entities import Plant, Projectile, Zombie, Shovel
from src.entities import __all__ as all_entities
from src.managers import ColorManager, GameManager, WaveManager
from src.screens import BaseScreen

Entity = Zombie | Plant | Projectile | Shovel

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import ScreenManager


def scale_background(img: str) -> Surface:
    """
    Scales the image provided to fit the application

    Args:
        img (str): The name of the image file in "/src/assets/images/screens/"

    Returns:
         Surface: The scaled image as a pygame Surface
    """
    if getattr(sys, 'frozen', False):
        base_path = os.path.join(sys._MEIPASS, f"src/assets/images/screens/{img}")
    else:
        base_path = f"src/assets/images/screens/{img}"
    scaled_img: Surface = pygame.image.load(base_path)
    scaled_img = pygame.transform.scale(scaled_img, (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    return scaled_img


def load_and_scale_entity_images(entities_module: ModuleType) -> dict[type, list[Surface | SurfaceType]]:
    """
    Load and scale images for each entity class defined in the entities' module.

    Args:
        entities_module (ModuleType): The module containing entity classes.

    Returns:
        dict[type[Entity], list[Surface]]: A dictionary mapping entity classes to their scaled images.
    """
    scaled_images: dict[type, list[Surface]] = {}
    for entity_name in all_entities:
        entity_class: type = getattr(entities_module, entity_name)  # Get Class from modules

        # Create an instance of the entity's Class for access to the image attrib
        entity_instance = entity_class(None, 0, 0)

        image_paths: list = entity_instance.attributes["images"]
        if image_paths:
            images = []
            for image_path in image_paths:
                if getattr(sys, 'frozen', False):
                    base_path = os.path.join(sys._MEIPASS, f"src/assets/images/entities/{image_path}")
                else:
                    base_path = f"src/assets/images/entities/{image_path}"
                try:
                    image_size = entity_instance.image_size
                    images.append(pygame.transform.scale(pygame.image.load(base_path), image_size))
                except AttributeError:
                    images.append(pygame.transform.scale(pygame.image.load(base_path), (GRID_SIZE, GRID_SIZE)))
            scaled_images[entity_class] = images

    return scaled_images


class GameState(Enum):
    """
    Enum for the different states of the game
    """
    PLAYING = 1
    PAUSED = 2
    LOST = 3


class GameplayScreen(BaseScreen):
    """
    The GameplayScreen renders the game itself
    """

    def __init__(self, screen_manager: 'ScreenManager', display: Surface) -> None:
        """
        Initialize the Gameplay screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (Surface): The pygame display
        """
        super().__init__(screen_manager, display, title="Leafy Legions: Gameplay")

        # Setup GameManager, WaveManager, entity management attributes, & ColorManager
        self.game_manager = GameManager(self.sound_manager)
        self.wave_manager = WaveManager(self.game_manager)
        self.zombies = self.game_manager.get_entities(Zombie)
        self.plants = self.game_manager.get_entities(Plant)
        self.projectiles = self.game_manager.get_entities(Projectile)
        self.colors = ColorManager()

        # Load all images
        self.background_img = scale_background('game_background.jpg')
        self.entity_imgs = load_and_scale_entity_images(sys.modules['src.entities'])

        # Set the game state to playing
        self.game_state = GameState.PLAYING
        self.sound_manager.play_music('gameplay.mp3')

        # Create a held item
        # Can be any Entity (Plant/Shovel) or None if no item is held
        self.held_item: type[Entity] | None = None

        # Create top bar: plant buttons + toolbar buttons
        self.create_plant_buttons()
        self.create_toolbar_buttons()

        # Create pause screen buttons
        self.return_button = None
        self.quit_button = None

    def get_button_colors(self, condition) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        """
        Get the button colors based on the condition.

        Returns:
            tuple[tuple[int, int, int], tuple[int, int, int]]: The button color and hover color.
        """
        if condition:
            return self.colors.LIGHT_RED, self.colors.RED
        return self.colors.GREEN, self.colors.LIGHT_BLUE

    def create_toolbar_buttons(self) -> None:
        """
        Create the toolbar buttons on the screen.
        """
        self.toolbar_buttons = [
            {"filename": 'icons/pause.png'},
            {"filename": 'icons/volume.png'},
            {"filename": 'icons/fast_forward.png'},
            {"filename": 'icons/shovel.png'}
        ]
        self.toolbar_button_size = (50, 50)

        btn_padding = 70
        btn_x = self.display.get_width() - (btn_padding * len(self.toolbar_buttons))
        btn_y = 25

        for (index, button_info) in enumerate(self.toolbar_buttons):
            button_info["position"] = (btn_x + (btn_padding * index), btn_y)

    def create_plant_buttons(self) -> None:
        """
        Create the plant buttons on the screen.
        """
        self.plant_buttons = []
        self.plant_button_size = (130, 75)

        # Create a list of all Plant classes
        plant_classes = [cls for name, cls in inspect.getmembers(entities, inspect.isclass) if issubclass(cls, Plant)]

        # Create instances of each plant class to access their cost, then sort by cost
        self.plant_instances = [(plant_class(None, 0, 0), plant_class) for plant_class in plant_classes]
        self.plant_instances = sorted(self.plant_instances, key=lambda instance: instance[0].cost)

        # Create buttons for each plant
        for i, (plant_instance, _) in enumerate(self.plant_instances):
            button_position = (50 + self.plant_button_size[0] + i * 160, 15)
            self.plant_buttons.append({
                "name": plant_instance.attributes["name"],  # The name of the plant
                "cost": plant_instance.cost,  # The cost of the plant
                "color": self.colors.GREEN,
                "hover_color": self.colors.LIGHT_BLUE,
                "position": button_position,  # Set button position
            })
            print(f"Plant {plant_instance.attributes['name']} button created at {button_position}")

    def draw_background_with_grid(self) -> None:
        """
        Draw the background with grid lines on the screen.
        """
        self.display.blit(self.background_img, (0, GRID_OFFSET))
        for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(self.display, self.colors.BLACK, (x, GRID_OFFSET),
                             (x, GRID_HEIGHT * GRID_SIZE + GRID_OFFSET))
        for y in range(GRID_OFFSET, GRID_HEIGHT * GRID_SIZE + GRID_OFFSET, GRID_SIZE):
            pygame.draw.line(self.display, self.colors.BLACK, (0, y), (GRID_WIDTH * GRID_SIZE, y))

    def draw_entities(self, objs: list[Entity]) -> None:
        """
        Draw the game entities on the screen.

        Args:
            objs (list[Entity]): List of game entities to draw.
        """
        # Sort objects so that Zombie is on top
        objs.sort(key=lambda objName: isinstance(objName, Zombie))
        current_time = pygame.time.get_ticks()

        # Attempt to draw each entity
        for obj in objs:
            images = self.entity_imgs.get(type(obj))
            if not images:
                continue
            try:
                self.draw_entity(obj, images, current_time)
            except (AttributeError, IndexError):
                continue

    def draw_entity(self, obj: Entity, images: list[Surface], current_time: int):
        """
        Draw a single game entity on the screen.

        Args:
            obj (Entity): The game entity to draw.
            images (list[Surface]): The images to use for drawing the entity.
            current_time (int): The current game time.
        """
        # If the entity has no image size, match GRID_SIZE
        if not hasattr(obj, 'image_size'):
            obj.image_size = (GRID_SIZE, GRID_SIZE)

        # Handle animations, if any
        if not hasattr(obj, 'animation_offset'):
            obj.animation_offset = random.randint(0, 10000)
        image_index = ((current_time + obj.animation_offset) // (500 // self.screen_manager.game_speed)) % len(images)

        # Display the entity at the center of the cell
        cell_center_x = obj.x + (GRID_SIZE - obj.image_size[0]) / 2
        cell_center_y = obj.y + GRID_OFFSET + (GRID_SIZE - obj.image_size[1]) / 2
        self.display.blit(images[image_index], (cell_center_x, cell_center_y))

    def reset_plant_buttons(self) -> None:
        """
        Resets the color of all plant buttons to None.
        """
        for button_info in self.plant_buttons:
            button_info["color"] = self.colors.GREEN
            button_info["hover_color"] = self.colors.LIGHT_BLUE

    def handle_no_play_buttons(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle return/quit buttons when the game is paused/lost.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.
        """
        if self.return_button and self.return_button.collidepoint(mouse_pos):
            self.sound_manager.toggle_music()
            if self.game_state is GameState.LOST:
                self.sound_manager.reset()
                self.screen_manager.set_screen("GameplayScreen")
            self.quit_button = None
            self.return_button = None
            self.game_state = GameState.PLAYING
        elif self.quit_button and self.quit_button.collidepoint(mouse_pos):
            self.screen_manager.game_speed = 1
            self.sound_manager.reset()
            self.screen_manager.set_screen("MainMenuScreen")

    def handle_plant_button_clicks(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle plant button clicks.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.
        """
        for button_info, (_, plant_class) in zip(self.plant_buttons, self.plant_instances):
            plant_class: type[Plant]
            button_rect = pygame.Rect(button_info["position"], self.plant_button_size)

            if button_rect.collidepoint(mouse_pos) and self.game_manager.get_coins() >= button_info["cost"]:
                if self.held_item == plant_class:
                    self.held_item = None
                    self.reset_plant_buttons()
                else:
                    self.held_item = plant_class
                    button_info["color"] = self.colors.LIGHT_RED
                    button_info["hover_color"] = self.colors.RED
            else:
                button_info["color"] = self.colors.GREEN
                button_info["hover_color"] = self.colors.LIGHT_BLUE

    def handle_toolbar_button_clicks(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle toolbar button clicks.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.
        """
        for button_info in self.toolbar_buttons:
            button_rect = pygame.Rect((button_info["position"], self.toolbar_button_size))

            if not button_rect.collidepoint(mouse_pos):
                continue

            # Go through each toolbar button and perform actions based on the filename
            self.reset_plant_buttons()
            match button_info["filename"]:
                case 'icons/pause.png':
                    self.held_item = None
                    self.game_state = GameState.PAUSED
                    self.sound_manager.toggle_music()
                case 'icons/volume.png':
                    self.held_item = None
                    self.sound_manager.mute_sounds()
                case 'icons/fast_forward.png':
                    self.held_item = None
                    self.screen_manager.game_speed = 2 if self.screen_manager.game_speed == 1 else 1
                case 'icons/shovel.png':
                    # If we are already holding the shovel, get rid of it
                    if self.held_item and issubclass(self.held_item, Shovel):
                        self.held_item = None
                    # Otherwise, set the held item to the shovel
                    else:
                        self.held_item = Shovel

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the gameplay screen.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.
        """
        super().handle_click_events(mouse_pos)
        grid_x: int = mouse_pos[0] // GRID_SIZE
        grid_y: int = (mouse_pos[1] - GRID_OFFSET) // GRID_SIZE

        click_in_grid: bool = (0 <= grid_x < GRID_WIDTH) and (0 <= grid_y < GRID_HEIGHT)

        # If the game is paused/lost, handle return/quit buttons
        if self.game_state is not GameState.PLAYING:
            self.handle_no_play_buttons(mouse_pos)
            return  # If the game is paused/lost, do not continue

        # Handle plant button clicks
        self.handle_plant_button_clicks(mouse_pos)
        self.handle_toolbar_button_clicks(mouse_pos)

        cell_x, cell_y = (grid_x * GRID_SIZE), (grid_y * GRID_SIZE)

        # If not clicking in grid or not holding something, do nothing
        if not click_in_grid or not self.held_item:
            return

        # If holding a shovel, remove the plant in that cell
        if issubclass(self.held_item, Shovel):
            for plant in self.plants:
                if plant.x != cell_x or plant.y != cell_y:
                    continue
                self.game_manager.remove(plant)
                self.game_manager.add_coins(plant.cost // 2)
                self.held_item = None
                break  # Stop looping through plants after it was removed
            else:
                # Throw an error if no plant was found in that cell
                self.throw_error()
            return

        # Throw an error if there's already a plant in that cell
        if any(plant.x == cell_x and plant.y == cell_y for plant in self.plants):
            self.throw_error()
            return

        # Attempt to create the entity
        # Throw an error if the player does not have enough coins
        new_entity = self.held_item(self.game_manager, cell_x, cell_y)
        if self.game_manager.get_coins() < new_entity.cost:
            self.throw_error()
            return

        # Otherwise, add the entity to the game_manager and remove the cost from the player's coins
        self.game_manager.add(new_entity)
        self.game_manager.remove_coins(new_entity.cost)
        print(f"New {self.held_item.__name__} {new_entity.x, new_entity.y}. Health: {new_entity.health}")
        self.held_item = None

    def throw_error(self) -> None:
        """
        Resets the held item & plant buttons, then throws an error sound.
        """
        self.held_item = None
        self.reset_plant_buttons()
        self.sound_manager.play_sound('error.mp3', 0.15)

    def render_held_item(self, item_image: Surface) -> None:
        """
        Renders the held item at the mouse cursor.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.display.blit(item_image,
                          (mouse_pos[0] - item_image.get_width() // 2, mouse_pos[1] - item_image.get_height() // 2))

    def render_plant_buttons(self) -> None:
        """
        Render the plant buttons on the screen.
        """
        for button_info in self.plant_buttons:

            # Disable buttons if user does not have enough coins
            if self.game_manager.get_coins() < button_info["cost"]:
                button_color = self.colors.GRAY
                hover_color = self.colors.GRAY
            else:
                button_color = button_info["color"]
                hover_color = button_info["hover_color"]

            # Remove hover effects when game is paused/lost
            if self.game_state is not GameState.PLAYING:
                hover_color = button_color

            self.display_button(
                message=button_info["name"],
                button_position=button_info["position"],
                button_color=button_color,
                hover_color=hover_color,
                button_size=self.plant_button_size,
                offset_text=(0, -8),  # Move text up slightly to fit cost under it
                font_size=36
            )

            # Add cost within the button position, slightly lower than the current text
            cost_position = (
                button_info["position"][0] + (self.plant_button_size[0] // 2), button_info["position"][1] + 52
            )

            self.display_message(
                message=f"Cost: {button_info['cost']}",
                font_color=self.colors.WHITE,
                text_position=cost_position,
                text_align="center",
                font_size=24
            )

    def render_toolbar_buttons(self) -> None:
        """
        Render the toolbar buttons on the screen.
        """
        for (button_info) in self.toolbar_buttons:
            # Set all the buttons to their respective colors, based on condition
            button_info["colors"] = self.get_button_colors(
                button_info["filename"] == 'icons/pause.png' and self.game_state is GameState.PAUSED or
                button_info["filename"] == 'icons/volume.png' and self.sound_manager.muted or
                button_info["filename"] == 'icons/fast_forward.png' and self.screen_manager.game_speed == 2 or
                button_info["filename"] == 'icons/shovel.png' and self.held_item and issubclass(self.held_item, Shovel)
            )

            # Remove hover effects when game is paused/lost
            hover_color = button_info["colors"][1]
            if self.game_state is not GameState.PLAYING:
                hover_color = button_info["colors"][0]

            # Draw the button
            self.display_button_image(
                image_filename=button_info["filename"],
                background_color=button_info["colors"][0],
                hover_color=hover_color,
                image_position=button_info["position"],
                image_size=self.toolbar_button_size
            )

    def render_entities(self) -> None:
        """
        Render the entities on the screen.
        """
        for plant in self.plants:
            for zombie in self.zombies:
                if zombie.y == plant.y:
                    # If a Zombie is inside the Plant's cell
                    if zombie.x <= plant.x <= zombie.x + GRID_SIZE:
                        zombie.attack_plant(plant)

                    # Ensure the zombie is visible on the board, in front of the plant
                    visible_distance = self.display.get_width() - 30
                    if plant.x <= zombie.x <= visible_distance:
                        plant.shoot_projectile()

        for zombie in self.zombies:
            zombie.update_position()
            zombie.collided_with_plant = False
            for projectile in self.projectiles:
                if zombie.y == projectile.y and zombie.x <= projectile.x <= zombie.x + GRID_SIZE:
                    projectile.attack_zombie(zombie)
        for projectile in self.projectiles:
            projectile.update_position()

    def render_pause_screen(self) -> None:
        """
        Render the pause screen.
        """
        # Create a semi-transparent surface
        pause_surface = Surface(self.display.get_size())
        pause_surface.fill(self.colors.BLACK)
        pause_surface.set_alpha(128)  # Adjust alpha level to make it semi-transparent

        # Blit the semi-transparent surface onto the display
        self.display.blit(pause_surface, (0, 0))

        # Display "Game Paused" message
        self.display_message(
            message="Game Paused" if self.game_state is GameState.PAUSED else "Game Over",
            font_color=self.colors.WHITE,
            text_position=(self.display.get_width() // 2, self.display.get_height() // 2 - 100),
            font_size=72
        )

        btn_size = (150, 50)

        # Display "Quit" (Left) and "Return/Play Again" (Right) buttons
        self.quit_button = self.display_button(
            message="Quit Game",
            button_color=self.colors.LIGHT_RED,
            hover_color=self.colors.RED,
            button_position=(self.display.get_width() // 2 - 175, self.display.get_height() // 2),
            button_size=btn_size
        )

        self.return_button = self.display_button(
            message="Return" if self.game_state is GameState.PAUSED else "Play Again",
            button_position=(self.display.get_width() // 2 + 20, self.display.get_height() // 2),
            button_size=btn_size
        )

    def render(self) -> None:
        """
        Render the gameplay screen.
        """
        # Copy the speed over to game manager so entities can access it
        self.game_manager.game_speed = self.screen_manager.game_speed

        self.display.fill(self.colors.BROWN)
        self.draw_background_with_grid()
        self.draw_entities(self.game_manager.get_entities())

        self.display_message(message=f"Coins: {self.game_manager.get_coins():,}",
                             font_color=self.colors.WHITE,
                             text_position=(15, 20),
                             text_align="topleft"
                             )
        self.display_message(message=f"Wave: {self.wave_manager.get_wave()}",
                             font_color=self.colors.WHITE,
                             text_position=(15, 50),
                             text_align="topleft"
                             )

        # Draw plant/toolbar buttons
        self.render_plant_buttons()
        self.render_toolbar_buttons()

        # Render held item if there is one
        if self.held_item is not None:
            img = self.entity_imgs[self.held_item][0]
            self.render_held_item(img)

        # If no zombies are on the board, spawn new ones + update wave
        if not self.game_manager.get_entities(Zombie):
            self.wave_manager.begin_wave()

        # If the game is not paused/lost
        if self.game_state is GameState.PLAYING:
            self.render_entities()

        # If the game is paused/lost
        else:
            self.render_pause_screen()

        # If a zombie is not outside of screen, do not continue
        if not any(zombie.x <= -GRID_SIZE for zombie in self.zombies):
            return

        # If a Zombie goes out of the screen, the player loses
        wave = self.wave_manager.get_wave()
        self.database_manager.update_high_score(self.screen_manager.user_logged_in, wave)
        self.screen_manager.game_speed = 1
        self.game_state = GameState.LOST

    def handle_key_events(self, key_pressed: int, unicode_char: str) -> None:
        if key_pressed != pygame.K_ESCAPE:
            return  # Only handle "ESC" key

        if self.game_state is GameState.PAUSED:
            self.game_state = GameState.PLAYING
        elif self.game_state is GameState.PLAYING:
            self.game_state = GameState.PAUSED

        self.sound_manager.toggle_music()
        self.held_item = None
        self.reset_plant_buttons()
