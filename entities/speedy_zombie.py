from entities.zombie import Zombie
from managers import GameController


class SpeedyZombie(Zombie):
    def __init__(self, game_controller: GameController, x: int, y: int) -> None:
        """
        Initializes a SpeedyZombie object, inheriting from the Zombie class

        Args:
            game_controller (GameController): An instance of the game controller managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        super().__init__(game_controller, x, y)
        self.speed: float = 3.0
        self.image: str = "assets/images/speedyZombie.png"
