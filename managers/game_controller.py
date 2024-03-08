from entities import Plant, Zombie


class GameController:
    def __init__(self) -> None:
        """
        Initialize a GameController object.
        """
        self.entities: dict[type[Zombie | Plant], list[Zombie | Plant]] = {
            Zombie: [],  # List to store instances of the Zombie class
            Plant: [],  # List to store instances of the Plant class
        }
        self.app_running: bool = True
        self.game_running: bool = True

    def _validate_entity(self, entity: Zombie | Plant) -> type[Zombie | Plant]:
        """
        Validate if an entity is of a registered type in the GameController and
        return its base class.

        Args:
            entity (type): The entity to be validated.

        Returns:
            type: The base class of the entity.

        Raises:
            ValueError: If the entity type is not registered in the GameController.
        """
        entity_type: type[Zombie | Plant] = type(entity)
        for base_class in self.entities:
            if issubclass(entity_type, base_class):
                return base_class
        raise ValueError(f"Entity type {entity_type} is not registered in GameController")

    def add(self, entity: Zombie | Plant) -> None:
        """
        Add an entity to the GameController.

        Args:
            entity: The entity to be added.
        """
        base_class: type[Zombie | Plant] = self._validate_entity(entity)
        self.entities[base_class].append(entity)

    def remove(self, entity: Zombie | Plant) -> None:
        """
        Remove an entity from the GameController.

        Args:
            entity: The entity to be removed.
        """
        base_class: type[Zombie | Plant] = self._validate_entity(entity)
        self.entities[base_class].remove(entity)

    def reset(self) -> None:
        """
        Reset the GameController by clearing all entities.
        """
        self.entities = {
            Zombie: [],  # List to store instances of the Zombie class
            Plant: [],  # List to store instances of the Plant class
        }

    def get_entities(self, entity_class: type[Zombie | Plant] = None) -> list[Zombie | Plant]:
        """
        Get entities on the board or entities of a specific class registered in the GameController.
        This will not return derived classes, such as SpeedyZombie.

        Args:
            entity_class (optional): The class of entities to retrieve (e.g., Zombie or Plant).

        Returns:
            list: A list containing all entities or entities of the specified class.

        Raises:
            ValueError: If the specified entity_class is not registered in the GameController.
        """
        if entity_class is None:
            return [entity for entities_list in self.entities.values() for entity in entities_list]
        elif entity_class in self.entities:
            return self.entities[entity_class]
        else:
            raise ValueError(f"Entity class {entity_class} is not registered in GameController")

    def set_game_status(self, game_running: bool) -> None:
        """
        Set the status of the game running and resets board state

        Args:
            game_running (bool): The status of the game.
        """
        self.game_running = game_running
        if not game_running:
            self.reset()

    def set_app_status(self, app_running: bool) -> None:
        """
        Set the status of the app running.

        Args:
            app_running (bool): The status of the game.
        """
        self.app_running = app_running

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
            return self.app_running
        elif status_type == 'game':
            return self.game_running
        else:
            raise ValueError("Invalid status_type. Use 'app' or 'game'.")
