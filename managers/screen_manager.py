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
        current_screen: The current screen being displayed.
        valid_screens: A list of valid screen classes.
    """

    def __init__(self, display: pygame.Surface) -> None:
        """
        Initialize the ScreenManager with an empty current_screen and fetch valid screen classes.
        """
        self.__running = True
        self.display = display
        self.current_screen = None
        self.valid_screens: list[str] = _get_valid_screens()
        self.user_logged_in = False

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
