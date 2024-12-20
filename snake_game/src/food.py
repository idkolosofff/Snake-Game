import pygame
from .drawing import draw_food
from . import config

class Food:
    size = config.FOOD_SIZE

    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        draw_food(screen, self.position, self.size)
    def get_food_data(self):
        return {
            'position': self.position,
        }