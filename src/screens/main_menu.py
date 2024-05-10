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
from src.screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import ScreenManager


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
        self.almanac_btn = None
        self.quit_btn = None
        self.sound_manager.play_music('main_menu.mp3')

    def render(self) -> None:
        """
        Render the main menu screen.
        """
        # Background color
        self.display.fill(self.colors.BROWN)

        # Calculate the vertical space occupied by the image
        image_height = 169
        image_margin_bottom = 10  # Additional space between the image and the buttons

        # Button Size
        button_width = 250
        button_height = 70

        # Button position calculations
        button_x = (self.display.get_width() - button_width) // 2

        # Total height including image and button spacing
        total_height = (button_height * 4) + image_height + image_margin_bottom
        button_gap = (self.display.get_height() - total_height) // 5  # Gap between each button and the image

        # Calculate the y positions for each button
        self.image_y = button_gap + 50  # Move image a bit down
        sign_in_btn_y = self.image_y + image_height + image_margin_bottom + button_gap - 110  # Move buttons a bit up
        leaderboard_btn_y = sign_in_btn_y + button_height + button_gap
        almanac_btn_y = leaderboard_btn_y + button_height + button_gap
        quit_btn_y = almanac_btn_y + button_height + button_gap

        # Render buttons and define as attributes
        if self.screen_manager.user_logged_in:
            sign_in_btn_label = "Start"
        else:
            sign_in_btn_label = "Sign In / Sign Up"

        self.sign_in_btn = self.display_button(message=sign_in_btn_label,
                                               button_position=(button_x, sign_in_btn_y),
                                               button_size=(button_width, button_height)
                                               )
        self.leaderboard_btn = self.display_button(message="Leaderboard",
                                                   button_position=(button_x, leaderboard_btn_y),
                                                   button_size=(button_width, button_height)
                                                   )
        self.almanac_btn = self.display_button(message="Almanac",
                                               button_position=(button_x, almanac_btn_y),
                                               button_size=(button_width, button_height)
                                               )
        self.quit_btn = self.display_button(message="Quit",
                                            button_position=(button_x, quit_btn_y),
                                            button_size=(button_width, button_height)
                                            )

        # Add a logo to the top of the screen
        self.display_image(image_filename="screens/rellisLogo.png",
                           image_position=(self.display.get_width() // 2, self.image_y),
                           image_size=(150, 169)
                           )

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the leaderboard screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        super().handle_click_events(mouse_pos)
        if self.sign_in_btn and self.sign_in_btn.collidepoint(mouse_pos):
            if self.screen_manager.user_logged_in:
                self.screen_manager.set_screen("GameplayScreen")
            else:
                self.screen_manager.set_screen("SignInSignUpScreen")
        elif self.leaderboard_btn and self.leaderboard_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("LeaderboardScreen")
        elif self.almanac_btn and self.almanac_btn.collidepoint(mouse_pos):  # Handle click event for the almanac button
            self.screen_manager.set_screen("AlmanacScreen")
        elif self.quit_btn and self.quit_btn.collidepoint(mouse_pos):
            self.screen_manager.quit()
