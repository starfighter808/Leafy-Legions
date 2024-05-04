"""
Leafy Legions: BigPlant (Plant/Entity)

This module contains the BigPlant class,
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


class BigPlant(Plant):
    """
    A BigPlant is a type of Plant with increased health and cost.
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a BigPlant object, inheriting from the Plant class

        Args:
            game_manager (GameManager): An instance of the GameManager managing the plant.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_manager, x, y)
        self.health: int = 400
        self.cost: int = 30

        self.attributes = {
            "name": "The Green Giant",
            "images": ["assets/images/big_plant.png"],
            "description": "A towering plant with increased health, it stands as a formidable barrier against zombies."
        }
