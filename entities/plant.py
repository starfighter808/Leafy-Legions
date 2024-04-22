# Standard Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from . import Entity, Projectile

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class Plant(Entity):
    """
    A Plant is a stationary entity that is placed
    on the game board to defend against zombies.
    """

    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a Plant object.

        Args:
            game_controller (GameController): An instance of the game controller managing the plant.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        super().__init__(game_controller, x, y, ["assets/images/plant.png"])
        self.health: int = 150  # Health of the plant
        self.cost: int = 15
        self.attack_speed: float = 1.0
        self.__last_attack: int = 0
        self.game_controller.play_sound('plant.ogg', 0.05)

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
            self.game_controller.play_sound('shoot.ogg', 0.05)

            new_projectile = Projectile(self.game_controller, self.x+75, self.y)
            self.game_controller.add(new_projectile)

