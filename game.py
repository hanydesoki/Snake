import json
import pygame
from grid import Grid
from menu_layout import Menu
from menu_layout import SCORE_PATH, COLOR_PATH
from tools import display_text
from color_layout import ColorLayout

class Game:

    BACKGROUND_COLOR = (50, 50, 50)

    def __init__(self):
        pygame.init()

        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(self.BACKGROUND_COLOR)

        tilesize = 26
        n_tile = 20
        pos = (40, 40)
        snake_pos = (10, 10)

        self.grid = Grid(tilesize=tilesize, n_tile=n_tile, pos=pos, snake_pos=snake_pos)

        self.menu = Menu(self)

        self.menu.game.grid.snake.playing = False

        self.color_layout = ColorLayout(self.menu)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def run(self):
        while True:
            all_events = pygame.event.get()
            for event in all_events:
                if event.type == pygame.QUIT:
                    with open(SCORE_PATH, 'w') as f:
                        json.dump(self.menu.scores, f)

                    with open(COLOR_PATH, 'w') as f:
                        json.dump(self.menu.colors, f)
                    pygame.quit()
                    exit()

            self.draw_background()
            if self.grid.snake.playing:
                self.grid.update(all_events)
                display_text(self.screen, f'{self.menu.difficulty}', 100, 20, size=30)
                display_text(self.screen, f'High score: {self.menu.scores[self.menu.difficulty]}', 400, 20, size=30)
            else:
                if self.menu.choosing_color:
                    self.color_layout.update()
                else:
                    self.menu.update(all_events)

            pygame.display.update()
            self.clock.tick(60)