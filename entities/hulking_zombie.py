# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from . import Zombie

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class HulkingZombie(Zombie):
    """
    A Hulking Zombie a type of Zombie with increased Health but Lower Speed.
    """

    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a Hulking Zombie object, inheriting from the Zombie class

        Args:
            game_controller (GameController): An instance of the game controller managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_controller, x, y)
        self.image = ["assets/images/Hulk_Zombie.png"]
        self.image_size = (125, 125)
        self.speed: float = 1.75
        self.health: int = 500