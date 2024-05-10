"""
Leafy Legions: WaveManager

This module contains the WaveManager class
for managing how to spawn zombies in the game
"""
# Standard Imports
import math
import random

# Local Imports
from src.constants import GRID_WIDTH, GRID_SIZE
from src.entities import Projectile, Zombie, SpeedyZombie, HulkingZombie, PolymorphZombie
from src.managers import GameManager


class WaveManager:
    """
    The WaveManager class is responsible for
    managing the spawning of zombies in the game.
    """
    def __init__(self, game_manager: GameManager) -> None:
        """
        Initialize a new WaveManager instance.

        Args:
            game_manager (GameManager): The game manager instance.
        """
        self.game_manager = game_manager
        self.__wave = 0
        self.__num_zombies = 0

    def calculate_num_zombies(self) -> int:
        """
        Calculate the number of zombies to spawn in a wave.

        Returns:
            int: The number of zombies to spawn in the wave.
        """
        if self.__wave <= 3:
            return self.__wave
        return self.__wave + math.ceil(3 + math.log(self.__wave, 4))

    def calculate_special_zombies(self, zombie_type: type[Zombie], threshold: int) -> list[type[Zombie]]:
        """
        Calculate the number of special zombies to spawn in a wave.

        Args:
            zombie_type (type[Zombie]): The type of special zombie to spawn.
            threshold (int): The wave number threshold to start spawning special zombies.

        Returns:
            list[type[Zombie]]: The list of special zombies to spawn.
        """
        weight = min((self.__wave - threshold - 1) * 0.1, 0.9)
        return [zombie_type] * int(self.__num_zombies * weight)

    def get_wave(self) -> int:
        """
        Get the current wave count
        """
        return self.__wave

    def update_wave(self) -> None:
        """
        Increase the wave count
        """
        self.__wave += 1

    def calculate_zombie_roles(self) -> list[type[Zombie]]:
        """
        Calculate the roles of zombies to spawn in a wave.

        Returns:
            list[type[Zombie]]: The list of zombies to spawn.
        """
        zombie_roles = []
        zombie_thresholds = {
            # ZombieType: Wave to spawn
            SpeedyZombie: 5,
            HulkingZombie: 10,
            PolymorphZombie: 15
        }

        for zombie_type, threshold in zombie_thresholds.items():
            if self.__wave >= threshold:
                zombie_roles.extend(self.calculate_special_zombies(zombie_type, threshold - 1))

        remaining_zombies = self.__num_zombies - len(zombie_roles)
        zombie_roles.extend([Zombie] * remaining_zombies)
        return zombie_roles

    def begin_wave(self) -> None:
        """
        Begin the wave by spawning zombies.
        """
        self.update_wave()
        self.game_manager.clear_entities(Projectile)
        self.__num_zombies = self.calculate_num_zombies()
        zombie_roles = self.calculate_zombie_roles()
        self.spawn_zombies(zombie_roles)

    def spawn_zombies(self, zombie_roles) -> None:
        """
        Spawn zombies on the board.
        """
        for _ in range(len(zombie_roles)):
            zombie_type = random.choice(zombie_roles)
            zombie_spawn_x = ((GRID_WIDTH - 1) * GRID_SIZE) + 75 + random.choice(list(range(-50, 126, 20)))
            zombie_spawn_y = random.randint(0, 4) * GRID_SIZE
            new_zombie = zombie_type(self.game_manager, zombie_spawn_x, zombie_spawn_y)
            self.game_manager.add(new_zombie)
