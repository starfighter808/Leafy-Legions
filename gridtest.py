import pygame
import sys

# Constants defining the grid dimensions, zombie properties, and game settings
GRID_WIDTH = 9
GRID_HEIGHT = 5
GRID_SIZE = 125
ZOMBIE_HEALTH = 100
ZOMBIE_SPEED = 1
SPEEDY_ZOMBIE_SPEED = 3
DAMAGE_PER_HIT = 25
DELAY_MS = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ZOMBIE_IMAGE_PATH = 'creeper.png'
SPEEDY_ZOMBIE_IMAGE_PATH = 'speedyZombie.png'
PLANT_IMAGE_PATH = 'plant.png'
BACKGROUND_IMAGE_PATH = 'Background.jpg'
BACKGROUND_MUSIC_PATH = 'backgroundMusic.wav'

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
pygame.display.set_caption("Leafy Legions Test Display")

# Load images and scale them to match the grid size
zombie_image = pygame.image.load(ZOMBIE_IMAGE_PATH)
zombie_image = pygame.transform.scale(zombie_image, (GRID_SIZE, GRID_SIZE))
speedy_zombie_image = pygame.image.load(SPEEDY_ZOMBIE_IMAGE_PATH)
speedy_zombie_image = pygame.transform.scale(speedy_zombie_image, (GRID_SIZE, GRID_SIZE))
plant_image = pygame.image.load(PLANT_IMAGE_PATH)
plant_image = pygame.transform.scale(plant_image, (GRID_SIZE, GRID_SIZE))
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))

# Initialize Pygame mixer and load background music
pygame.mixer.init()
pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
pygame.mixer.music.play(-1)

# Define the Zombie class
class Zombie:
    def __init__(self, x, y, health, speed, image):
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.image = image

    def update_position(self):
        # Update the zombie's position
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def take_damage(self, damage):
        # Reduce zombie's health by the specified damage
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            # Reset zombie's position if its health drops to zero
            self.reset_position()

    def reset_position(self):
        # Reset zombie's position to the rightmost side of the grid
        self.x = (GRID_WIDTH - 1) * GRID_SIZE

    def draw(self, screen):
        # Draw the zombie on the screen
        screen.blit(self.image, (self.x, self.y))


# Define the SpeedyZombie class inheriting from Zombie
class SpeedyZombie(Zombie):
    def __init__(self, x, y, health):
        super().__init__(x, y, health, SPEEDY_ZOMBIE_SPEED, speedy_zombie_image)


# Define the Plant class
class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = plant_image


    def draw(self, screen):
        # Draw the plant on the screen
        screen.blit(self.image, (self.x, self.y))



zombies = []
plants = []
for i in range(GRID_HEIGHT):
    if i == 1:
        zombies.append(
            SpeedyZombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH))
    else:
        zombies.append(
            Zombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH, ZOMBIE_SPEED,
                   zombie_image))
game_over = False
running = True


# Function to draw the grid lines and background image
def draw_grid():
    screen.blit(background_image, (0, 0))
    for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, GRID_HEIGHT * GRID_SIZE))
    for y in range(0, GRID_HEIGHT * GRID_SIZE, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (GRID_WIDTH * GRID_SIZE, y))


# Function to display a message on the screen
def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(text, text_rect)
    draw_button()
    pygame.display.flip()


def draw_button():
    font = pygame.font.Font(None, 36)
    button_text = font.render("Try Again", True, WHITE)
    button_rect = button_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
    pygame.draw.rect(screen, BLACK, button_rect, border_radius=5)
    screen.blit(button_text, button_rect)


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game if the window is closed
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(screen.get_width() / 2 - 54, screen.get_height() / 2 + 36, 110, 26)
                print('mouse', mouse_pos, 'button', button_rect)
                if button_rect.collidepoint(mouse_pos):
                    zombies = []
                    plants = []
                    for i in range(GRID_HEIGHT):
                        if i == 1:
                            zombies.append(
                                SpeedyZombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH))
                        else:
                            zombies.append(
                                Zombie((GRID_WIDTH - 1) * GRID_SIZE, i * GRID_SIZE, ZOMBIE_HEALTH, ZOMBIE_SPEED,
                                       zombie_image))
                    game_over = False
            else:
                # Plant a plant at the clicked position if the game is not over
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // GRID_SIZE
                grid_y = mouse_y // GRID_SIZE
                if (0 <= grid_x < GRID_WIDTH) and (0 <= grid_y < GRID_HEIGHT):
                    # Plant a plant at the clicked position if it's within the grid
                    new_plant = Plant(grid_x * GRID_SIZE, grid_y * GRID_SIZE)
                    plants.append(new_plant)

    if not game_over:
        # Update and draw zombies and plants
        draw_grid()

        for plant in plants:
            plant.draw(screen)

        for zombie in zombies:
            zombie.update_position()
            zombie.draw(screen)

        # Check if any zombie has reached the left edge of the screen
        if any(zombie.x <= 0 for zombie in zombies):
            game_over = True
            display_message("Your Legion was defeated")

        pygame.display.flip()
        pygame.time.delay(DELAY_MS)

    else:
        # Display game over message and play again button
        draw_grid()
        display_message("Your Legion was defeated")

    pygame.display.flip()

# Quit Pygame and exit the program
pygame.quit()
sys.exit()
