import pygame
import sys
import random
import asyncio

# Global constants
WIDTH, HEIGHT = 800, 600
FPS = 40

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Car Game')

# Load fonts
test_font = pygame.font.Font('Pixeltype.ttf', 60)

# Load images
road_surface = pygame.image.load("road.png").convert_alpha()
road_surface = pygame.transform.scale(road_surface, (WIDTH, HEIGHT))

car_image = pygame.image.load('car.png').convert_alpha()
scaled_car = pygame.transform.scale(car_image, (car_image.get_width() // 3.2, car_image.get_height() // 3.2))

bomb = pygame.image.load("bomb.png").convert_alpha()
bomb_image = pygame.transform.scale(bomb, (bomb.get_width() // 0.6, bomb.get_height() // 0.6))

# Initialize game variables
game_active = False
start_time = 0
obstacles = []
road_y = 0
obstacle_frequency = 50
obstacle_speed = 5
car_rect = scaled_car.get_rect(center=(WIDTH // 2, HEIGHT - 300))
scrolling_road = pygame.Surface((WIDTH, HEIGHT * 2), pygame.SRCALPHA)
clock = pygame.time.Clock()

# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Function to handle player input
def handle_input():
    keys = pygame.key.get_pressed()
    if game_active:
        if keys[pygame.K_LEFT] and car_rect.left > 0:
            car_rect.x -= 5
        if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
            car_rect.x += 5
        if keys[pygame.K_UP] and car_rect.top > 0:
            car_rect.y -= 5
        if keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:
            car_rect.y += 5

# Function to draw the player's score
def draw_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render(f'Score: {current_time // 1000}', False, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# Function to draw obstacles on the screen
def draw_obstacles():
    for obstacle_rect in obstacles:
        screen.blit(bomb_image, obstacle_rect)

# Function to update the display
def update_display():
    pygame.display.update()

# Function to cap the frame rate
def cap_frame_rate():
    clock.tick(FPS)

# Function to display the game introduction screen
def game_intro():
    intro = True

    game_intro_text = test_font.render("Evade Bombs", True, (255, 255, 255))
    game_intro_rect = game_intro_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))

    start_text = test_font.render("Press S to start", True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=(WIDTH // 2 + 10, HEIGHT // 2 + 160))

    car_intro_rect = scaled_car.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while intro:
        screen.fill((64, 64, 64))
        screen.blit(game_intro_text, game_intro_rect)
        screen.blit(start_text, start_text_rect)
        screen.blit(scaled_car, car_intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    reset_game()
                    intro = False

        pygame.display.flip()

# Function to display the game over screen
def game_over_screen():
    screen.fill((64, 64, 64))  # Fill the screen with a background color
    game_over_text = test_font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    score_text = test_font.render(f"Your Score: {current_score // 1000}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 0))

    restart_text = test_font.render("Press R to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    waiting_for_key = False

# Function to reset the game state
def reset_game():
    global game_active, start_time, obstacles, road_y, obstacle_frequency, obstacle_speed
    game_active = True
    start_time = pygame.time.get_ticks()
    obstacles = []
    road_y = 0
    obstacle_frequency = 50
    obstacle_speed = 5
    car_rect.center = (WIDTH // 2, HEIGHT - 300)

# Main game loop
async def main():
    global game_active, road_speed, road_y, obstacle_speed, obstacle_frequency, obstacles, difficulty_level, current_score
    game_active = True
    road_speed = 5
    road_y = 0
    obstacle_speed = 5
    obstacle_frequency = 45
    obstacles = []
    difficulty_level = 1
    current_score = 0

    while True:
        handle_events()
        handle_input()

        # Scroll the road
        road_y += road_speed

        scrolling_road.fill((0, 0, 0, 0))
        scrolling_road.blit(road_surface, (0, road_y % HEIGHT))
        scrolling_road.blit(road_surface, (0, (road_y % HEIGHT) - HEIGHT))

        # Spawn obstacles
        if game_active and random.randint(1, obstacle_frequency) == 1:
            obstacle_rect = bomb_image.get_rect()
            obstacle_rect.x = random.randint(10, WIDTH - obstacle_rect.width)
            obstacle_rect.y = -obstacle_rect.height
            obstacles.append(obstacle_rect)

        # Move obstacles
        for obstacle_rect in obstacles:
            obstacle_rect.y += obstacle_speed

        # Remove obstacles that have gone off the screen
        obstacles = [obs for obs in obstacles if obs.y < HEIGHT]

        # Check for collisions with obstacles
        for obstacle_rect in obstacles:
            if car_rect.colliderect(obstacle_rect):
                game_active = False
                obstacles = []

        if not game_active:
            game_over_screen()

        screen.blit(scrolling_road, (0, 0))
        screen.blit(scaled_car, car_rect)
        draw_obstacles()

        current_score = draw_score()
        current_score_copy = current_score / 1000

        print(current_score_copy)

        if current_score_copy > 10:
            obstacle_speed += 0.00001 * difficulty_level
            if obstacle_frequency > 29:
                obstacle_frequency -= 1

        if current_score_copy > 2 and difficulty_level < 10:
            difficulty_level += 0.0001

        update_display()
        cap_frame_rate()
        await asyncio.sleep(0)  # Allow other tasks to run

game_intro()
asyncio.run(main())
