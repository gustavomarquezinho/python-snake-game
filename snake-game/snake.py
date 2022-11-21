from random import randint
import pygame
import pygame.locals


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

        self.display = pygame.display.set_mode((self.window_width, self.window_height), )
        self.display.fill((19, 41, 61))

        pygame.display.set_caption('Snake Game')

        self.clock = pygame.time.Clock()
        self.move_direction = None

        self.create_snake()
        self.create_food(new_pos=True)

    def run_game(self, difficulty: int) -> None:
        self.difficulty = difficulty
        self.fps = 8 + difficulty + 1

        while True:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or len(self.snake) >= self.max_size:
                    self.game_over()

                elif event.type == pygame.locals.KEYDOWN:
                    can_change_direction = True

                    if self.move_direction == pygame.locals.K_LEFT or self.move_direction == pygame.locals.K_RIGHT:
                        if event.key == pygame.locals.K_LEFT or event.key == pygame.locals.K_RIGHT:
                            can_change_direction = False

                    elif self.move_direction == pygame.locals.K_UP or self.move_direction == pygame.locals.K_DOWN:
                        if event.key == pygame.locals.K_UP or event.key == pygame.locals.K_DOWN:
                            can_change_direction = False

                    if can_change_direction:
                        self.move_direction = event.key

            if self.move_direction is not None:
                if self.move_direction == pygame.locals.K_LEFT:
                    self.snake_x -= self.snake_size
                elif self.move_direction == pygame.locals.K_RIGHT:
                    self.snake_x += self.snake_size
                elif self.move_direction == pygame.locals.K_UP:
                    self.snake_y -= self.snake_size
                elif self.move_direction == pygame.locals.K_DOWN:
                    self.snake_y += self.snake_size

                if self.is_snake_collided():
                    self.game_over()

                if self.snake_x < 0:
                    self.snake_x = self.window_width
                elif self.snake_x > self.window_width:
                    self.snake_x = 0
                elif self.snake_y < 0:
                    self.snake_y = self.window_height
                elif self.snake_y > self.window_height:
                    self.snake_y = 0

                self.display.fill((19, 41, 61))

                if (self.snake_x, self.snake_y) == (self.food_x, self.food_y):
                    pygame.display.set_caption(f'Snake Game ({len(self.snake)} points)')

                    self.extend_snake()
                    self.create_food(new_pos=True)
                else:
                    self.create_food(new_pos=False)

                self.move_snake()

            pygame.display.update()

    def get_nearest_divisible(self, num: int, divisor: int) -> int:
        for i in range(1, divisor + 1):
            if (num + i) % divisor == 0:
                return num + i
        return num

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

        if self.snake_x % self.snake_size != 0:
            self.snake_x = self.get_nearest_divisible(self.snake_x, self.snake_size)

        if self.snake_y % self.snake_size != 0:
            self.snake_y = self.get_nearest_divisible(self.snake_y, self.snake_size)

        pygame.draw.rect(surface=self.display, color=(255, 232, 115), rect=(self.snake_x, self.snake_y, self.snake_size, self.snake_size))
        self.snake.append((self.snake_x, self.snake_y, self.snake_size, self.snake_size))

    def create_food(self, new_pos: bool) -> bool:
        if new_pos:
            self.food_x = randint(self.food_size, self.window_width - (self.food_size * 2))
            self.food_y = randint(self.food_size, self.window_height - (self.food_size * 2))

            if self.food_x % self.snake_size != 0:
                self.food_x = self.get_nearest_divisible(self.food_x, self.snake_size)

            if self.food_y % self.snake_size != 0:
                self.food_y = self.get_nearest_divisible(self.food_y, self.snake_size)

            for info in self.snake:
                if info[:2] == (self.food_x, self.food_y):
                    return self.create_food(new_pos)

        pygame.draw.rect(surface=self.display, color=(220, 20, 60), rect=(self.food_x, self.food_y, self.food_size, self.food_size))
        return True

    def move_snake(self) -> None:
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = self.snake[i - 1]
            pygame.draw.rect(surface=self.display, color=(255, 232, 115), rect=self.snake[i])

        self.snake[0] = (self.snake_x, self.snake_y, self.snake_size, self.snake_size)
        pygame.draw.rect(surface=self.display, color=(255, 232, 115), rect=self.snake[0])

    def extend_snake(self) -> None:
        snake_end_x = self.snake[len(self.snake) - 1][0]
        snake_end_y = self.snake[len(self.snake) - 1][1]

        if self.move_direction == pygame.locals.K_LEFT:
            snake_end_x += self.snake_size
        elif self.move_direction == pygame.locals.K_RIGHT:
            snake_end_x -= self.snake_size
        elif self.move_direction == pygame.locals.K_UP:
            snake_end_y += self.snake_size
        elif self.move_direction == pygame.locals.K_DOWN:
            snake_end_y += self.snake_size

        self.snake.append((snake_end_x, snake_end_y, self.snake_size, self.snake_size))

    def game_over(self):
        pygame.quit()
        quit()
