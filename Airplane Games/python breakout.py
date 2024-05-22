!pip install pygame

import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Paddle
paddle_width = 100
paddle_height = 10
paddle_y = screen_height - 30
paddle_speed = 6

# Ball
ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_dx = 4
ball_dy = -4

# Bricks
brick_width = 75
brick_height = 20
brick_padding = 10
brick_offset_top = 30
brick_offset_left = 30
brick_row_count = 5
brick_column_count = 8

bricks = []

def create_bricks():
    global bricks
    bricks = []
    for row in range(brick_row_count):
        brick_row = []
        for col in range(brick_column_count):
            brick_x = brick_offset_left + col * (brick_width + brick_padding)
            brick_y = brick_offset_top + row * (brick_height + brick_padding)
            brick_row.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
        bricks.append(brick_row)

create_bricks()

# Game variables
lives = 3
level = 1
running = True
game_over = False
clock = pygame.time.Clock()

def reset_game():
    global lives, level, ball_x, ball_y, ball_dx, ball_dy, game_over
    lives = 3
    level = 1
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_dx = 4
    ball_dy = -4
    game_over = False
    create_bricks()

# Main game loop
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_over:
        if keys[pygame.K_r]:
            reset_game()
    else:
        # Move paddle with keyboard
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += paddle_speed

        # Move paddle with mouse
        mouse_x, _ = pygame.mouse.get_pos()
        paddle_x = mouse_x - paddle_width // 2
        paddle_x = max(0, min(paddle_x, screen_width - paddle_width))

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x - ball_radius < 0 or ball_x + ball_radius > screen_width:
            ball_dx = -ball_dx
        if ball_y - ball_radius < 0:
            ball_dy = -ball_dy
        if ball_y + ball_radius > screen_height:
            lives -= 1
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_dy = -ball_dy
            if lives == 0:
                game_over = True

        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if paddle_rect.collidepoint(ball_x, ball_y + ball_radius):
            ball_dy = -ball_dy

        # Ball collision with bricks
        for row in bricks:
            for brick in row:
                if brick.collidepoint(ball_x, ball_y):
                    ball_dy = -ball_dy
                    row.remove(brick)
                    if not row:
                        bricks.remove(row)
                    break

        # Draw paddle
        pygame.draw.rect(screen, blue, paddle_rect)

        # Draw ball
        pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)

        # Draw bricks
        for row in bricks:
            for brick in row:
                pygame.draw.rect(screen, green, brick)

        # Check for level completion
        if not bricks:
            level += 1
            ball_dx += 1
            ball_dy -= 1
            create_bricks()

        # Draw lives and level
        font = pygame.font.Font(None, 36)
        text = font.render(f"Lives: {lives}  Level: {level}", True, white)
        screen.blit(text, (10, 10))

    if game_over:
        # Display Game Over message
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, red)
        screen.blit(text, (screen_width // 2 - 150, screen_height // 2 - 36))
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to Restart", True, white)
        screen.blit(text, (screen_width // 2 - 100, screen_height // 2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
