"""
Leafy Legions: AppleProjectile (Projectile/Entity)

This module contains the AppleProjectile class,
a type of Projectile/Entity on the Gameplay board
"""
# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from src.entities import Projectile

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import GameManager


class AppleProjectile(Projectile):
    """
    A AppleProjectile is a type of Projectile that deals 50 damage and moves faster
    """

    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a AppleProjectile object, inheriting from the Projectile class

        Args:
            game_manager (GameManager): An instance of the GameManager managing the projectile.
            x (int): The initial x-coordinate of the projectile.
            y (int): The initial y-coordinate of the projectile.
        """
        super().__init__(game_manager, x, y)
        self.speed: float = 7.0
        self.damage: int = 50
        self.image_size: tuple[int, int] = (35, 44)

        self.attributes = {
            "images": ["apple_projectile.png"]
        }
