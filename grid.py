import random
import pygame
from snake import Snake
from utils import get_empty_space

class Grid:
    BACKGROUND_COLOR = (150, 150, 150)
    def __init__(self, tilesize, n_tile, pos, snake_pos, head_color=None, body_color=None):
        self.screen = pygame.display.get_surface()
        self.tilesize = tilesize
        self.n_tile = n_tile
        self.pos = pos
        self.snake_pos = snake_pos
        self.background = pygame.Surface((self.n_tile * self.tilesize, self.n_tile * self.tilesize))
        self.background.fill(self.BACKGROUND_COLOR)
        self.all_events = []

        self.head_color = head_color
        self.body_color = body_color

        self.inititalisation()

    def inititalisation(self):

        self.grid = [[' ' for _ in range(self.n_tile)] for _ in range(self.n_tile)]

        self.snake = Snake(grid=self, pos=self.snake_pos, tilesize=self.tilesize,
                           head_color=self.head_color, body_color=self.body_color)


    def spawn_apple(self):
        empty_squares = get_empty_space(self.grid)
        i, j = random.choice(empty_squares)

        self.grid[i][j] = 'A'


    def draw_background(self):
        self.screen.blit(self.background, self.pos)

    def update(self, all_events):
        self.draw_background()
        self.snake.update(all_events)
