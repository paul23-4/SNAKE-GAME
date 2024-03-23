import pygame
import argparse
from food import Food
from snake import Snake
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('snake_game.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    score INTEGER
)
''')
conn.commit()

# Define constants
WIDTH = 640
HEIGHT = 480

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Define cell size and initial FPS for each difficulty level
CELL_SIZE = 20
DIFFICULTY_LEVELS = {
    "easy": 5,
    "medium": 10,
    "hard": 15
}

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game class
class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.paused = False
        self.score = 0
        self.high_score = 0
        self.difficulty_level = "easy"  # Default difficulty level
        self.fps = DIFFICULTY_LEVELS[self.difficulty_level]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_p:  # Pause the game
                        self.paused = not self.paused
                else:
                    if event.key == pygame.K_r:  # Restart the game
                        self.restart_game()
                    elif event.key == pygame.K_q:  # Quit the game
                        pygame.quit()
                        quit()

    def restart_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        self.score = 0
        self.fps = DIFFICULTY_LEVELS[self.difficulty_level]

    def update(self):
        if not self.game_over and not self.paused:
            self.snake.move()

            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food.position = self.food.randomize_position()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score

            if self.snake.check_collision() or self.snake.check_boundary_collision(WIDTH, HEIGHT):
                self.game_over = True
                self.save_score()

    def save_score(self):
        name = input("Enter your name: ")
        if name:
            cursor.execute('INSERT INTO users (name, score) VALUES (?,?)', (name, self.score))
            conn.commit()
            self.restart_game()  # Restart the game after saving the score

    def draw(self):
        self.screen.fill(BLACK)

        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(self.screen, RED, (self.food.position[0] * CELL_SIZE, self.food.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Display scores
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 30))

        if self.game_over:
            game_over_text = font.render("Game Over - Press 'R' to restart or 'Q' to quit", True, WHITE)
            self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2 - game_over_text.get_height() // 2))

        if self.paused:
            paused_text = font.render("Paused - Press 'P' to resume", True, WHITE)
            self.screen.blit(paused_text, (self.width // 2 - paused_text.get_width() // 2, self.height // 2 - paused_text.get_height() // 2))

        pygame.display.update()

    def run(self):
        running = True
        while running:
            self.handle_events()  # Handle user input
            self.update()         # Update game state
            self.draw()           # Draw game scene
            self.clock.tick(self.fps)  # Cap the frame rate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=WIDTH, help="Width of the game window")
    parser.add_argument("--height", type=int, default=HEIGHT, help="Height of the game window")
    args = parser.parse_args()

    game = Game(args.width, args.height)
    game.run()
