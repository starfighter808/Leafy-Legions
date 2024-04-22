"""
Leafy Legions: MainMenuScreen

This module contains the MainMenuScreen class
for managing the start-up screen in the game
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


class MainMenuScreen(BaseScreen):
    """
    The MainMenuScreen renders the
    starting page of the application
    """

    def __init__(self, screen_manager: 'ScreenManager', display: pygame.Surface) -> None:
        """
        Initialize the Main Menu screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (pygame.Surface): The pygame display
        """
        super().__init__(screen_manager, display, title="Leafy Legions: Main Menu")
        self.sign_in_btn = None
        self.leaderboard_btn = None
        self.quit_btn = None

    def render(self) -> None:
        """
        Render the main menu screen.
        """
        # Background color
        self.display.fill(self.colors.BROWN)

        # Render "Leafy Legions" message
        # self.display_message(message="Leafy Legions",
        #                      font_color=self.colors.GREEN,
        #                      text_position=(self.display.get_width() // 2, 100),
        #                      font_size=64
        #                      )

        # Add a logo to the top of the screen
        self.display_image(image_filename="rellisLogo.png",
                           image_position=(self.display.get_width() // 2, 125),
                           image_size=(150, 169)
                           )

        # Button Size
        button_width = 250
        button_height = 70

        # Button position calculations
        button_x = (self.display.get_width() - button_width) // 2
        total_height = (button_height * 3) + (125 // 2)  # Total height of all buttons and spacing
        sign_in_btn_y = (self.display.get_height() - total_height) // 2
        leaderboard_btn_y = sign_in_btn_y + button_height + 100  # Adjusted positioning for the leaderboard button
        quit_btn_y = leaderboard_btn_y + button_height + 100

        # Render buttons and define as attributes
        if self.screen_manager.user_logged_in:
            sign_in_btn_label = "Start"
        else:
            sign_in_btn_label = "Sign In / Sign Up"

        # Render buttons and define as attributes
        self.sign_in_btn = self.display_button(message=sign_in_btn_label,
                                               button_position=(button_x, sign_in_btn_y),
                                               button_size=(button_width, button_height)
                                               )
        self.leaderboard_btn = self.display_button(message="Leaderboard",
                                                   button_position=(button_x, leaderboard_btn_y),
                                                   button_size=(button_width, button_height)
                                                   )
        self.quit_btn = self.display_button(message="Quit",
                                            button_position=(button_x, quit_btn_y),
                                            button_size=(button_width, button_height)
                                            )

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the leaderboard screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        if self.sign_in_btn.collidepoint(mouse_pos):
            if self.screen_manager.user_logged_in:
                self.screen_manager.set_screen("GameplayScreen")
            else:
                self.screen_manager.set_screen("SignInSignUpScreen")
        elif self.leaderboard_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("LeaderboardScreen")
        elif self.quit_btn.collidepoint(mouse_pos):
            self.screen_manager.quit()
