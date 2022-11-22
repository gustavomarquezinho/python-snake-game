from random import randint
import pygame
import pygame.locals


KEYS_UP = (
    pygame.locals.K_UP,
    pygame.locals.K_w
)

KEYS_LEFT = (
    pygame.locals.K_LEFT,
    pygame.locals.K_a
)

KEYS_DOWN = (
    pygame.locals.K_DOWN,
    pygame.locals.K_s
)

KEYS_RIGHT = (
    pygame.locals.K_RIGHT,
    pygame.locals.K_d
)


class Snake():
    def __init__(self) -> None:
        self.window_width = 600
        self.window_height = 400

        self.snake_size = 20
        self.food_size = 20

        self.max_size = round((self.window_width / self.snake_size) * (self.window_height / self.snake_size))

        self.snake = [
        ]

        pygame.init()

        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

    def start_game(self, difficulty: int) -> None:
        pygame.display.set_caption('Snake Game')
        self.display.fill((19, 41, 61))

        self.move_direction = None

        if len(self.snake):
            self.snake.clear()

        self.create_lines()
        self.create_snake()
        self.create_food(new_pos=True)

        self.difficulty = difficulty
        self.fps = 8 + difficulty + 1

        while True:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    quit()

                elif len(self.snake) >= self.max_size:
                    self.restart_game()

                elif event.type == pygame.locals.KEYDOWN:
                    can_change_direction = True

                    if event.key not in (*KEYS_UP, *KEYS_LEFT, *KEYS_DOWN, *KEYS_RIGHT):
                        can_change_direction = False

                    elif self.move_direction in KEYS_UP or self.move_direction in KEYS_DOWN:
                        if event.key in KEYS_UP or event.key in KEYS_DOWN:
                            can_change_direction = False

                    elif self.move_direction in KEYS_LEFT or self.move_direction in KEYS_RIGHT:
                        if event.key in KEYS_LEFT or event.key in KEYS_RIGHT:
                            can_change_direction = False

                    if can_change_direction:
                        self.move_direction = event.key

            if self.move_direction is not None:
                if self.move_direction in KEYS_UP:
                    self.snake_y -= self.snake_size
                elif self.move_direction in KEYS_LEFT:
                    self.snake_x -= self.snake_size
                elif self.move_direction in KEYS_DOWN:
                    self.snake_y += self.snake_size
                elif self.move_direction in KEYS_RIGHT:
                    self.snake_x += self.snake_size

                if self.is_snake_collided():
                    self.restart_game()

                if self.snake_x < 0:
                    self.snake_x = self.window_width
                elif self.snake_x > self.window_width:
                    self.snake_x = 0
                elif self.snake_y < 0:
                    self.snake_y = self.window_height
                elif self.snake_y > self.window_height:
                    self.snake_y = 0

                self.display.fill((19, 41, 61))
                self.create_lines()

                if (self.snake_x, self.snake_y) == (self.food_x, self.food_y):
                    pygame.display.set_caption(f'Snake Game ({len(self.snake)} points)')

                    self.extend_snake()
                    self.create_food(new_pos=True)
                else:
                    self.create_food(new_pos=False)

                self.move_snake()

            pygame.display.update()

    def is_snake_collided(self) -> bool:
        if self.difficulty >= 1:
            if self.snake_x < 0 or self.snake_x > self.window_width:
                return True
            elif self.snake_y < 0 or self.snake_y > self.window_height:
                return True

        for info in self.snake[1:]:
            if self.snake[0][:2] == info[:2]:
                return True
        return False

    def create_snake(self) -> None:
        self.snake_x = randint(self.snake_size, self.window_width - (self.snake_size * 2))
        self.snake_y = randint(self.snake_size, self.window_height - (self.snake_size * 2))

        self.snake_x = (self.snake_x // self.snake_size) * self.snake_size
        self.snake_y = (self.snake_y // self.snake_size) * self.snake_size

        pygame.draw.rect(surface=self.display, color=(255, 232, 115), rect=(self.snake_x, self.snake_y, self.snake_size, self.snake_size))
        self.snake.append((self.snake_x, self.snake_y, self.snake_size, self.snake_size))

    def create_food(self, new_pos: bool) -> bool:
        if new_pos:
            self.food_x = randint(self.food_size, self.window_width - (self.food_size * 2))
            self.food_y = randint(self.food_size, self.window_height - (self.food_size * 2))

            self.food_x = (self.food_x // self.food_size) * self.food_size
            self.food_y = (self.food_y // self.food_size) * self.food_size

            for info in self.snake:
                if info[:2] == (self.food_x, self.food_y):
                    return self.create_food(new_pos)

        pygame.draw.rect(surface=self.display, color=(220, 20, 60), rect=(self.food_x, self.food_y, self.food_size, self.food_size))
        return True

    def create_lines(self) -> None:
        for x in range(0, self.window_width, self.food_size):
            pygame.draw.line(self.display, (28, 50, 70), (x, 0), (x, self.window_height))

        for y in range(0, self.window_height, self.food_size):
            pygame.draw.line(self.display, (28, 50, 70), (0, y), (self.window_width, y))

    def move_snake(self) -> None:
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = self.snake[i - 1]
            pygame.draw.rect(surface=self.display, color=(255, 232, 115), rect=self.snake[i])

        self.snake[0] = (self.snake_x, self.snake_y, self.snake_size, self.snake_size)
        pygame.draw.rect(surface=self.display, color=(255, 232, 115), rect=self.snake[0])

    def extend_snake(self) -> None:
        self.snake.append((0, 0, self.snake_size, self.snake_size))

    def restart_game(self):
        self.start_game(self.difficulty)
