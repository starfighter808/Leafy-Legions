"""
Leafy Legions: GameManager

This module contains the GameManager class
for managing everything happening after the
user presses on the "Start" button
"""
# Local Imports
from src.entities import Plant, Zombie, Projectile
from src.managers import SoundManager

Entity = Zombie | Plant | Projectile


class GameManager:
    """
    The GameManager class is responsible for managing entities on the game board,
    along with the application and game running statuses.
    """
    def __init__(self) -> None:
        """
        Initialize a GameManager object.
        """
        self.__entities: dict[type[Entity], list[Entity]] = {
            Zombie: [],  # List to store instances of the Zombie class
            Plant: [],  # List to store instances of the Plant class
            Projectile: [],  # List to store instances of the Projectile class
        }
        self.__game_running: bool = False
        self.sound_manager = SoundManager()
        self.__coins: int = 25  # Default: 25 coins
        self.__wave: int = 1    # Default: 1 wave

    def __validate_entity(self, entity: Entity) -> type[Entity]:
        """
        Validate if an entity is of a registered type in the GameManager and
        return its base class.

        Args:
            entity (Entity): The entity to be validated.

        Returns:
            type[Entity]: The base class of the entity.

        Raises:
            ValueError: If the entity type is not registered in the GameManager.
        """
        entity_type: type[Entity] = type(entity)
        for base_class in self.__entities:
            if issubclass(entity_type, base_class):
                return base_class
        raise ValueError(f"Entity type {entity_type} is not registered in GameManager")

    def add(self, entity: Entity) -> None:
        """
        Add an entity to the GameManager.

        Args:
            entity (Entity): The entity to be added.
        """
        base_class: type[Entity] = self.__validate_entity(entity)
        self.__entities[base_class].append(entity)

    def remove(self, entity: Entity) -> None:
        """
        Remove an entity from the GameManager.

        Args:
            entity (Entity): The entity to be removed.
        """
        for entities_list in self.__entities.values():
            if entity in entities_list:
                base_class: type[Entity] = self.__validate_entity(entity)
                self.__entities[base_class].remove(entity)

    def get_entities(self, entity_class: type[Entity] = None) -> list[Entity]:
        """
        Get entities on the board or entities of a specific class registered in the GameManager.
        This will not return derived classes, such as SpeedyZombie.

        Args:
            entity_class (type[Entity] | None): The class of entities to retrieve (e.g., Zombie or Plant).

        Returns:
            list: A list containing all entities or entities of the specified class.

        Raises:
            ValueError: If the specified entity_class is not registered in the GameManager.
        """
        if entity_class is None:
            return [entity for entities_list in self.__entities.values() for entity in entities_list]
        if entity_class in self.__entities:
            return self.__entities[entity_class]
        raise ValueError(f"Entity class {entity_class} is not registered in GameManager")

    def clear_entities(self, entity_class: type[Entity]) -> None:
        """
        Clears the entities of that specific class

        Args:
            entity_class (type[Entity]): The class of entities to clear (e.g., Zombie or Plant).
        """
        if entity_class in self.__entities:
            self.__entities[entity_class].clear()
        else:
            raise ValueError(f"Entity class {entity_class} is not registered in GameManager")

    def reset(self) -> None:
        """
        Reset the GameManager by clearing all entities.
        """
        for entity in self.__entities:
            self.clear_entities(entity)
        self.__coins = 25
        self.__wave = 1

    def set_game_status(self, game_running: bool) -> None:
        """
        Set the status of the game running and resets board state

        Args:
            game_running (bool): The status of the game.
        """
        self.__game_running = game_running
        if not self.__game_running:
            self.reset()

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
        self.sound_manager.play_sound('moneyfalls.ogg')

    def remove_coins(self, coins: int) -> None:
        """
        Remove users' coins
        """
        self.__coins -= coins

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