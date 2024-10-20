import pygame
import random

# Initialize pygame
pygame.init()

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sounds
pygame.mixer.music.load("background_music.mp3")  # Background music
eat_sound = pygame.mixer.Sound("eat_sound.mp3")  # Eating sound effect
game_over_sound = pygame.mixer.Sound("game_over.mp3")  # Game over sound effect
pygame.mixer.music.set_volume(0.1)
game_over_sound.set_volume(0.1)
# Load background image
background_image = pygame.image.load("background_image.jpg")

# Define Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # For borders

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
FPS = 15

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game with Boundaries and Background")

# Font for displaying score
font = pygame.font.SysFont("arial", 24)

# Function to display score
def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, [0, 0])

# Function to draw the snake
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])

# Function to draw boundaries
def draw_boundaries():
    # Draw rectangles on each edge of the screen
    pygame.draw.rect(screen, BLUE, [0, 0, SCREEN_WIDTH, GRID_SIZE])  # Top
    pygame.draw.rect(screen, BLUE, [0, SCREEN_HEIGHT - GRID_SIZE, SCREEN_WIDTH, GRID_SIZE])  # Bottom
    pygame.draw.rect(screen, BLUE, [0, 0, GRID_SIZE, SCREEN_HEIGHT])  # Left
    pygame.draw.rect(screen, BLUE, [SCREEN_WIDTH - GRID_SIZE, 0, GRID_SIZE, SCREEN_HEIGHT])  # Right

# Function for the game loop
def game_loop():
    # Start the background music and loop it indefinitely
    pygame.mixer.music.play(-1)

    game_over = False
    game_close = False

    # Initial position of the snake
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2

    # Change in position
    x_change = 0
    y_change = 0

    # Snake starting length and position
    snake_list = []
    snake_length = 1

    # Randomly placing food
    food_x = round(random.randrange(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE * 2) / GRID_SIZE) * GRID_SIZE
    food_y = round(random.randrange(GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE * 2) / GRID_SIZE) * GRID_SIZE

    # Main game loop
    while not game_over:

        while game_close:
            screen.fill(BLACK)
            msg = font.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            screen.blit(msg, [SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3])
            display_score(snake_length - 1)
            pygame.display.update()

            # Play game over sound effect once
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(game_over_sound)

            # Handle the game over events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -GRID_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = GRID_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -GRID_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = GRID_SIZE
                    x_change = 0

        # Update the snake's position
        x += x_change
        y += y_change

        # Check if the snake hits the boundaries
        if x < GRID_SIZE or x >= SCREEN_WIDTH - GRID_SIZE or y < GRID_SIZE or y >= SCREEN_HEIGHT - GRID_SIZE:
            game_close = True

        # Fill screen with the background image
        screen.blit(background_image, [0, 0])

        # Draw boundaries
        draw_boundaries()

        # Draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, GRID_SIZE, GRID_SIZE])

        # Add new segment to the snake's body
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Ensure snake only keeps its length
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if the snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw the snake
        draw_snake(snake_list)

        # Display the score
        display_score(snake_length - 1)

        # Update the display
        pygame.display.update()

        # Check if the snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE * 2) / GRID_SIZE) * GRID_SIZE
            food_y = round(random.randrange(GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE * 2) / GRID_SIZE) * GRID_SIZE
            snake_length += 1

            # Play the eating sound effect
            pygame.mixer.Sound.play(eat_sound)

        # Control the game's speed
        pygame.time.Clock().tick(FPS)

    pygame.quit()
    quit()

# Start the game loop
game_loop()