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
        self.leaderboard_data = self.database_manager.get_high_scores()

        # Calculate the range of entries to display based on the current page number
        start_index = (self.current_page - 1) * self.entries_per_page
        end_index = start_index + self.entries_per_page
        display_data = self.leaderboard_data[start_index:end_index]

        # Display leaderboard data
        x, y = self.display.get_width() // 2, 150
        text_and_buttons_x = x - (x * 0.32)
        for idx, entry in enumerate(display_data, start=start_index + 1):
            username = entry["username"]
            waves = entry["high_score"]
            line = f"{idx}. {username}: Wave {waves}"
            self.display_message(message=line,
                                 font_color=self.colors.WHITE,
                                 text_position=(text_and_buttons_x, y),
                                 text_align="topleft"
                                 )
            y += 50  # Adjust vertical spacing for the next line

        # Calculate button position based on a fixed vertical offset from the bottom
        button_width, button_height = 150, 50
        bottom_offset = 300  # Offset from the bottom of the screen
        right_button_x = text_and_buttons_x + button_width + 55
        button_y = self.display.get_height() - bottom_offset

        if self.current_page == 1:
            # If there are no more pages, disable button
            self.previous_btn = self.display_button(message="Previous",
                                                    button_position=(text_and_buttons_x, button_y),
                                                    button_size=(button_width, button_height),
                                                    button_color=self.colors.GRAY,
                                                    hover_color=self.colors.GRAY
                                                    )
        else:
            # Otherwise, display the button with normal colors
            self.previous_btn = self.display_button(message="Previous",
                                                    button_position=(text_and_buttons_x, button_y),
                                                    button_size=(button_width, button_height)
                                                    )

        if end_index >= len(self.leaderboard_data):
            # If there are no more pages, disable button
            self.next_btn = self.display_button(message="Next",
                                                button_position=(right_button_x, button_y),
                                                button_size=(button_width, button_height),
                                                button_color=self.colors.GRAY,
                                                hover_color=self.colors.GRAY
                                                )
        else:
            # Otherwise, display the button with normal colors
            self.next_btn = self.display_button(message="Next",
                                                button_position=(right_button_x, button_y),
                                                button_size=(button_width, button_height)
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
        super().handle_click_events(mouse_pos)
        if self.return_btn and self.return_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("MainMenuScreen")
        if self.previous_btn and self.previous_btn.collidepoint(mouse_pos) and self.current_page > 1:
            self.current_page -= 1
        elif self.next_btn and (self.next_btn.collidepoint(mouse_pos) and
              (self.current_page * self.entries_per_page) < len(self.leaderboard_data)):
            self.current_page += 1
