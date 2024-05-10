"""
Leafy Legions: Shovel (Entity)

This module contains the Shovel class,
a type of Entity on the Gameplay board

This is only rendered when the player presses the
shovel button icon. It is used to remove plants
"""
# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from src.entities import Entity

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import GameManager


class Shovel(Entity):
    """
    The Shovel is used to remove plants from the game board.
    """

    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a Shovel object.

        Args:
            game_manager (GameManager): An instance of the GameManager.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        super().__init__(game_manager, x, y)
        self.image_size = (100, 100)

        self.attributes = {
            "images": ["shovel.png"],
        }
