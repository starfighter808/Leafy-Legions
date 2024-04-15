# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from . import Zombie

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class SpeedyZombie(Zombie):
    """
    A SpeedyZombie a type of Zombie with increased speed.
    """

    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a SpeedyZombie object, inheriting from the Zombie class

        Args:
            game_controller (GameController): An instance of the game controller managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_controller, x, y)
        self.image = ["assets/images/speedyZombie.png"]
        self.image_size = (125, 125)
        self.speed: float = 4.0

