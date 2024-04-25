"""
Leafy Legions: Entity

This module contains the Entity class
for managing every Entity in the Gameplay board
"""

# Standard Imports
from typing import TYPE_CHECKING

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import GameManager


class Entity:
    """
    An Entity is anything on the game board
    """

    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes any Entity object.

        Args:
            game_manager (GameManager): An instance of the GameManager managing the entity.
            x (int): The initial x-coordinate of the entity.
            y (int): The initial y-coordinate of the entity.
        """
        self.game_manager = game_manager
        self.x = x
        self.y = y

        self.attributes = {
            "images": []
        }
