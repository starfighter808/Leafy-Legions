"""
Leafy Legions: BaseScreen

This module contains the BaseScreen class
for managing functions used in any Screen in the game
"""
# Standard Imports
from abc import ABC, abstractmethod
import os
import sys
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from src.managers import ColorManager

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import ScreenManager


class BaseScreen(ABC):
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
        self.sound_manager = self.screen_manager.sound_manager
        self.button_hover_states = {}  # Dictionary to store hover states of buttons
        self.database_manager = self.screen_manager.database_manager
        pygame.display.set_caption(title)

    def display_message(self,
                        message: str,
                        font_color: tuple[int, int, int],
                        text_position: tuple[float, float],
                        text_align: str = "center",
                        font_size: int = 36,
                        alpha: int = 255,
                        allowed_width: int = None
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
            allowed_width (int): The allowed width for text wrapping
        """
        font = pygame.font.Font(None, font_size)

        # Wrap text if allowed_width is provided
        if allowed_width:
            wrapped_lines = []
            space_width = font.size(' ')[0]
            words = message.split(' ')
            width, _ = font.size(message)
            line = ''
            for word in words:
                word_width = font.size(word)[0]
                if width + word_width < allowed_width:
                    line += word + ' '
                    width += word_width + space_width
                else:
                    wrapped_lines.append(line)
                    line = word + ' '
                    width = word_width + space_width
            wrapped_lines.append(line)

            wrapped_lines = [line for line in wrapped_lines if line.strip()]

            # Render wrapped lines
            text_lines = [font.render(line, True, font_color) for line in wrapped_lines]
            line_height = font.get_height()
            text_height = line_height * len(text_lines)

            # Create a surface for wrapped text
            text = pygame.Surface((allowed_width, text_height), pygame.SRCALPHA)
            for i, text_line in enumerate(text_lines):
                text.blit(text_line, (0, i * line_height))

        else:
            text = font.render(message, True, font_color)

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
                       font_size: int = 36,
                       button_size: tuple[int, int] = (200, 50),
                       offset_text: tuple = (0, 0),
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
            font_size (int): The size of the font. Default: 36
            button_size (tuple[int, int]):  The size of the button (width, height). Default: (200, 50)
            offset_text (tuple): The offset of the text from the button position. Default: None
            alpha (int): The alpha value for transparency. Default: 255 (fully opaque)

        Returns:
            pygame.Rect: The rectangle representing the button area.
        """
        if button_color is None:
            button_color = self.colors.GREEN
        if hover_color is None:
            hover_color = self.colors.LIGHT_BLUE

        font = pygame.font.Font(None, font_size)
        button_text: pygame.Surface = font.render(message, True, self.colors.WHITE)
        button_text.set_alpha(alpha)
        button_rect = button_text.get_rect(topleft=button_position)

        # Adjust button size
        button_rect.width, button_rect.height = button_size

        button_pos_tuple = (button_rect.x, button_rect.y)

        # Draw the regular buttons
        border_color = tuple(max(0, c - 15) for c in button_color)
        pygame.draw.rect(self.display, button_color, button_rect, border_radius=5)
        pygame.draw.rect(self.display, border_color, button_rect, border_radius=5, width=2)

        # If there is a hover color and the mouse is over the button, draw the hover color
        if hover_color and button_rect.collidepoint(pygame.mouse.get_pos()):
            # Ensure button is not disabled:
            if hover_color is not button_color:
                border_color = tuple(max(0, c - 60) for c in hover_color)
                pygame.draw.rect(self.display, hover_color, button_rect, border_radius=5)
                pygame.draw.rect(self.display, border_color, button_rect, border_radius=5, width=2)

                # Play sound if not already played
                if not self.button_hover_states.get(button_pos_tuple, False):
                    self.button_hover_states[button_pos_tuple] = True
                    self.sound_manager.play_sound('button_hover.mp3')
        else:
            self.button_hover_states[button_pos_tuple] = False

        # Center text within the button
        # Allow user to create an "offset" so that the text is not immediately centered
        text_rect = button_text.get_rect(
            center=(button_rect.center[0] + offset_text[0], button_rect.center[1] + offset_text[1]))

        self.display.blit(button_text, text_rect)
        return button_rect

    def display_image(self,
                      image_filename: str,
                      image_position: tuple[float, float],
                      image_size: tuple[int, int] = None
                      ) -> None:
        """
        Display an image on the current screen.

        Args:
            image_filename (str): The filename of the image located in "/src/assets/images/..." directory.
            image_position (tuple[float, float]): The position of the image (x, y).
            image_size (tuple[int, int]): The size of the image (width, height).
        """
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, f"src/assets/images/{image_filename}")
        else:
            base_path = f"src/assets/images/{image_filename}"

        image = pygame.image.load(base_path)
        if image_size:
            image = pygame.transform.scale(image, image_size)
        image_rect = image.get_rect(center=image_position)
        self.display.blit(image, image_rect)

    def display_button_image(self,
                             image_filename: str,
                             image_position: tuple[float, float],
                             image_size: tuple[int, int],
                             background_color: tuple[int, int, int] = None,
                             hover_color: tuple[int, int, int] = None,
                             ) -> pygame.Rect:
        """
        Display an image as a button on the current screen.

        Args:
            image_filename (str): The filename of the image located in "/src/assets/images/..." directory.
            image_position (tuple[float, float]): The position of the image (x, y).
            image_size (tuple[int, int]): The size of the image (width, height).
            background_color (tuple[int, int, int]): Optional - The color of the button background.
                Default: self.colors.GREEN
            hover_color (tuple[int, int, int]): Optional - The color of the button background when hovered.
                Default: self.colors.LIGHT_BLUE
        """
        if background_color is None:
            background_color = self.colors.GREEN
        if hover_color is None:
            hover_color = self.colors.LIGHT_BLUE

        # Create a surface for the circular background
        background = pygame.Surface(image_size)

        # Check if the mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        if (image_position[0] <= mouse_pos[0] <= image_position[0] + image_size[0]
                and image_position[1] <= mouse_pos[1] <= image_position[1] + image_size[1]):
            pygame.draw.circle(background, hover_color, (image_size[0] // 2, image_size[1] // 2), image_size[0] // 2)
        else:
            pygame.draw.circle(background, background_color, (image_size[0] // 2, image_size[1] // 2),
                               image_size[0] // 2)

        # Load, convert and scale the image
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, f"src/assets/images/{image_filename}")
        else:
            base_path = f"src/assets/images/{image_filename}"

        image = pygame.image.load(base_path).convert_alpha()
        image = pygame.transform.scale(image, image_size)

        # Blit the image onto the center of the background
        image_rect = image.get_rect(center=background.get_rect().center)
        background.blit(image, image_rect)

        # Blit the background onto the display
        button_rect = background.get_rect(topleft=image_position)

        button_pos_tuple = (button_rect.x, button_rect.y)

        # Draw the border
        border_color = tuple(max(0, c - 15) for c in background_color)
        pygame.draw.rect(self.display, background_color, button_rect, border_radius=5)
        pygame.draw.rect(self.display, border_color, button_rect, border_radius=5, width=2)

        # If there is a hover color and the mouse is over the button, draw the hover color
        if hover_color and button_rect.collidepoint(pygame.mouse.get_pos()):
            # Ensure button is not disabled:
            if hover_color is not background_color:
                border_color = tuple(max(0, c - 60) for c in hover_color)
                pygame.draw.rect(self.display, hover_color, button_rect, border_radius=5)
                pygame.draw.rect(self.display, border_color, button_rect, border_radius=5, width=2)

                # Play sound if not already played
                if not self.button_hover_states.get(button_pos_tuple, False):
                    self.button_hover_states[button_pos_tuple] = True
                    self.sound_manager.play_sound('button_hover.mp3')
        else:
            self.button_hover_states[button_pos_tuple] = False

        # Blit the image directly onto the display
        image_rect = image.get_rect(topleft=image_position)
        self.display.blit(image, image_rect)

        return image_rect

    @abstractmethod
    def render(self) -> None:
        """
        Render the application
        """
        # This function is intentionally left blank and should be overridden in derived classes.
        # It is marked as abstractmethod to require implementation in each derived Screen.
        return

    def handle_key_events(self, key_pressed: int, unicode_char: str) -> None:
        """
        Render when a key is pressed on the keyboard in the
        event that it is not registered by other Screen

        Args:
            key_pressed (int): The key pressed on the keyboard in integer form
            unicode_char (str): The value that the key represents
        """
        # This function is intentionally left blank and should be overridden in derived classes.
        return

    def handle_click_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle events on the leaderboard screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        # After each click, reset the button states to play the sound again
        self.button_hover_states = {}
