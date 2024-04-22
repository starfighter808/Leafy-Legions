"""
Leafy Legions: LeaderboardScreen

This module contains the LeaderboardScreen class
for managing the leaderboard screen in the game
"""

# Standard Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import ScreenManager


class LeaderboardScreen(BaseScreen):
    """
    The LeaderboardScreen renders the "Leaderboard"
    section of the application
    """

    def __init__(self, screen_manager: 'ScreenManager', display: pygame.Surface) -> None:
        """
        Initialize the Leaderboard screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (pygame.Surface): The pygame display
        """
        super().__init__(screen_manager, display, title="Leafy Legions: Leaderboard")
        self.leaderboard_data = None
        self.previous_btn = None
        self.next_btn = None
        self.return_btn = None
        self.current_page = 1
        self.entries_per_page = 5

    def render(self) -> None:
        """
        Render the leaderboard screen
        """
        self.display.fill(self.colors.BROWN)

        self.display_message(message="Leaderboard",
                             font_color=self.colors.GREEN,
                             text_position=(self.display.get_width() // 2, 100),
                             font_size=64
                             )

        # Sample leaderboard data, sorted by waves in descending order
        self.leaderboard_data = [
            ("Player 1", 80),
            ("Player 2", 70),
            ("Player 3", 60),
            ("Player 4", 55),
            ("Player 5", 50),
            ("Player 6", 45),
            ("Player 7", 40),
            ("Player 8", 35),
            ("Player 9", 30),
            ("Player 10", 25),
            ("Player 11", 20),
            ("Player 12", 15),
            ("Player 13", 10)
        ]

        # Calculate the range of entries to display based on the current page number
        start_index = (self.current_page - 1) * self.entries_per_page
        end_index = start_index + self.entries_per_page
        display_data = self.leaderboard_data[start_index:end_index]

        # Display leaderboard data
        x, y = 360, 160
        for idx, (username, waves) in enumerate(display_data, start=start_index + 1):
            line = f"{idx}. {username}: Waves {waves}"
            self.display_message(message=line,
                                 font_color=self.colors.WHITE,
                                 text_position=(x, y)
                                 )
            y += 50  # Adjust vertical spacing for the next line

        # Calculate button position based on a fixed vertical offset from the bottom
        button_width, button_height = 150, 50
        padding = 30  # Padding between buttons and text
        bottom_offset = 300  # Offset from the bottom of the screen
        left_button_x = x - padding
        right_button_x = x + button_width + padding
        button_y = self.display.get_height() - bottom_offset

        # Render "Previous" button aligned to the left
        self.previous_btn = self.display_button(message="Previous",
                                                button_position=(left_button_x, button_y),
                                                button_size=(button_width, button_height)
                                                )
        # Render "Next" button aligned to the right
        self.next_btn = self.display_button(message="Next",
                                            button_position=(right_button_x, button_y),
                                            button_size=(button_width, button_height)
                                            )

        # Disable previous button if already on the first page
        if self.current_page == 1:
            self.previous_btn = self.display_button(message="Previous",
                                                    button_position=(left_button_x, button_y),
                                                    button_size=(button_width, button_height),
                                                    button_color=self.colors.GRAY,
                                                    hover_color=self.colors.GRAY
                                                    )
        # Disable next button if no more pages left
        if end_index >= len(self.leaderboard_data):
            self.next_btn = self.display_button(message="Next",
                                                button_position=(right_button_x, button_y),
                                                button_size=(button_width, button_height),
                                                button_color=self.colors.GRAY,
                                                hover_color=self.colors.GRAY
                                                )

        # Calculate the center position for the "Return to Main Menu" button
        return_button_width, return_button_height = 300, 70
        return_button_x = (self.display.get_width() - return_button_width) // 2
        return_button_y = button_y + 100  # Offset from the "Next" button

        # Render "Return to Main Menu" button aligned to the center
        self.return_btn = self.display_button(message="Return to Main Menu",
                                              button_position=(return_button_x, return_button_y),
                                              button_size=(return_button_width, return_button_height)
                                              )

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the leaderboard screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        if self.return_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("MainMenuScreen")
        if self.previous_btn.collidepoint(mouse_pos) and self.current_page > 1:
            self.current_page -= 1
        elif (self.next_btn.collidepoint(mouse_pos) and
              (self.current_page * self.entries_per_page) < len(self.leaderboard_data)):
            self.current_page += 1
