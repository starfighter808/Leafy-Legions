import pygame
from typing import TYPE_CHECKING
from . import Plant


# To import GameController without circular dependency errors
if TYPE_CHECKING:
    from managers import GameController


class Zombie:
    def __init__(self, game_controller: 'GameController', x: int, y: int) -> None:
        """
        Initializes a Zombie object.

        Args:
            game_controller (GameController): An instance of the game controller managing the zombie.
            x (int): The initial x-coordinate of the zombie.
            y (int): The initial y-coordinate of the zombie.
        """
        self.game_controller: 'GameController' = game_controller
        self.x: int = x
        self.y: int = y
        self.health: int = 100
        self.speed: float = 1.0
        self.image: str = "assets/images/creeper.png"
        self.collided_with_plant: bool = False  # Flag to indicate collision with a plant

        self.attack_speed: float = 1.0
        self.last_attack: int = 0

    def _can_attack(self) -> bool:
        """
        Check if the zombie can perform an attack based on attack speed.

        Returns:
            bool: True if the zombie can attack, False otherwise.
        """
        current_time: int = pygame.time.get_ticks()
        return current_time - self.last_attack >= 1000 / self.attack_speed

    def attack_plant(self, plant: Plant) -> None:
        """
        Attack a plant.

        Args:
            plant (Plant): The plant object being attacked.
        """
        self.collided_with_plant = True
        if self._can_attack():
            self.last_attack = pygame.time.get_ticks()

            plant.health -= 25
            print(f"Zombie attacking Plant ({plant.x}, {plant.y}). Health: {plant.health}")

            if plant.health <= 0:
                print(f"Plant {plant.x, plant.y} has died")
                self.game_controller.remove(plant)
                self.collided_with_plant = False

    def update_position(self) -> None:
        """
        Update the zombie's position.
        """
        # Update the zombie's position
        if not self.collided_with_plant and self.x > -125:  # Check if not collided with a plant or out of bounds
            self.x -= self.speed
