"""
Leafy Legions: SpeedyZombie (Zombie/Entity)

This module contains the SpeedyZombie class,
a type of Zombie/Entity on the Gameplay board
"""
# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from entities import Zombie

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import GameManager


class SpeedyZombie(Zombie):
    """
    A SpeedyZombie a type of Zombie with increased speed.
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a SpeedyZombie object, inheriting from the Zombie class

        Args:
            game_manager (GameManager): An instance of the GameManager managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_manager, x, y)
        self.image_size = (125, 125)
        self.speed: float = 3.0

        self.attributes = {
            "name": "The Sprinter",
            "images": ["assets/images/speedyZombie.png"],
            "description": "A blur of decayed flesh, dashing with alarming speed to catch its prey."
        }
