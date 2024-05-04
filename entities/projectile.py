"""
Leafy Legions: Projectile (Entity)

This module contains the Projectile class,
a type of Entity on the Gameplay board
"""
# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from entities import Entity, Zombie

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import GameManager


class Projectile(Entity):
    """
    A Projectile is a moving entity that is shot
    from plants on the game board to hurt zombies.
    """
    def __init__(self, game_manager: 'GameManager', x: int, y: int) -> None:
        """
        Initializes a Projectile object.

        Args:
            game_manager (GameManager): An instance of the GameManager managing the projectile.
            x (int): The initial x-coordinate of the projectile.
            y (int): The initial y-coordinate of the projectile.
        """
        super().__init__(game_manager, x, y)
        self.image_size: tuple[int, int] = (25, 25)
        self.speed: float = 5.0
        self.collided_with_zombie: bool = False  # Flag to indicate collision with a plant

        self.attributes = {
            "images": ["assets/images/projectile.png"]
        }

    def attack_zombie(self, zombie: Zombie):
        """
        Attack a zombie.

        Args:
            zombie (Zombie): The zombie object being attacked.
        """
        zombie.health -= 25
        print(f"Projectile hit Zombie {zombie.x, zombie.y}. Health: {zombie.health}")

        if zombie.health <= 0:
            print(f"Zombie {zombie.x, zombie.y} has died")
            self.game_manager.remove(zombie)
            self.game_manager.add_coins(10)

        self.sound_manager.play_sound('hit.ogg')
        self.game_manager.remove(self)

    def update_position(self) -> None:
        """
        Update the projectile's position.
        """
        if self.x < 1125:  # Check if the projectile is not out of bounds
            self.x += self.speed
        else:
            self.game_manager.remove(self)
