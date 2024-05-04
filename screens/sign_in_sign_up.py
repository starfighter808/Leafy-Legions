"""
Leafy Legions: SignInSignUpScreen

This module contains the SignInSignUpScreen class
for managing the Sign In and Sign Up screen in the application
"""
# Standard Imports
from typing import TYPE_CHECKING

# Library Imports
import pygame

# Local Imports
from managers import ColorManager
from screens import BaseScreen

# The following packages are imported only for type hinting.
# They are not used in this package, preventing circular dependency errors.
if TYPE_CHECKING:
    from managers import ScreenManager


class SignInSignUpScreen(BaseScreen):
    """
    The SignInSignUpScreen renders the "Sign In/Sign Up"
    section of the application. It only displays if the
    user is not already logged into the application.
    """
    def __init__(self, screen_manager: 'ScreenManager', display: pygame.Surface) -> None:
        """
        Initialize the Sign In/Sign Up screen.

        Args:
            screen_manager (ScreenManager): The screen manager of the application
            display (pygame.Surface): The pygame display
        """
        super().__init__(screen_manager, display, title="Leafy Legions: Sign In/Sign Up")
        self.colors = ColorManager()
        self.input_rect_username = pygame.Rect((self.display.get_width() // 2 - 125, 200, 250, 40))
        self.input_rect_password = pygame.Rect((self.display.get_width() // 2 - 125, 300, 250, 40))
        self.font = pygame.font.Font(None, 32)
        self.username_active = False
        self.password_active = False
        self.username_text = ''
        self.password_text = ''
        self.username_surface = self.font.render(self.username_text, True, self.colors.WHITE)
        self.password_surface = self.font.render("*" * len(self.password_text), True, self.colors.WHITE)

        self.sign_up_btn = None
        self.sign_in_btn = None
        self.return_btn = None
        self.error_text = ''

    def render(self) -> None:
        """
        Render the Sign In/Sign Up screen
        """
        self.display.fill(self.colors.BROWN)

        self.display_message(message="Sign In/Sign Up",
                             font_color=self.colors.GREEN,
                             text_position=(self.display.get_width() // 2, 100),
                             font_size=64
                             )

        # Render labels for username and password
        username_label = self.font.render("Username:", True, self.colors.WHITE)
        password_label = self.font.render("Password:", True, self.colors.WHITE)
        self.display.blit(username_label, (self.input_rect_username.x, self.input_rect_username.y - 30))
        self.display.blit(password_label, (self.input_rect_password.x, self.input_rect_password.y - 30))

        # Render username and password input boxes
        pygame.draw.rect(self.display,
                         self.colors.LIGHT_BLUE
                         if self.username_active
                         else self.colors.GRAY,
                         self.input_rect_username,
                         2
                         )

        self.display.blit(self.username_surface, (self.input_rect_username.x + 5, self.input_rect_username.y + 5))

        pygame.draw.rect(self.display,
                         self.colors.LIGHT_BLUE
                         if self.password_active
                         else self.colors.GRAY,
                         self.input_rect_password,
                         2
                         )
        self.display.blit(self.password_surface, (self.input_rect_password.x + 5, self.input_rect_password.y + 5))

        if self.error_text:
            error_text = self.font.render(self.error_text, True, self.colors.RED)
            self.display.blit(error_text, (self.display.get_width() // 2 - error_text.get_width() // 2, 350))

        # Render Sign In and Sign Up buttons horizontally
        button_width, button_height = 150, 50
        button_x = self.display.get_width() // 2 - button_width // 2
        button_y = 400

        self.sign_in_btn = self.display_button(message="Sign In",
                                               button_position=(button_x, button_y),
                                               button_size=(button_width, button_height)
                                               )

        self.sign_up_btn = self.display_button(message="Sign Up",
                                               button_position=(button_x + button_width + 20, button_y),
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
        Handle click events on the sign-in/sign-up screen.

        Args:
            mouse_pos (Tuple[int, int]): The position of the mouse cursor.
        """
        super().handle_click_events(mouse_pos)
        if self.input_rect_username.collidepoint(mouse_pos):
            self.username_active = True
            self.password_active = False
        elif self.input_rect_password.collidepoint(mouse_pos):
            self.password_active = True
            self.username_active = False
        else:
            self.username_active = False
            self.password_active = False
            if self.sign_in_btn.collidepoint(mouse_pos):
                if self.database_manager.verify_login(self.username_text, self.password_text):
                    self.screen_manager.set_screen("MainMenuScreen")
                    self.screen_manager.user_logged_in = self.username_text
                else:
                    if self.username_text == '' or self.password_text == '':
                        self.error_text = "Username and password cannot be blank"
                    else:
                        self.error_text = "Invalid username or password"

            elif self.sign_up_btn.collidepoint(mouse_pos):
                if self.database_manager.create_user(self.username_text, self.password_text):
                    self.screen_manager.set_screen("MainMenuScreen")
                    self.screen_manager.user_logged_in = self.username_text
                else:
                    if self.username_text == '' or self.password_text == '':
                        self.error_text = "Username and password cannot be blank"
                    else:
                        self.error_text = "Username already exists"
            elif self.return_btn.collidepoint(mouse_pos):
                self.screen_manager.set_screen("MainMenuScreen")

    def handle_key_events(self, key_pressed: int, unicode_char: str) -> None:
        """
        Handle key press events on the sign-in/sign-up screen.

        Args:
            key_pressed (int): The key pressed on the keyboard in integer form
            unicode_char (str): The value that the key represents
        """
        # Ignore ENTER key
        if key_pressed == pygame.K_RETURN:
            unicode_char = ""
        # If tab key, cycle between both fields
        if key_pressed == pygame.K_TAB:
            unicode_char = ""
            if self.username_active:
                self.username_active = False
                self.password_active = True
            else:
                self.username_active = True
                self.password_active = False

        if self.username_active:
            if key_pressed == pygame.K_BACKSPACE:
                self.username_text = self.username_text[:-1]
            else:
                self.username_text += unicode_char

            self.username_surface = self.font.render(self.username_text,
                                                     True,
                                                     self.colors.LIGHT_BLUE
                                                     if self.username_active
                                                     else self.colors.GRAY
                                                     )
        if self.password_active:
            if key_pressed == pygame.K_BACKSPACE:
                self.password_text = self.password_text[:-1]
            else:
                self.password_text += unicode_char

            self.password_surface = self.font.render("*" * len(self.password_text),
                                                     True,
                                                     self.colors.LIGHT_BLUE
                                                     if self.password_active
                                                     else self.colors.GRAY
                                                     )
