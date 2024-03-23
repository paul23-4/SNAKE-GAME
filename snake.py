import pygame
import random

# Constants
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# snake.py
class Snake:
    def __init__(self):
        self.body = [(10, 10)]
        self.direction = RIGHT  # Snake starts moving right
        self.grow_pending = 0  # Number of pending segments to grow

    def move(self):
        head = self.body[0]
        x, y = self.direction
        new_head = (head[0] + x, head[1] + y)
        self.body.insert(0, new_head)
        if self.grow_pending == 0:
            self.body.pop()
        else:
            self.grow_pending -= 1

    def grow(self):
        self.grow_pending += 1

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def reset(self):
        self.body = [(10, 10)]
        self.direction = RIGHT
        self.grow_pending = 0

    def check_collision(self):
        head = self.body[0]
        # Check collision with walls
        if (
            head[0] < 0
            or head[0] >= WIDTH // CELL_SIZE
            or head[1] < 0
            or head[1] >= HEIGHT // CELL_SIZE
        ):
            return True
        # Check collision with snake's own body
        if head in self.body[1:]:
            return True
        return False

    def check_boundary_collision(self, width, height):
        # Check if the snake's head has collided with the boundaries of the game window
        x, y = self.body[0]
        return x < 0 or x >= width // CELL_SIZE or y < 0 or y >= height // CELL_SIZE

