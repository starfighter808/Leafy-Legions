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
from src.entities import Plant, Zombie
from src.screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from src.managers import ScreenManager


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
                             text_position=(self.display.get_width() // 2, 70),
                             font_size=64
                             )

        self.almanac_data = grab_attributes()

        # Calculate the range of entries to display based on the current page number
        start_index = self.current_page - 1
        end_index = start_index + 1
        display_data = list(self.almanac_data.values())[start_index:end_index]

        # # Display almanac data
        x, y = self.display.get_width() // 2, 340
        text_and_buttons_x = x - (x * 0.32)
        for attributes in display_data:
            # Add the almanac background
            self.display_image(image_filename="screens/almanac.png",
                               image_position=(x, y),
                               image_size=(396, 474)
                               )

            self.display_message(message=f"The {attributes['name']}",
                                 font_color=self.colors.WHITE,
                                 text_position=(x, y - 220)
                                 )

            self.display_image(image_filename=f"entities/{attributes["images"]}",
                               image_position=(x, y - 85),
                               image_size=(140, 140)
                               )

            self.display_message(message=attributes["description"],
                                 font_color=self.colors.LIGHT_BROWN,
                                 text_position=(text_and_buttons_x, y + 40),
                                 text_align="topleft",
                                 allowed_width=370,
                                 font_size=32
                                 )

        # Calculate button position based on a fixed vertical offset from the bottom
        button_width, button_height = 150, 50
        bottom_offset = 180  # Offset from the bottom of the screen
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

        if end_index >= len(self.almanac_data):
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
        return_button_y = button_y + 80  # Offset from the "Next" button

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
        super().handle_click_events(mouse_pos)
        if self.return_btn and self.return_btn.collidepoint(mouse_pos):
            self.screen_manager.set_screen("MainMenuScreen")
        if self.previous_btn and self.previous_btn.collidepoint(mouse_pos) and self.current_page > 1:
            self.current_page -= 1
        elif self.next_btn and self.next_btn.collidepoint(mouse_pos) and self.current_page < len(self.almanac_data):
            self.current_page += 1
