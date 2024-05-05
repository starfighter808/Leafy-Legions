"""
Leafy Legions: GameplayScreen

This module contains the GameplayScreen class
for managing the game itself when running
"""
# Standard Imports
import inspect
import math
import random
import os
import sys
from types import ModuleType
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from src import entities
from src.entities import Plant, Projectile, SpeedyZombie, Zombie, PolymorphZombie, HulkingZombie
from src.entities import __all__ as all_entities
from src.managers import ColorManager, GameManager
from src.screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import ScreenManager

# CONSTANTS
GRID_WIDTH: int = 9
GRID_HEIGHT: int = 5
GRID_SIZE: int = 125
GRID_OFFSET: int = 100
PLANT_COST: int = 15


def scale_background(img: str) -> pygame.Surface:
    """
    Scales the image provided to fit the application

    Args:
        img (str): The name of the image file in "/src/assets/images/"

    Returns:
         pygame.Surface: The scaled image as a pygame Surface
    """
    if getattr(sys, 'frozen', False):
        base_path = os.path.join(sys._MEIPASS, f"src/assets/images/{img}")
    else:
        base_path = f"src/assets/images/{img}"
    scaled_img: pygame.Surface = pygame.image.load(base_path)
    scaled_img = pygame.transform.scale(scaled_img, (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    return scaled_img


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
        entity_instance = entity_class(None, 0, 0)

        image_paths: list = entity_instance.attributes["images"]
        if image_paths:
            images = []
            for image_path in image_paths:
                if getattr(sys, 'frozen', False):
                    base_path = os.path.join(sys._MEIPASS, f"src/assets/images/{image_path}")
                else:
                    base_path = f"src/assets/images/{image_path}"
                try:
                    image_size = entity_instance.image_size
                    images.append(pygame.transform.scale(pygame.image.load(base_path), image_size))
                except AttributeError:
                    images.append(pygame.transform.scale(pygame.image.load(base_path), (GRID_SIZE, GRID_SIZE)))
            scaled_images[entity_class] = images

    return scaled_images


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
        self.entity_imgs = load_and_scale_entity_images(sys.modules['src.entities'])

        # Create plant topbar
        self.plant_buttons = []
        self.button_size = (130, 75)

        # Create a list of all Plant classes
        plant_classes = [cls for name, cls in inspect.getmembers(entities, inspect.isclass) if issubclass(cls, Plant)]

        # Create instances of each plant class to access their cost, then sort by cost
        self.plant_instances = [(plant_class(None, 0, 0), plant_class) for plant_class in plant_classes]
        self.plant_instances = sorted(self.plant_instances, key=lambda instance: instance[0].cost)

        # Create buttons for each plant
        for i, (plant_instance, _) in enumerate(self.plant_instances):
            button_position = (30 + self.button_size[0] + i * 160, 15)
            self.plant_buttons.append({
                "name": plant_instance.attributes["name"],  # The name of the plant
                "cost": plant_instance.cost,  # The cost of the plant
                "color": self.colors.GREEN,
                "hover_color": self.colors.LIGHT_BLUE,
                "position": button_position,  # Set button position
            })
            print(f"Plant {plant_instance.attributes['name']} button created at {button_position}")

        # Create toolbar buttons
        self.pause_button = None
        self.game_paused = False
        self.fast_forward_button = None
        self.shovel_button = None
        self.held_item: any = None

        # Create pause screen buttons
        self.return_button = None
        self.quit_button = None

        # When all assets are loaded, start the game
        self.game_manager.set_game_status(True)
        self.sound_manager.play_music('gameplay.mp3')

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

        # For Wave 10+, start adding Hulking Zombies
        if wave >= 10:
            weight_hulking = min((wave - 9) * 0.1, 1.0)  # Weight HulkingZombies into the mix
            zombie_roles.extend([HulkingZombie] * int(num_zombies * weight_hulking))

        # For Wave 15+, start adding Polymorph Zombies
        if wave >= 15:
            weight_poly = min((wave - 14) * 0.1, 1.0)  # Weight PolymorphZombies into the mix
            zombie_roles.extend([PolymorphZombie] * int(num_zombies * weight_poly))

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

    def draw_grid_and_entities(self, objs: list[Zombie | Plant | Projectile]) -> None:
        """
        Draw the grid lines, background, and entities on the game screen.

        Args:
            objs (List): A list of entities to be drawn.
        """
        # Draw background
        self.display.blit(self.background_img, (0, GRID_OFFSET))

        # Draw grid
        for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(self.display, self.colors.BLACK, (x, GRID_OFFSET),
                             (x, GRID_HEIGHT * GRID_SIZE + GRID_OFFSET))
        for y in range(GRID_OFFSET, GRID_HEIGHT * GRID_SIZE + GRID_OFFSET, GRID_SIZE):
            pygame.draw.line(self.display, self.colors.BLACK, (0, y), (GRID_WIDTH * GRID_SIZE, y))

        # Sort entities by type: Plant, then Zombie, so that zombies always appear "on top"
        objs.sort(key=lambda objName: isinstance(objName, Zombie))
        current_time = pygame.time.get_ticks()
        for obj in objs:
            images = self.entity_imgs.get(type(obj))
            if images:
                try:
                    cell_center_x = obj.x + (GRID_SIZE - obj.image_size[0]) / 2
                    cell_center_y = obj.y + GRID_OFFSET + (GRID_SIZE - obj.image_size[1]) / 2

                    # Assign a random animation offset to each entity
                    if not hasattr(obj, 'animation_offset'):
                        obj.animation_offset = random.randint(0, 10000)

                    # Calculate index of the image to display based on time
                    image_index = ((current_time + obj.animation_offset) // (
                            500 // self.screen_manager.game_speed)) % len(images)
                    self.display.blit(images[image_index], (cell_center_x, cell_center_y))
                except (AttributeError, IndexError):
                    self.display.blit(images[0], (obj.x, obj.y + GRID_OFFSET))

    def reset_plant_buttons(self) -> None:
        """
        Resets the color of all plant buttons to None.
        """
        for button_info in self.plant_buttons:
            button_info["color"] = self.colors.GREEN
            button_info["hover_color"] = self.colors.LIGHT_BLUE

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the gameplay screen.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.
        """
        super().handle_click_events(mouse_pos)
        mouse_x: int = mouse_pos[0]
        mouse_y: int = mouse_pos[1]
        grid_x: int = mouse_x // GRID_SIZE
        grid_y: int = (mouse_y - GRID_OFFSET) // GRID_SIZE

        click_in_grid: bool = (0 <= grid_x < GRID_WIDTH) and (0 <= grid_y < GRID_HEIGHT)

        # If the game is paused, handle return/quit buttons
        if self.game_paused:
            if self.return_button and self.return_button.collidepoint(mouse_pos):
                self.quit_button = None
                self.return_button = None
                self.game_paused = False
                self.sound_manager.toggle_music()
            elif self.quit_button and self.quit_button.collidepoint(mouse_pos):
                self.screen_manager.game_speed = 1
                self.screen_manager.set_screen("MainMenuScreen")

        # Handle plant button clicks
        for button_info, (_, plant_class) in zip(self.plant_buttons, self.plant_instances):
            button_rect = pygame.Rect(button_info["position"], self.button_size)

            if not self.game_paused:
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
                if self.pause_button and self.pause_button.collidepoint(mouse_pos):
                    self.game_paused = True
                    self.held_item = None
                    self.reset_plant_buttons()
                    self.sound_manager.toggle_music()
                elif self.fast_forward_button and self.fast_forward_button.collidepoint(mouse_pos):
                    self.screen_manager.game_speed = 2 if self.screen_manager.game_speed == 1 else 1
                    self.held_item = None
                    self.reset_plant_buttons()
                elif self.shovel_button and self.shovel_button.collidepoint(mouse_pos):
                    if self.held_item == 'shovel':
                        self.held_item = None
                    else:
                        self.held_item = 'shovel'
                    self.reset_plant_buttons()

        cell_x = grid_x * GRID_SIZE
        cell_y = grid_y * GRID_SIZE
        existing_plant: bool = any(plant.x == cell_x and plant.y == cell_y for plant in self.plants)

        # If we click in the grid and there is a held item
        if click_in_grid and self.held_item is not None:
            # If we do not have the shovel
            if self.held_item != 'shovel':
                if not existing_plant:
                    new_plant = self.held_item(self.game_manager, cell_x, cell_y)
                    if self.game_manager.get_coins() >= new_plant.cost:
                        # If we have enough coins and can plant, remove the coins, plant it, and reset held_item
                        self.game_manager.add(new_plant)
                        self.game_manager.remove_coins(new_plant.cost)
                        print(f"New {self.held_item.__name__} {new_plant.x, new_plant.y}. Health: {new_plant.health}")
                        self.held_item = None
                    else:
                        # If we don't have enough coins, reset held_item and throw error
                        self.held_item = None
                        self.sound_manager.play_sound('error.mp3', 0.15)
                else:
                    # If there is already a plant in the cell, throw error
                    self.held_item = None
                    self.reset_plant_buttons()
                    self.sound_manager.play_sound('error.mp3', 0.15)
            else:
                # If we click in the grid with a shovel
                for plant in self.plants:
                    # And we click on a plant
                    if plant.x == cell_x and plant.y == cell_y:
                        # Remove the plant, give user half the coins back, & reset held item
                        self.game_manager.remove(plant)
                        self.game_manager.add_coins(plant.cost // 2)
                        self.held_item = None
                        break  # Stop looping through plants after it was removed

    def render_held_item(self, item_image: pygame.Surface) -> None:
        """
        Renders the held item at the mouse cursor.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.display.blit(item_image,
                          (mouse_pos[0] - item_image.get_width() // 2, mouse_pos[1] - item_image.get_height() // 2))

    def render(self) -> None:
        """
        Render the gameplay screen.
        """
        # Copy the speed over to game manager so entities can access it
        self.game_manager.game_speed = self.screen_manager.game_speed

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
        # Draw plant buttons
        for button in self.plant_buttons:

            # Disable buttons if user does not have enough coins
            if self.game_manager.get_coins() < button["cost"]:
                button_color = self.colors.GRAY
                hover_color = self.colors.GRAY
            else:
                button_color = button["color"]
                hover_color = button["hover_color"]

            # Remove hover effects when game is paused
            if self.game_paused:
                hover_color = button_color

            self.display_button(
                message=button["name"],
                button_position=button["position"],
                button_color=button_color,
                hover_color=hover_color,
                button_size=self.button_size,
                offset_text=(0, -8),  # Move text up slightly to fit cost under it
                font_size=36
            )
            # Add cost within the button position, slightly lower than the current text
            cost_position = (button["position"][0] + (self.button_size[0] // 2), button["position"][1] + 52)
            self.display_message(
                message=f"Cost: {button['cost']}",
                font_color=self.colors.WHITE,
                text_position=cost_position,
                text_align="center",
                font_size=24
            )
        btn_x = self.display.get_width() - 200
        btn_y = 25
        btn_padding = 70
        btn_size = (50, 50)

        pause_color = self.colors.LIGHT_RED if self.game_paused is True else self.colors.GREEN
        pause_hover_color = self.colors.RED if self.game_paused is True else self.colors.LIGHT_BLUE

        fast_forward_color = self.colors.LIGHT_RED if self.screen_manager.game_speed == 2 else self.colors.GREEN
        fast_forward_hover_color = self.colors.RED if self.screen_manager.game_speed == 2 else self.colors.LIGHT_BLUE

        shovel_color = self.colors.LIGHT_RED if self.held_item == 'shovel' else self.colors.GREEN
        shovel_hover_color = self.colors.RED if self.held_item == 'shovel' else self.colors.LIGHT_BLUE

        # Remove hover effects when game is paused
        if self.game_paused:
            pause_hover_color = pause_color
            fast_forward_hover_color = fast_forward_color
            shovel_hover_color = shovel_color

        self.pause_button = self.display_button_image(
            image_filename='pause_icon.png',
            image_size=btn_size,
            image_position=(btn_x, btn_y),
            background_color=pause_color,
            hover_color=pause_hover_color
        )
        self.fast_forward_button = self.display_button_image(
            image_filename='fast_forward_icon.png',
            image_size=btn_size,
            image_position=(btn_x + btn_padding, btn_y),
            background_color=fast_forward_color,
            hover_color=fast_forward_hover_color
        )
        self.shovel_button = self.display_button_image(
            image_filename='shovel_icon.png',
            image_size=btn_size,
            image_position=(btn_x + (btn_padding * 2), btn_y),
            background_color=shovel_color,
            hover_color=shovel_hover_color
        )

        if self.held_item is not None:
            if self.held_item == 'shovel':
                if getattr(sys, 'frozen', False):
                    base_path = os.path.join(sys._MEIPASS, "src/assets/images/shovel_icon.png")
                else:
                    base_path = "src/assets/images/shovel_icon.png"
                shovel_image = pygame.image.load(base_path)
                shovel_image = pygame.transform.scale(shovel_image, (50, 50))
                self.render_held_item(shovel_image)
            elif issubclass(self.held_item, Plant):
                plant_image = self.entity_imgs[self.held_item][0]
                self.render_held_item(plant_image)

        # If no zombies are on the board, spawn new ones + update wave
        if not self.game_manager.get_entities(Zombie):
            self.begin_wave()
            self.game_manager.update_wave()

        # If the game is not paused
        if not self.game_paused:
            # Auto sets the Collision false to fix the collision issue when
            # Attacking plants
            for zombie in self.zombies:
                zombie.collided_with_plant = False

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

        # If the game is paused
        else:
            # Create a semi-transparent surface
            pause_surface = pygame.Surface(self.display.get_size())
            pause_surface.fill(self.colors.BLACK)
            pause_surface.set_alpha(128)  # Adjust alpha level to make it semi-transparent

            # Blit the semi-transparent surface onto the display
            self.display.blit(pause_surface, (0, 0))

            # Display "Game Paused" message
            self.display_message(
                message="Game Paused",
                font_color=self.colors.WHITE,
                text_position=(self.display.get_width() // 2, self.display.get_height() // 2 - 100),
                font_size=72
            )

            # Display "Quit" (Left) and "Return" (Right) buttons
            self.quit_button = self.display_button(
                message="Quit",
                button_color=self.colors.LIGHT_RED,
                hover_color=self.colors.RED,
                button_position=(self.display.get_width() // 2 - 175, self.display.get_height() // 2),
                button_size=(150, 50)
            )

            self.return_button = self.display_button(
                message="Return",
                button_position=(self.display.get_width() // 2 + 20, self.display.get_height() // 2),
                button_size=(150, 50)
            )

        # Check if any zombie go outside the screen
        if any(zombie.x <= -GRID_SIZE for zombie in self.zombies):
            wave = self.game_manager.get_wave() - 1
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
            self.database_manager.update_high_score(self.screen_manager.user_logged_in, wave)
            self.screen_manager.game_speed = 1
            self.screen_manager.set_screen("YouLostScreen")
