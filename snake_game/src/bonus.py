import pygame
from .drawing import draw_bonus
from . import config

class Bonus:
    def __init__(self, position, bonus_type = "add_points"):
        self.type = bonus_type
        self.position = position
        self.size = config.BONUS_SIZES.get(self.type, config.DEFAULT_BONUS_SIZE)

    def draw(self, screen):
        draw_bonus(screen, self.position, self.size, self.type)

    def get_bonus_data(self):
        return {
            'type' : self.type,
            'position': self.position,
        }