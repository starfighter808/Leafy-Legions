# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from . import Plant

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController

class BigPlant(Plant):
    """
    A BigPlant a type of Plant with increased health, and cost.
    """
    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a BigPlant object, inheriting from the Plant class

        Args:
            game_controller (GameController): An instance of the game controller managing the plant.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_controller, x, y)
        self.image = ["assets/images/bigPlant.png"]
        self.health: int = 400
        self.cost: int = 30