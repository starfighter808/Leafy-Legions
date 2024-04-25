"""
Leafy Legions: AlmanacScreen

This module contains the AlmanacScreen class
for managing functions used in the Almanac section of the application
"""

# Standard Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from entities import Plant, Zombie
from screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import ScreenManager


def grab_attributes() -> dict[str, dict[str, any]]:
    """
    Grab attributes from all classes and subclasses of Plant and Zombie.

    Returns:
        dict[str, dict[str, any]]: A dictionary containing class names as keys and their attributes as values.
    """
    all_attributes: dict[str, dict[str, any]] = {}
    for entity_class in [Plant, Zombie]:
        subclasses = entity_class.__subclasses__()
        all_subclasses = [entity_class] + subclasses
        for subclass in all_subclasses:
            instance = subclass(None, 0, 0)  # Instantiate the class
            attributes = instance.attributes
            if 'images' in attributes:
                attributes['images'] = attributes['images'][0]  # Grab the first image
            all_attributes[subclass.__name__] = attributes
    return all_attributes


class AlmanacScreen(BaseScreen):
    """
    The AlmanacScreen renders the "Almanac"
    section of the application
    """

    def __init__(self, screen_manager: 'ScreenManager', display: pygame.Surface) -> None:
        """
        Initialize the Almanac screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (pygame.Surface): The pygame display
        """
        super().__init__(screen_manager, display, title="Leafy Legions: Almanac")
        self.almanac_data = None
        self.previous_btn = None
        self.next_btn = None
        self.return_btn = None
        self.current_page = 1

    def render(self) -> None:
        """
        Render the Almanac screen
        """
        self.display.fill(self.colors.BROWN)

        self.display_message(message="Almanac",
                             font_color=self.colors.GREEN,
                             text_position=(self.display.get_width() // 2, 50),
                             font_size=64
                             )

        self.almanac_data = grab_attributes()

        # Calculate the range of entries to display based on the current page number
        start_index = self.current_page - 1
        end_index = start_index + 1
        display_data = list(self.almanac_data.values())[start_index:end_index]

        # # Display almanac data
        x, y = 360, 330
        for attributes in display_data:
            # Add the almanac background
            self.display_image(image_filename="almanac.png",
                               image_position=(self.display.get_width() // 2, y),
                               image_size=(396, 474)
                               )

            self.display_message(message=attributes["name"],
                                 font_color=self.colors.WHITE,
                                 text_position=(self.display.get_width() // 2, y - 220)
                                 )

            self.display_image(image_filename=attributes["images"],
                               image_position=(self.display.get_width() // 2, y - 85),
                               image_size=(140, 140)
                               )

            self.display_message(message=attributes["description"],
                                 font_color=self.colors.WHITE,
                                 text_position=(self.display.get_width() // 4 + 75, y + 40),
                                 text_align="topleft",
                                 allowed_width=370,
                                 font_size=32
                                 )

        # Calculate button position based on a fixed vertical offset from the bottom
        button_width, button_height = 150, 50
        padding = 30  # Padding between buttons and text
        bottom_offset = 190  # Offset from the bottom of the screen
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
        if end_index >= len(self.almanac_data):
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
        Handle events on the almanac screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        if self.return_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("MainMenuScreen")
        if self.previous_btn.collidepoint(mouse_pos) and self.current_page > 1:
            self.current_page -= 1
        elif self.next_btn.collidepoint(mouse_pos) and self.current_page < len(self.almanac_data):
            self.current_page += 1
