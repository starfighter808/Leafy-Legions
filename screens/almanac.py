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
                             text_position=(self.display.get_width() // 2, 100),
                             font_size=64
                             )

        # Sample Almanac data, sorted by waves in descending order
        self.almanac_data = [
            ("The Cowboy",
             "plant.png",
             "A sharpshooting sentinel with a ten-gallon hat and a lasso, it wrangles foes while providing cover. "
             "Agile and precise, it turns the tide with its quick reflexes and summons allies to stampede to victory!"
            ),
            ("The Sprinter",
             "speedyZombie.png",
             "A decaying blur of tattered clothes and gnashing teeth, sprinting towards prey with lightning speed."
                "Fragile but swift, it hunts down survivors with relentless agility, "
                "posing a constant threat to the unprepared."
             )
        ]

        # Calculate the range of entries to display based on the current page number
        start_index = (self.current_page - 1)
        end_index = start_index + 1
        display_data = self.almanac_data[start_index:end_index]

        # # Display almanac data
        x, y = 360, 430
        for idx, (plant_name, plant_img, plant_desc) in enumerate(display_data, start=start_index + 1):
            # Add the almanac background
            self.display_image(image_filename="almanac.png",
                               image_position=(self.display.get_width() // 2 - 15, y)
                               )

            self.display_message(message=plant_name,
                                 font_color=self.colors.WHITE,
                                 text_position=(self.display.get_width() // 2, y - 283)
                                 )

            self.display_image(image_filename=plant_img,
                               image_position=(self.display.get_width() // 2, y - 160),
                               image_size=(140, 140)
                               )

            self.display_message(message=plant_desc,
                                 font_color=self.colors.WHITE,
                                 text_position=(self.display.get_width() // 4 + 95, y - 45),
                                 text_align="topleft",
                                 allowed_width=340,
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
        elif (self.next_btn.collidepoint(mouse_pos) and
              (self.current_page) < len(self.almanac_data)):
            self.current_page += 1
