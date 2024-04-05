# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from . import Entity

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController
    from . import Zombie


class Projectile(Entity):
    """
    A Projectile is a moving entity that is shot
    from plants on the game board to hurt zombies.
    """

    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a Projectile object.

        Args:
            game_controller (GameController): An instance of the game controller managing the projectile.
            x (int): The initial x-coordinate of the projectile.
            y (int): The initial y-coordinate of the projectile.
        """
        super().__init__(game_controller, x, y, ["assets/images/projectile.png"])
        self.image_size: tuple[int, int] = (25, 25)
        self.speed: float = 5.0
        self.collided_with_zombie: bool = False  # Flag to indicate collision with a plant

    def attack_zombie(self, zombie: 'Zombie'):
        """
        Attack a zombie.

        Args:
            zombie (Zombie): The zombie object being attacked.
        """
        zombie.health -= 25
        print(f"Projectile hit Zombie {zombie.x, zombie.y}. Health: {zombie.health}")

        if zombie.health <= 0:
            print(f"Zombie {zombie.x, zombie.y} has died")
            self.game_controller.remove(zombie)
            self.game_controller.add_coins(10)

        self.game_controller.play_sound('hit.ogg', 0.05)
        self.game_controller.remove(self)

    def update_position(self) -> None:
        """
        Update the projectile's position.
        """
        if self.x < 1125:  # Check if the projectile is not out of bounds
            self.x += self.speed
        else:
            self.game_controller.remove(self)
