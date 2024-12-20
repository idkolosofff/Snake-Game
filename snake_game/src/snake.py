import pygame
import random
from .drawing import draw_snake
from . import config

class Snake:
    def __init__(self, color = config.GREEN, start_pos = config.START_POS, block_size = config.SNAKE_SIZE, start_speed = config.START_SPEED):
        self.color = color
        self.block_size = block_size
        self.body = [start_pos]
        self.direction = config.LEFT
        self.speed = start_speed
        self.points = 0
        self.lost = False
        self.growth = 0             #How many tail blocks to grow

    def change_direction(self, new_direction):
        if self.direction[0] * new_direction[0] + self.direction[1] * new_direction[1] == 0:
            self.direction = new_direction

    def update(self):
        if self.direction == (0, 0):
            return

        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * self.speed / config.HEAD_SPEED_PARAMETER, head_y + self.direction[1] * self.speed / config.HEAD_SPEED_PARAMETER)
        self.body.insert(0, new_head)
        self.speed += config.PASSIVE_SPEED_INCREMENT
        if self.growth > 0:
            self.growth -= 1
        else:
            self.body.pop()

    def grow(self, growth=1):
        self.growth += growth

    def speed_up(self, speed_rate = config.DEFAULT_SPEED_FACTOR):
        # Increase the snake's speed by a factor of choice
        self.speed *= speed_rate

    def slow_down(self, slow_rate = config.DEFAULT_SLOW_FACTOR):
        # Decrease the snake's speed by a factor of choice
        self.speed *= slow_rate

    def trip(self):
        self.color = config.COLOR_OPTIONS[random.randint(0, 6)]

    def draw(self, screen):
        draw_snake(screen, self.body, self.block_size, self.color)

    def reset(self, start_pos = config.START_POS):
        self.body = [start_pos]
        self.direction = config.LEFT
        self.growth = 0

    def get_snake_data(self):
        return {
            'color': self.color,
            'body': self.body,
            'direction': self.direction,
            'speed': self.speed,
            'points': self.points,
            'lost': self.lost,
        }
    
    @classmethod
    def from_data(cls, data):
        snake = cls(color=data['color'], block_size=config.SNAKE_SIZE, start_speed=data['speed'])
        snake.body = data['body']
        snake.direction = data['direction']
        snake.points = data['points']
        snake.lost = data['lost']
        return snake

