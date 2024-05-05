"""
Leafy Legions: ScreenManager

This module contains the ScreenManager class
for managing every screen view in the application
"""
# Standard Imports
import inspect

# Library Imports
import pygame

# Local Imports
from managers import DatabaseManager
import screens


def _get_valid_screens() -> list[str]:
    """
    Fetch valid screen classes from the screens module.

    Returns:
        list: A list of valid screen classes.
    """
    screens_module = inspect.getmembers(screens, inspect.isclass)
    return [screen_class_name for screen_class_name, _ in screens_module]


class ScreenManager:
    """
    A class to manage different screens in the game.

    Attributes:
        display (pygame.Surface): The current pygame display being used to render
        current_screen (type[BaseScreen]): The current screen class being displayed.
        valid_screens (list[str]): A list of valid screen classes.
        user_logged_in (str): If the user has validated their login
    """
    def __init__(self, display: pygame.Surface) -> None:
        """
        Initialize the ScreenManager with an empty current_screen and fetch valid screen classes.

        Args:
            display (pygame.Surface): The current pygame display being used to render
        """
        self.__running = True
        self.database_manager = DatabaseManager()
        self.display = display
        self.current_screen = None
        self.valid_screens: list[str] = _get_valid_screens()
        self.user_logged_in = None
        self.game_speed = 1

    def is_running(self):
        """
        Whether the application is running or not
        """
        return self.__running

    def quit(self):
        """
        Close the application
        """
        self.__running = False

    def set_screen(self, screen_name: str) -> None:
        """
        Set the current screen based on the provided screen name.

        Args:
            screen_name (str): The name of the screen to set

        Raises:
            ValueError: If an invalid screen name is provided.
        """
        if screen_name in self.valid_screens:
            screen_class = getattr(screens, screen_name)
            self.current_screen = screen_class(display=self.display, screen_manager=self)
        else:
            raise ValueError("Invalid screen name")

    def run_current_screen(self) -> None:
        """
        Run the game loop of the current screen.

        Raises:
            ValueError: If no screen is set.
        """
        if self.current_screen:
            self.current_screen.render()
        else:
            raise ValueError("No screen set")
