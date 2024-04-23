"""
Leafy Legions: Zombie (Entity)

This module contains the Zombie class,
a type of Entity on the Gameplay board
"""

# System Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from entities import Entity

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import GameManager
    from entities import Plant


class Zombie(Entity):
    """
    A Zombie is a hostile entity that moves across the
    board and attacks plants on the game board.
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a Zombie object.

        Args:
            game_manager (GameManager): An instance of the GameManager managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_manager, x, y)
        self.image_size: tuple[int, int] = (56, 112)
        self.health: int = 100
        self.speed: float = 1.0
        self.attack_speed: float = 1.0
        self.collided_with_plant: bool = False  # Flag to indicate collision with a plant

        self.__last_attack: int = 0
        self.attributes = {
            "name": "The Stumbler",
            "images": ["assets/images/zombie_1.png", "assets/images/zombie_2.png"],
            "description": "Slow but relentless, it overwhelms defenses with sheer numbers."
        }

    def __can_attack(self) -> bool:
        """
        Check if the zombie can perform an attack based on attack speed.

        Returns:
            bool: True if the zombie can attack, False otherwise.
        """
        current_time: int = pygame.time.get_ticks()
        return current_time - self.__last_attack >= 1000 / self.attack_speed

    def attack_plant(self, plant: 'Plant') -> None:
        """
        Attack a plant.

        Args:
            plant (Plant): The plant object being attacked.
        """
        self.collided_with_plant = True
        if self.__can_attack():
            self.__last_attack = pygame.time.get_ticks()

            plant.health -= 25
            print(f"Zombie attacking Plant ({plant.x}, {plant.y}). Health: {plant.health}")

            if plant.health <= 0:
                print(f"Plant {plant.x, plant.y} has died")
                self.game_manager.remove(plant)
                self.collided_with_plant = False

    def update_position(self) -> None:
        """
        Update the zombie's position.
        """
        # Update the zombie's position
        if not self.collided_with_plant and self.x > -125:  # Check if not collided with a plant or out of bounds
            self.x -= self.speed
