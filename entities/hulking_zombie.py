"""
Leafy Legions: HulkingZombie (Zombie/Entity)

This module contains the HulkingZombie class,
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


class HulkingZombie(Zombie):
    """
    A Hulking Zombie a type of Zombie with increased Health but Lower Speed.
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a Hulking Zombie object, inheriting from the Zombie class

        Args:
            game_manager (GameManager): An instance of the GameManager managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_manager, x, y)
        self.image_size = (125, 125)
        self.speed: float = 1.75
        self.health: int = 500
        self.damage: int = 150

        self.attributes = {
            "name": "Behemoth",
            "images": ["assets/images/hulk_zombie.png"],
            "description": "A towering zombie with immense strength and resilience, it crushes plants in its path."
        }
