# Standard Imports
import os

# Library Imports
import pygame

# Local Imports
from entities import Plant, Zombie, Projectile

Entity = Zombie | Plant | Projectile


class GameController:
    """
    The GameController class is responsible for managing entities on the game board,
    along with the application and game running statuses.
    """

    def __init__(self) -> None:
        """
        Initialize a GameController object.
        """
        self.__entities: dict[type[Entity], list[Entity]] = {
            Zombie: [],  # List to store instances of the Zombie class
            Plant: [],  # List to store instances of the Plant class
            Projectile: [],  # List to store instances of the Projectile class
        }
        self.__app_running: bool = True
        self.__game_running: bool = False
        self.__coins: int = 25
        self.__wave: int = 1

    def __validate_entity(self, entity: Entity) -> type[Entity]:
        """s
        Validate if an entity is of a registered type in the GameController and
        return its base class.

        Args:
            entity (Entity): The entity to be validated.

        Returns:
            type[Entity]: The base class of the entity.

        Raises:
            ValueError: If the entity type is not registered in the GameController.
        """
        entity_type: type[Entity] = type(entity)
        for base_class in self.__entities:
            if issubclass(entity_type, base_class):
                return base_class
        raise ValueError(f"Entity type {entity_type} is not registered in GameController")

    def add(self, entity: Entity) -> None:
        """
        Add an entity to the GameController.

        Args:
            entity (Entity): The entity to be added.
        """
        base_class: type[Entity] = self.__validate_entity(entity)
        self.__entities[base_class].append(entity)

    def remove(self, entity: Entity) -> None:
        """
        Remove an entity from the GameController.

        Args:
            entity (Entity): The entity to be removed.
        """
        base_class: type[Entity] = self.__validate_entity(entity)
        self.__entities[base_class].remove(entity)

    def reset(self) -> None:
        """
        Reset the GameController by clearing all entities.
        """
        self.__entities = {
            Zombie: [],  # List to store instances of the Zombie class
            Plant: [],  # List to store instances of the Plant class
            Projectile: [],  # List to store instances of the Projectile class
        }
        self.__coins = 25
        self.__wave = 1

    def get_entities(self, entity_class: type[Entity] = None) -> list[Entity]:
        """
        Get entities on the board or entities of a specific class registered in the GameController.
        This will not return derived classes, such as SpeedyZombie.

        Args:
            entity_class (type[Entity] | None): The class of entities to retrieve (e.g., Zombie or Plant).

        Returns:
            list: A list containing all entities or entities of the specified class.

        Raises:
            ValueError: If the specified entity_class is not registered in the GameController.
        """
        if entity_class is None:
            return [entity for entities_list in self.__entities.values() for entity in entities_list]
        if entity_class in self.__entities:
            return self.__entities[entity_class]
        raise ValueError(f"Entity class {entity_class} is not registered in GameController")

    def set_game_status(self, game_running: bool) -> None:
        """
        Set the status of the game running and resets board state

        Args:
            game_running (bool): The status of the game.
        """
        self.__game_running = game_running
        if not game_running:
            self.reset()

    def set_app_status(self, app_running: bool) -> None:
        """
        Set the status of the app running.

        Args:
            app_running (bool): The status of the game.
        """
        self.__app_running = app_running

    def get_status(self, status_type: str) -> bool:
        """
        Get either the game status or the running status.

        Args:
            status_type (str): Either 'app' or 'game' to indicate which status to retrieve.

        Returns:
            bool: The requested status.

        Raises:
            ValueError: If an invalid status_type is provided.
        """
        if status_type == 'app':
            return self.__app_running
        if status_type == 'game':
            return self.__game_running
        raise ValueError("Invalid status_type. Use 'app' or 'game'.")

    def play_sound(self, effect_file: str, volume: float = 1.0) -> None:
        """
        Play sound effect

        Args:
            effect_file (str): Name of the sound effect file
            volume (float): Volume of the sound effect (default = 1.0)

        Raises:
            FileNotFoundError: If no sound is found
        """

        sound_path = f"./assets/sounds/{effect_file}"
        if self.__game_running:
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(volume)
                sound.play()
            else:
                raise FileNotFoundError(f"No sound effect at {sound_path}")

    def get_coins(self) -> int:
        """
        Get the coins of the current game session

        Returns:
            int: The current coins.
        """
        return self.__coins

    def add_coins(self, coins: int) -> None:
        """
        Add users' coins
        """
        self.__coins += coins
        self.play_sound('moneyfalls.ogg', 0.05)

    def remove_coins(self, coins: int) -> None:
        """
        Remove users' coins
        """
        self.__coins -= coins
        self.play_sound('moneyfalls.ogg', 0.05)

    def get_wave(self) -> int:
        """
        Return the current wave
        """
        return self.__wave

    def update_wave(self) -> None:
        """
        Increase the wave
        """
        self.__wave += 1
