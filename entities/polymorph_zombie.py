"""
Leafy Legions: PolymorphZombie (Zombie/Entity)

This module contains the PolymorphZombie class,
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


class PolymorphZombie(Zombie):
    """
    A Polymorph Zombie a type of Zombie with increased Health and Speed.
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a Polymorph Zombie object, inheriting from the Zombie class

        Args:
            game_manager (GameManager): An instance of the GameManager managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_manager, x, y)
        self.image_size = (125, 125)
        self.speed: float = 3
        self.health: int = 600

        self.attributes = {
            "name": "The Shapeshifter",
            "images": ["assets/images/polymorph_zombie.png"],
            "description": "A formidable zombie with increased health and speed, it adapts to its surroundings for survival."
        }
