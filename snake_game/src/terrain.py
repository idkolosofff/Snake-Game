import pygame
from .drawing import draw_terrain
from . import config

class Terrain:
    def __init__(self, position, terrain_type = "add_points"):
        self.type = terrain_type
        self.position = position
        self.size = config.TERRAIN_SIZES.get(self.type, config.DEFAULT_TERRAIN_SIZE)

    def draw(self, screen):
        draw_terrain(screen, self.position, self.size, self.type)

    def get_terrain_data(self):
        return {
            'type' : self.type,
            'position': self.position,
        }