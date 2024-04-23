"""
Leafy Legions: Plant (Entity)

This module contains the Plant class,
a type of Entity on the Gameplay board
"""

# Standard Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from entities import Entity, Projectile

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import GameManager


class Plant(Entity):
    """
    A Plant is a stationary entity that is placed
    on the game board to defend against zombies.
    """

    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a Plant object.

        Args:
            game_manager (GameManager): An instance of the GameManager managing the plant.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        super().__init__(game_manager, x, y)
        self.health: int = 150  # Health of the plant

        self.attack_speed: float = 1.0
        self.__last_attack: int = 0
        if game_manager:
            self.game_manager.play_sound('plant.ogg')

        self.attributes = {
            "name": "The Cowboy",
            "images": ["assets/images/plant.png"],
            "description": "A sharpshooting sentinel with a ten-gallon hat and a lasso, it wrangles foes while "
                           "providing cover. Agile and precise, it turns the tide with its quick reflexes and summons"
                           "allies to stampede to victory!"
        }

    def __can_attack(self) -> bool:
        """
        Check if the plant can perform an attack based on attack speed.

        Returns:
            bool: True if the plant can attack, False otherwise.
        """
        current_time: int = pygame.time.get_ticks()
        return current_time - self.__last_attack >= 1000 / self.attack_speed

    def shoot_projectile(self) -> None:
        """
        Shoot a projectile to attack a zombie.
        """
        if self.__can_attack():
            self.__last_attack = pygame.time.get_ticks()
            self.game_manager.play_sound('shoot.ogg')

            new_projectile = Projectile(self.game_manager, self.x + 75, self.y)
            self.game_manager.add(new_projectile)
