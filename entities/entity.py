# Standard Imports
from typing import TYPE_CHECKING

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class Entity:
    """
    An Entity is anything on the game board
    """

    def __init__(self, game_controller: 'GameController', x: int, y: int, image: list = None) -> None:
        """
        Initializes any Entity object.

        Args:
            game_controller (GameController): An instance of the game controller managing the entity.
            x (int): The initial x-coordinate of the entity.
            y (int): The initial y-coordinate of the entity.
            image (str): The image of this entity
        """
        self.game_controller = game_controller
        self.x = x
        self.y = y
        self.image = image
