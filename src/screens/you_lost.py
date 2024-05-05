"""
Leafy Legions: YouLostScreen

This module contains the YouLostScreen class
for managing the "You Lost!" screen after losing the game
"""
# Standard Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from src.screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import ScreenManager


class YouLostScreen(BaseScreen):
    """
    The YouLostScreens renders the "You Lost!"
    screen after losing in the GameplayScreen
    """
    def __init__(self, screen_manager: 'ScreenManager', display: pygame.Surface) -> None:
        """
        Initialize the You Lost! screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (pygame.Surface): The pygame display
        """
        super().__init__(screen_manager, display, title="Leafy Legions: You Lost!")
        self.play_again_btn = None
        self.return_btn = None
        self.alpha = 10

    def render(self) -> None:
        """
        Render the "You Lost!" screen
        """
        self.display.fill(self.colors.BROWN)

        # Increase alpha value gradually until it reaches 255 (fully opaque)
        self.alpha = min(self.alpha + 60, 255)

        # Render the "You Lost!" message
        self.display_message(message="You Lost!",
                             font_color=self.colors.GREEN,
                             text_position=(self.display.get_width() // 2, 100),
                             font_size=64,
                             alpha=self.alpha
                             )

        # Button Size
        btn_width = 280
        btn_height = 70

        # Button position calculations
        btn_x = (self.display.get_width() - btn_width) // 2
        total_height = (btn_height * 2) + (100 * 2)  # Total height of all buttons and spacing
        play_again_btn_y = (self.display.get_height() - total_height) // 2
        return_btn_y = play_again_btn_y + btn_height + 100

        # Render "Play Again" button aligned to the center
        self.play_again_btn = self.display_button(message="Play Again!",
                                                  button_position=(btn_x, play_again_btn_y),
                                                  button_size=(btn_width, btn_height),
                                                  alpha=self.alpha
                                                  )

        # Render "Return to Main Menu" button aligned to the center
        self.return_btn = self.display_button(message="Return to Main Menu",
                                              button_position=(btn_x, return_btn_y),
                                              button_size=(btn_width, btn_height),
                                              alpha=self.alpha
                                              )

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the leaderboard screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        super().handle_click_events(mouse_pos)
        if self.play_again_btn and self.play_again_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("GameplayScreen")
        elif self.return_btn and self.return_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("MainMenuScreen")
