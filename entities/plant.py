# Standard Imports
from typing import TYPE_CHECKING

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class Plant:
    """
    A Plant is a stationary entity that is placed
    on the game board to defend against zombies.
    """
    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a Plant object.

        Args:
            game_controller (GameController): An instance of the game controller managing the plant.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        self.game_controller = game_controller
        self.x = x
        self.y = y
        self.image: str = "assets/images/plant.png"
        self.health: int = 150  # Health of the plant
