from enum import Enum
import pygame
import random
import time

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


block_size = 16
window_width = 1280
window_height = 720
x_blocks = window_width/block_size
y_blocks = window_height/block_size
global score
score = 0
fps = 8

pygame.init()
pygame.display.set_caption("Sanke")
window = pygame.display.set_mode((window_width, window_height))

refresh_controller = pygame.time.Clock()

snake_position = [x_blocks//2*block_size, y_blocks//2*block_size]
snake_body = [[snake_position[0], snake_position[1]],
              [snake_position[0], snake_position[1]+block_size],
              [snake_position[0], snake_position[1]+block_size*2]]

def generate_new_food():
    food_position[0] = random.randint(block_size, ((window_width-block_size)//block_size))*block_size
    food_position[1] = random.randint(block_size, ((window_height-block_size)//block_size))*block_size

global food_position
food_position = [0, 0]
generate_new_food()


def handle_keys(direction):
    new_direction = direction
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_UP and direction != Direction.DOWN:
            new_direction = Direction.UP
        if event.key == pygame.K_DOWN and direction != Direction.UP:
            new_direction = Direction.DOWN
        if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
            new_direction = Direction.LEFT
        if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
            new_direction = Direction.RIGHT
    return new_direction
        

def move_snake(direction):
    if direction == Direction.UP:
        snake_position[1] -= block_size
    elif direction == Direction.DOWN:
        snake_position[1] += block_size
    elif direction == Direction.LEFT:
        snake_position[0] -= block_size
    elif direction == Direction.RIGHT:
        snake_position[0] += block_size
    
    snake_body.insert(0, list(snake_position))


def get_food():
    global score
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 10
        generate_new_food()
    else:
        snake_body.pop()


def repaint():
    window.fill(pygame.Color(0, 0, 0))
    for body in snake_body:
        pygame.draw.rect(window, pygame.Color(100,225,0), pygame.Rect(body[0], body[1], block_size, block_size))
    
    pygame.draw.circle(window, pygame.Color(225, 0, 0), (food_position[0]+block_size/2, food_position[1]+block_size/2), block_size/2)


def game_over_message():
    font = pygame.font.SysFont('Arial', 48)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width/2, window_height/2)
    window.blit(render, rect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    exit(0)


def game_over():
    if snake_position[0] < 0 or snake_position[0] > window_width-block_size:
        game_over_message()
    if snake_position[1] < 0 or snake_position[1] > window_height-block_size:
        game_over_message()
    
    for body_part in snake_body[1:]:
        if snake_position[0] == body_part[0] and snake_position[1] == body_part[1]:
            game_over_message()


def paint_hud():
    font = pygame.font.SysFont('Arial', 20)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    window.blit(render, rect)
    pygame.display.flip()


def game_loop():
    direction = Direction.UP
    
    while True:
        direction = handle_keys(direction)
        move_snake(direction)
        get_food()
        repaint()
        game_over()
        paint_hud()
        pygame.display.update()
        refresh_controller.tick(fps)
        

if __name__ == "__main__":
    game_loop()