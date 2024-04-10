# Standard Imports
from typing import TYPE_CHECKING

# Local Imports
from . import Plant

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class RosePlant(Plant):
    """
    A Rose Plant a type of Plant with with decreased health but Faster attack speed.
    """

    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a Rose Plant object.

        Args:
            game_controller (GameController): An instance of the game controller managing the plant.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        super().__init__(game_controller, x, y, ["assets/images/Rose_plant.png"])
        self.health: int = 100  # Health of the plantss
        self.attack_speed: float = 2.0
        self.game_controller.play_sound('plant.ogg', 0.05)