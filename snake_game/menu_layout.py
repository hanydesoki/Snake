import json
import os
import pygame
from .tools import Button, display_text
from . import __version__

SCORE_PATH = 'Saves/scores.json'
COLOR_PATH = 'Saves/snake_color.json'

if not os.path.exists('Saves'):
    os.mkdir('Saves')

difficulty_speed = {'Very Easy': 32,
                      'Easy': 16,
                      'Medium': 8,
                      'Hard': 4,
                      'Very Hard': 2}

class Menu:
    BACKGROUND_COLOR = (50, 50, 50)
    LOSE_BACKGROUND_COLOR = (255, 100, 100)

    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(self.BACKGROUND_COLOR)

        self.lose_background = pygame.Surface((self.screen_width, self.screen_height))
        self.lose_background.fill(self.LOSE_BACKGROUND_COLOR)
        self.lose_background.set_alpha(0)

        self.background.set_alpha(200)
        self.play_button = Button(self.screen, 250, 320, 'Play', size=50)
        self.boot_menu = True

        self.increase_button = Button(self.screen, 200, 500, ' + ', size=20)
        self.decrease_button = Button(self.screen, 200, 530, ' - ', size=25)

        self.choosing_color = False

        self.color_button = Button(self.screen, 450, 400, 'Colors', size=20)

        if os.path.exists(SCORE_PATH):
            with open(SCORE_PATH, 'r') as f:
                self.scores = json.load(f)

        else:
            self.scores = {'Very Easy': 0,
                      'Easy': 0,
                      'Medium': 0,
                      'Hard': 0,
                      'Very Hard': 0}

        if os.path.exists(COLOR_PATH):
            with open(COLOR_PATH, 'r') as f:
                self.colors = json.load(f)
        else:
            self.colors = {}

        self.difficulties = list(self.scores)

        self.difficulty_indice = 2

        self.last_difficulty = self.difficulties[self.difficulty_indice]

        self.last_score = 0

        self.frame = 0


    @property
    def difficulty(self):
        return self.difficulties[self.difficulty_indice]

    @property
    def can_interact(self):
        self.frame -= 1
        self.frame = max(0, self.frame)
        return self.frame == 0

    def draw_background(self):
        self.game.draw_background()
        self.game.grid.draw_background()
        if not self.boot_menu:
            self.game.grid.snake.draw()
        self.screen.blit(self.background, (0, 0))

    def draw(self):
        display_text(self.screen, 'SNAKE', 235, 50, size=60)

        if self.game.grid.snake.lose:
            self.last_score = self.game.grid.snake.score
            self.last_difficulty = self.difficulty
            self.frame = 60
            self.game.grid.snake.lose = False

        self.lose_background.set_alpha(2 * self.frame)

        self.screen.blit(self.lose_background, (0, 0))
        display_text(self.screen, __version__, 570, 585, size=15)


        if self.boot_menu:
            display_text(self.screen, f'High Score: {self.scores[self.difficulty]}', 195, 200, size=50)
        else:
            display_text(self.screen, f'High Score: {self.scores[self.difficulty]}', 195, 150, size=50)
            if self.game.grid.snake.score > self.scores[self.difficulty]:
                self.scores[self.difficulty] = self.game.grid.snake.score

            if self.difficulty == self.last_difficulty:
                display_text(self.screen, f'Score: {self.last_score}', 230, 230, size=50)

        for i in range(4):
            if i == 0:
                color = self.game.grid.head_color
                if color is None:
                    color = self.game.grid.snake.SNAKE_HEAD_COLOR
            else:
                color = self.game.grid.body_color
                if color is None:
                    color = self.game.grid.snake.SNAKE_COLOR


            surf = pygame.Surface((15, 15))
            surf.fill(color)
            self.screen.blit(surf, (475, 430 + i*15))

        display_text(self.screen, self.difficulty, 230, 515, size=30)

    def check_button(self, all_events):
        if self.play_button.check_released() or pygame.key.get_pressed()[pygame.K_SPACE]:
            self.game.grid.inititalisation()
            self.game.grid.snake.playing = True
            self.boot_menu = False

        if self.color_button.check_released():
            self.game.menu.choosing_color = True

        if self.can_interact:

            key_pressed = None

            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    key_pressed = event.key

            if self.increase_button.check_released() or key_pressed in [pygame.K_UP, pygame.K_z]:
                if self.difficulty_indice < len(self.difficulties) - 1:
                    self.game.grid.snake.size = self.game.grid.snake.init_size
                    self.difficulty_indice += 1

            if self.decrease_button.check_released() or key_pressed in [pygame.K_DOWN, pygame.K_s]:
                if self.difficulty_indice > 0:
                    self.game.grid.snake.size = self.game.grid.snake.init_size
                    self.difficulty_indice -= 1

        self.game.grid.snake.frame_to_update = difficulty_speed[self.difficulty]

    def update(self, all_events):
        self.draw_background()
        self.draw()
        self.play_button.update()
        self.increase_button.update()
        self.decrease_button.update()
        self.color_button.update()
        self.check_button(all_events)