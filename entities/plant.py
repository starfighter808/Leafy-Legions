from typing import TYPE_CHECKING

# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class Plant:
    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a Plant object.

        Args:
            game_controller (GameController): An instance of the game controller managing the plant.
            x (int): The initial x-coordinate of the plant.
            y (int): The initial y-coordinate of the plant.
        """
        self.game_controller: 'GameController' = game_controller
        self.x: int = x
        self.y: int = y
        self.image: str = "assets/images/plant.png"
        self.health: int = 150  # Health of the plant
