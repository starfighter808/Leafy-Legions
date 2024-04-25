"""
Leafy Legions: RosePlant (Plant/Entity)

This module contains the RosePlant class,
a type of Plant/Entity on the Gameplay board
"""
# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from entities import Plant

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import GameManager


class RosePlant(Plant):
    """
    A Rose Plant is a type of Plant with decreased health but faster attack speed.
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a Rose Plant object.

        Args:
            game_manager (GameManager): An instance of the GameManager managing the plant.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        super().__init__(game_manager, x, y)
        self.health: int = 75  # Health of the plants
        self.attack_speed: float = 2.0

        self.attributes = {
            "name": "Rose Plant",
            "images": ["assets/images/rose_plant.png"],
            "description": "???"
        }
