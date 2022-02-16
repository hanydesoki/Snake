import pygame
from .tools import SlideBar, display_text, Button
import random

color_bar = {'R': (255, 0, 0),
             'G': (0, 255, 0),
             'B': (0, 0, 255)}

class ColorLayout:
    BACKGROUND_COLOR = (50, 50, 50)

    def __init__(self, menu):
        self.menu = menu
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(self.BACKGROUND_COLOR)

        self.background_tile = 40

        self.background_snake = pygame.Surface((self.background_tile, self.background_tile))
        self.background_snake.fill(self.menu.game.grid.BACKGROUND_COLOR)

        self.snake_tilesize = 50

        self.head_slidebars = {}

        for i, color in enumerate(['R', 'G', 'B']):
            self.head_slidebars[color] = SlideBar(self.screen, color + ' ', 230, 30, 60 + i * 30, range(256), fill_bar_color=color_bar[color])

        self.body_slidebars = {}

        for i, color in enumerate(['R', 'G', 'B']):
            self.body_slidebars[color] = SlideBar(self.screen, color + ' ', 230, 30, 200 + i * 30, range(256), fill_bar_color=color_bar[color])

        self.head_slidebars['G'].set_current_value(255)
        self.body_slidebars['G'].set_current_value(200)

        self.set_color_button = Button(self.screen, 400, 300, 'Set color', size=20)
        self.random_color_button = Button(self.screen, 100, 300, 'Random', size=20)
        self.save_button = Button(self.screen, 40, 360, 'Save', size=15)

        self.update_snake_preview()

        self.display_message = False

        self.time_to_delete = 30
        self.frame = 0

    def update_snake_preview(self):

        self.snake_previews = []

        for i, color in self.menu.colors.items():
            if int(i) > 13: y = 480
            else: y = 410
            head_color = tuple(color['head_color'])
            body_color = tuple(color['body_color'])
            self.snake_previews.append(SnakePreview(head_color, body_color, 26 + int(i)%14 * 40, y))


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        display_text(self.screen, 'Snake head color:', 63, 25, size=20)
        display_text(self.screen, 'Snake body color:', 63, 165, size=20)
        self.draw_snake()

    def set_random_color(self):
        for sb in self.head_slidebars.values():
            sb.set_current_value(random.randint(0, 255))

        for sb in self.body_slidebars.values():
            sb.set_current_value(random.randint(0, 255))

    def get_head_color(self):
        return tuple([sb.get_current_value() for sb in self.head_slidebars.values()])

    def get_body_color(self):
        return tuple([sb.get_current_value() for sb in self.body_slidebars.values()])

    def interact(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.menu.choosing_color = False

    def draw_favorite_snakes(self):
        for i in range(14):
            for j in range(4):
                self.screen.blit(self.background_snake, (20 + i*self.background_tile, 400 + j * self.background_tile))

        for i, sp in enumerate(self.snake_previews):
            sp.update()
            if sp.clicked:
                head_color = sp.head_color
                body_color = sp.body_color

                for sb, hc in zip(self.head_slidebars.values(), head_color):
                    sb.set_current_value(hc)

                for sb, bc in zip(self.body_slidebars.values(), body_color):
                    sb.set_current_value(bc)

            if sp.right_clicked and self.frame == 0:
                self.delete_snake_from_favorite(i)
                self.frame = self.time_to_delete



        if self.display_message:
            display_text(self.screen,
                         'Cannot add a new snake to favorite, please delete a snake with a right click',
                         20, 580, 15)

    def draw_snake(self):

        for i in range(4):
            for j in range(6):
                self.screen.blit(self.background_snake, (360 + i*self.background_tile, 30 + j * self.background_tile))


        for i in range(4):
            if i == 0: color = self.get_head_color()
            else: color = self.get_body_color()

            surf = pygame.Surface((self.snake_tilesize, self.snake_tilesize))
            surf.fill(color)

            self.screen.blit(surf, (400, 40 + i * self.snake_tilesize))

        self.screen.blit(surf, (400 + self.snake_tilesize, 40 + i * self.snake_tilesize))


    def check_button(self):
        if self.set_color_button.check_released():
            self.menu.game.grid.body_color = self.get_body_color()
            self.menu.game.grid.head_color = self.get_head_color()
            self.menu.choosing_color = False

        if self.random_color_button.check_released():
            self.set_random_color()

        if self.save_button.check_released():
            self.add_current_color_to_favorite()

    def add_current_color_to_favorite(self):
        if len(self.menu.colors) < 28:
            self.display_message = False
            new_dict = {}
            i = -1
            for i, colors in enumerate(self.menu.colors.values()):
                new_dict[str(i)] = colors

            new_dict[str(i + 1)] = {}

            new_dict[str(i + 1)]['head_color'] = self.get_head_color()
            new_dict[str(i + 1)]['body_color'] = self.get_body_color()

            self.menu.colors = new_dict
            self.update_snake_preview()
        else:
            self.display_message = True

    def delete_snake_from_favorite(self, slot):
        new_dict = self.menu.colors.copy()

        del new_dict[str(slot)]

        new_dict2 = {}

        for i, colors in enumerate(new_dict.values()):
            new_dict2[str(i)] = colors

        self.menu.colors = new_dict2
        self.update_snake_preview()

    def update_delete_frame(self):
        self.frame -= 1

        if self.frame < 0:
            self.frame = 0


    def update(self):
        self.draw()
        self.draw_favorite_snakes()
        self.interact()
        for sb in self.head_slidebars.values():
            sb.update()
        for sb in self.body_slidebars.values():
            sb.update()

        self.set_color_button.update()
        self.random_color_button.update()
        self.save_button.update()
        self.check_button()
        self.update_delete_frame()

class SnakePreview:

    def __init__(self, head_color, body_color, x, y):

        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.head_color = head_color
        self.body_color = body_color
        self.x = x
        self.y = y

        self.surf = pygame.Surface((30, 60))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.fill((200, 200, 200))

        self.clicked = False
        self.right_clicked = False

        self.tilesize = 13

        self.head_surf = pygame.Surface((self.tilesize, self.tilesize))
        self.head_surf.fill(self.head_color)

        self.body_surf = pygame.Surface((self.tilesize, self.tilesize))
        self.body_surf.fill(self.body_color)

    def draw(self):
        for i in range(4):
            if i == 0: surf = self.head_surf
            else: surf = self.body_surf
            self.screen.blit(surf, (self.x + 8, self.y + 4 + i * self.tilesize))

    def interact(self):

        mouse_pos = pygame.mouse.get_pos()

        pressed = pygame.mouse.get_pressed()[0]
        right_pressed = pygame.mouse.get_pressed()[2]

        self.clicked = False
        self.right_clicked = False

        if pressed:
            if self.rect.collidepoint(*mouse_pos):
                self.clicked = True

        if right_pressed:
            if self.rect.collidepoint(*mouse_pos):
                self.right_clicked = True

    def draw_hover_rect(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(*mouse_pos):
            self.screen.blit(self.surf, self.rect)


    def update(self):
        self.interact()
        self.draw_hover_rect()
        self.draw()