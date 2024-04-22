"""
Leafy Legions: BaseScreen

This module contains the BaseScreen class
for managing functions used in any Screen in the game
"""

# Standard Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from managers import ColorManager

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import ScreenManager


class BaseScreen:
    """
    A base class for all screens in the game.
    """

    def __init__(self,
                 screen_manager: 'ScreenManager',
                 display: pygame.Surface,
                 title: str = "Leafy Legions: 404 - Not Found"
                 ) -> None:
        """
        Initialize the base screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (pygame.Surface): The pygame display
        """
        self.screen_manager = screen_manager
        self.display = display
        self.colors = ColorManager
        pygame.display.set_caption(title)

        self.return_btn = None

    def render(self) -> None:
        """
        Render an error screen in the event that one is not properly implemented
        """
        self.display.fill(self.colors.BROWN)
        self.display_message(message="404 - Not Found",
                             font_color=self.colors.GREEN,
                             text_position=(self.display.get_width() // 2, 100),
                             font_size=64
                             )

        self.display_message(message="This page has not yet been implemented",
                             font_color=self.colors.WHITE,
                             text_position=(self.display.get_width() // 2, 200)
                             )

        btn_width, btn_height = 300, 70
        btn_x = (self.display.get_width() - btn_width) // 2
        btn_y = (self.display.get_height() - 300) + 100

        # Render "Return to Main Menu" button aligned to the center
        self.return_btn = self.display_button(message="Return to Main Menu",
                                              button_position=(btn_x, btn_y),
                                              button_size=(btn_width, btn_height)
                                              )
        self.screen_manager.user_logged_in = True

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the leaderboard screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        if self.return_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("MainMenuScreen")

    def display_message(self,
                        message: str,
                        font_color: tuple[int, int, int],
                        text_position: tuple[float, float],
                        text_align: str = "center",
                        font_size: int = 36,
                        alpha: int = 255
                        ) -> None:
        """
        Display a message on the current screen.

        Args:
            message (str): The message to be displayed on the screen.
            font_color (tuple[int, int, int]): The color of the font.
            text_position (tuple[float, float]): The position of the text (x, y).
            text_align (str): The alignment of the text. Default: center
            font_size (int): The font size of the text. Default: 36
            alpha (int): The alpha value for transparency. Default: 255 (fully opaque)
        """
        font = pygame.font.Font(None, font_size)
        text: pygame.Surface = font.render(message, True, font_color)
        text.set_alpha(alpha)
        if text_align == 'center':
            text_rect = text.get_rect(center=text_position)
        elif text_align == 'topleft':
            text_rect = text.get_rect(topleft=text_position)
        else:
            raise ValueError("Invalid argument")

        self.display.blit(text, text_rect)

    def display_button(self,
                       message: str,
                       button_position: tuple[float, float],
                       button_color: tuple[int, int, int] = None,
                       hover_color: tuple[int, int, int] = None,
                       button_size: tuple[int, int] = (200, 50),
                       alpha: int = 255
                       ) -> pygame.Rect:
        """
        Draws a button on the current screen

        Args:
            message (str): The message to be displayed on the button.
            button_position (tuple[float, float]): The position of the button (x, y).
            button_color (tuple[int, int, int]): Optional - The color of the button background.
                Default: self.colors.GREEN
            hover_color (tuple[int, int, int]): Optional - The color of the button background when hovered.
                Default: self.colors.LIGHT_BLUE
            button_size (tuple[int, int]):  The size of the button (width, height). Default: (200, 50)
            alpha (int): The alpha value for transparency. Default: 255 (fully opaque)

        Returns:
            pygame.Rect: The rectangle representing the button area.
        """
        if button_color is None:
            button_color = self.colors.GREEN
        if hover_color is None:
            hover_color = self.colors.LIGHT_BLUE

        font = pygame.font.Font(None, 36)
        button_text: pygame.Surface = font.render(message, True, self.colors.WHITE)
        button_text.set_alpha(alpha)  # Set the alpha value for transparency
        button_rect = button_text.get_rect(topleft=button_position)

        # Adjust button size
        button_rect.width, button_rect.height = button_size

        # Draw the regular buttons
        border_color = tuple(max(0, c - 15) for c in button_color)
        pygame.draw.rect(self.display, button_color, button_rect, border_radius=5)
        pygame.draw.rect(self.display, border_color, button_rect, border_radius=5, width=2)

        # If the mouse is over the buttons, redraw with hover colors
        if hover_color and button_rect.collidepoint(pygame.mouse.get_pos()):
            border_color = tuple(max(0, c - 15) for c in hover_color)
            pygame.draw.rect(self.display, hover_color, button_rect, border_radius=5)
            pygame.draw.rect(self.display, border_color, button_rect, border_radius=5, width=2)

        # Center text within the button
        text_rect = button_text.get_rect(center=button_rect.center)

        self.display.blit(button_text, text_rect)
        return button_rect

    def display_image(self,
                      image_filename: str,
                      image_position: tuple[float, float],
                      image_size: tuple[int, int]
                      ) -> None:
        """
        Display an image on the current screen.

        Args:
            image_filename (str): The filename of the image located in "/assets/images/" directory.
            image_position (tuple[float, float]): The position of the image (x, y).
            image_size (tuple[int, int]): The size of the image (width, height).
        """
        image = pygame.image.load(f"./assets/images/{image_filename}")
        image = pygame.transform.scale(image, image_size)
        image_rect = image.get_rect(center=image_position)
        self.display.blit(image, image_rect)