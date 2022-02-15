import pygame
from .utils import check_similar_element, check_boundaries, check_apple_in_grid
from .tools import display_text

class Snake:

    SNAKE_COLOR = (0, 200, 0)
    SNAKE_HEAD_COLOR = (0, 255, 0)

    APPLE_COLOR = (255, 0, 0)
    PAUSE_BACKGROUND_COLOR = (50, 50, 50)

    def __init__(self, grid, pos, tilesize, init_size=4, head_color=None, body_color=None):
        self.grid = grid
        self.size = init_size
        self.init_size = init_size
        self.tilesize = tilesize
        self.pos = pos
        self.head_color = head_color
        self.body_color = body_color

        if self.head_color is None: self.head_color = self.SNAKE_HEAD_COLOR
        if self.body_color is None: self.body_color = self.SNAKE_COLOR

        self.squares = [[self.pos[0], self.pos[1] + i * 1] for i in range(init_size)]
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.snake_tile = pygame.Surface((tilesize, tilesize))
        self.snake_tile.fill(self.body_color)
        self.snake_head_tile = pygame.Surface((tilesize, tilesize))
        self.snake_head_tile.fill(self.head_color)

        self.pause_background = pygame.Surface((self.screen_width, self.screen_height))
        self.pause_background.fill(self.PAUSE_BACKGROUND_COLOR)
        self.pause_background.set_alpha(150)

        self.apple_tile = pygame.Surface((tilesize, tilesize))
        self.apple_tile.fill(self.APPLE_COLOR)

        self.direction = 'neutral'

        self.frames = 0
        self.frame_to_update = 10

        self.n_tiles = len(self.grid.grid)
        self.grid.spawn_apple()

        self.playing = True

        self.paused = False

        self.lose = False

    def update_grid(self):
        for i in range(self.n_tiles):
            for j in range(self.n_tiles):
                if [i, j] in self.squares:
                    if self.squares[0] == [i, j]:
                        self.grid.grid[i][j] = 'H'
                    else:
                        self.grid.grid[i][j] = 'X'
                elif self.grid.grid[i][j] == 'A':
                    pass
                else:
                    self.grid.grid[i][j] = ' '

    def update_squares(self):
        old_squares = self.squares.copy()

        if self.direction != 'neutral':
            if self.direction == 'up':
                new_square = [old_squares[0][0], old_squares[0][1] - 1]
            elif self.direction == 'down':
                new_square = [old_squares[0][0], old_squares[0][1] + 1]
            elif self.direction == 'left':
                new_square = [old_squares[0][0] - 1, old_squares[0][1]]
            elif self.direction == 'right':
                new_square = [old_squares[0][0] + 1, old_squares[0][1]]


            self.squares = [new_square] + old_squares[:-1]


        self.check_loses()

        self.check_eat()


    def check_loses(self):
        if check_similar_element(self.squares) or check_boundaries(self.squares, self.n_tiles):
            self.playing = False
            self.lose = True


    def check_eat(self):
        if not check_apple_in_grid(self.grid.grid):
            self.squares.append(self.squares[-1])
            self.grid.spawn_apple()
            self.size += 1



    def draw(self):
        for i, row in enumerate(self.grid.grid):
            for j, col in enumerate(row):
                if col == 'X':
                    self.screen.blit(self.snake_tile,
                                     (self.grid.pos[0] + i*self.tilesize,
                                      self.grid.pos[0] + j*self.tilesize))
                if col == 'H' and self.direction != 'neutral':
                    self.screen.blit(self.snake_head_tile,
                                     (self.grid.pos[0] + i*self.tilesize,
                                      self.grid.pos[0] + j*self.tilesize))
                elif col == 'H' and self.direction == 'neutral':
                    self.screen.blit(self.snake_tile,
                                     (self.grid.pos[0] + i * self.tilesize,
                                      self.grid.pos[0] + j * self.tilesize))
                if col == 'A':
                    self.screen.blit(self.apple_tile,
                                     (self.grid.pos[0] + i * self.tilesize,
                                      self.grid.pos[0] + j * self.tilesize))

        if self.paused:
            self.screen.blit(self.pause_background, (0, 0))
            display_text(self.screen, 'Paused', 20, 570, size=30)

    def draw_score(self):
        display_text(self.screen, f'SCORE: {self.score}', 250, 20, size=30)


    @property
    def score(self):
        return self.size - self.init_size


    def input(self):
        keys = pygame.key.get_pressed()

        if self.direction == 'neutral':
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.squares.reverse()
                self.direction = 'down'

        if (keys[pygame.K_UP] or keys[pygame.K_z]) and not self.direction == 'down':
            self.direction = 'up'
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.direction == 'up':
            self.direction = 'down'
        elif (keys[pygame.K_LEFT] or keys[pygame.K_q]) and not self.direction == 'right':
            self.direction = 'left'
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.direction == 'left':
            self.direction = 'right'

        #if keys[pygame.K_SPACE]:
        #    self.update_squares()

    def metronome(self):
        self.frames += 1
        if self.frames % self.frame_to_update == 0:
            self.update_squares()

    def check_pause(self, all_events):
        for event in all_events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_SPACE]:
                    self.paused = not self.paused


    def update(self, all_events):
        self.check_pause(all_events)
        if not self.paused:
            self.input()
            self.update_grid()
            self.metronome()
        self.draw()
        self.draw_score()
        #print(self.direction)


