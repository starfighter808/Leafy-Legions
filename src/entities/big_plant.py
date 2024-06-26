"""
Leafy Legions: BigPlant (Plant/Entity)

This module contains the BigPlant class,
a type of Plant/Entity on the Gameplay board
"""
# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from src.entities import Plant, AppleProjectile

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import GameManager


class BigPlant(Plant):
    """
    A BigPlant is a type of Plant with increased health and damage, but slower attack speed and higher cost
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a BigPlant object, inheriting from the Plant class

        Args:
            game_manager (GameManager): An instance of the GameManager managing the plant.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        super().__init__(game_manager, x, y)
        self.health: int = 400
        self.cost: int = 65
        self.attack_speed: float = 0.5
        self.projectile_type = AppleProjectile

        self.attributes = {
            "name": "Giant",
            "images": ["big_plant.png"],
            "description": "A slow, towering plant with high health and damage, it stands as a formidable barrier "
                           "against zombies."
        }
