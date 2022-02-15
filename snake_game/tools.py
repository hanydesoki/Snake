import pygame

def display_text(screen, text, x, y, size=10, color=(255, 255, 255)):
    text_base_font = pygame.font.Font(None, size)
    text_surface = text_base_font.render(str(text), True, color)

    screen.blit(text_surface, (x, y))

class Button:

    BLUE = (0, 0, 200)
    DARK_BLUE = (0, 0, 100)
    RED = (100, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, screen, x, y, text, size=20):
        self.screen = screen

        self.x = x
        self.y = y

        base_font = pygame.font.Font(None, int(size))
        self.text_surface = base_font.render(str(text), True, self.WHITE)
        self.width = self.text_surface.get_width() * 1.4
        self.height = self.text_surface.get_height() * 1.4
        self.bg_surface = pygame.Surface((self.width, self.height))
        self.bg_surface2 = pygame.Surface((self.width, self.height + 3))
        self.rect = self.bg_surface.get_rect(topleft=(self.x, self.y))

        self.clicked = False

        self.history = []

    def draw(self):

        if self.clicked:
            self.bg_surface.fill(self.DARK_BLUE)
        else:
            self.bg_surface.fill(self.BLUE)
            self.bg_surface2.fill(self.RED)

        if not self.clicked:
            self.screen.blit(self.bg_surface2, self.rect)

        self.screen.blit(self.bg_surface, self.rect)
        self.screen.blit(self.text_surface, (self.rect[0] + self.width/2 - self.text_surface.get_width()/2,
                                             self.rect[1] + self.height/2 - self.text_surface.get_height()/2))


    def interact(self):

        mouse_pos = pygame.mouse.get_pos()

        pressed = pygame.mouse.get_pressed()[0]

        self.rect.x = self.x
        self.rect.y = self.y

        self.clicked = False

        if pressed:
            if self.rect.collidepoint(*mouse_pos):
                self.clicked = True
                self.rect.y += 3


    def check_released(self, must_be_in=True):
        if must_be_in:
            return self.history == [True, False] and self.rect.collidepoint(*pygame.mouse.get_pos())
        else:
            return self.history == [True, False]


    def update(self):
        self.interact()
        self.draw()

        self.history.append(self.clicked)

        if len(self.history) >= 2:
            self.history = self.history[-2:]

class SlideBar:

    instances = []

    def __init__(self, screen, name, width, x, y, range_values, fill_bar_color=(255, 255, 0)):
        self.screen = screen
        self.name = name
        self.width = width
        self.x = x
        self.y = y
        self.range_values = list(range_values)
        self.fill_bar_color = fill_bar_color
        self.current_value = range_values[0]

        self.curs_surf = pygame.Surface((10, 10))
        self.bar_surf = pygame.Surface((self.width, 2))
        self.curs_rect = self.curs_surf.get_rect(center=(self.x, self.y))
        self.bar_rect = self.bar_surf.get_rect(midleft=(self.x, self.y))

        self.moving = False

        self.curs_surf.fill((230, 230, 230))
        self.bar_surf.fill((10, 10, 10))

        self.instances.append(self)

        self.lock_value = None


    def interact(self):
        mouse_pos = pygame.mouse.get_pos()

        pressed = pygame.mouse.get_pressed()[0]

        if pressed:
            if self.curs_rect.collidepoint(*mouse_pos) and self.get_sum_moving() == 0:
                self.moving = True

            if self.moving:
                self.curs_rect.centerx = mouse_pos[0]

                if self.curs_rect.centerx < self.x:
                    self.curs_rect.centerx = self.x

                if self.curs_rect.centerx > self.x + self.width:
                    self.curs_rect.centerx = self.x + self.width

        else:
            self.moving = False

        ratio = (self.curs_rect.centerx - self.x)/self.width
        indice = round(ratio*(len(self.range_values)-1))
        self.current_value = self.range_values[indice]

        if self.lock_value is not None:
            if self.current_value > self.lock_value:
                self.current_value = self.lock_value
                self.curs_rect.centerx = self.x + self.lock_value



    def draw(self):
        ratio = (self.curs_rect.centerx - self.x) / self.width

        fill_surf = pygame.Surface((int(self.width * ratio), 2))
        fill_surf.fill(self.fill_bar_color)

        self.screen.blit(self.bar_surf, self.bar_rect)
        self.screen.blit(fill_surf, (self.x, self.y - 1))
        self.screen.blit(self.curs_surf, self.curs_rect)

        text_base_font = pygame.font.Font(None, 15)
        text_surface = text_base_font.render(self.name, True, (255, 255, 255))

        value_base_font = pygame.font.Font(None, 20)
        value_surface = value_base_font.render(str(self.current_value), True, (255, 255, 255))

        if self.moving:
            self.curs_surf.fill((170, 170, 170))
        else:
            self.curs_surf.fill((230, 230, 230))

        self.screen.blit(text_surface, (self.x - len(self.name) * 11, self.bar_rect.y - 5))
        self.screen.blit(value_surface, (self.x + self.width + 10, self.bar_rect.y - 5))

    def get_current_value(self):
        return self.current_value

    def set_lock(self, value):
        self.lock_value = value

    def set_current_value(self, value):
        ratio = value / (len(self.range_values) - 1)
        self.curs_rect.centerx = self.x + round(self.width * ratio)
        self.current_value = value

    def update(self):
        self.interact()
        self.draw()

    @classmethod
    def get_sum_moving(cls):
        return sum([sb.moving for sb in cls.instances])

    def __repr__(self):
        return f"{self.__class__.__name__}(screen={self.screen},\
    name={self.name}, width={self.width}, x={self.x}, y={self.y}, range_values={self.range_values})"