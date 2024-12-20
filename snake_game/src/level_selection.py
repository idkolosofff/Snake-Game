import pygame
from .drawing import draw_level_selection
from . import config

class LevelSelection:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.levels = [("1", "Basic"), ("2", "Easy"), ("3", "Good"), ("4", "Better"), ("5", "Medium")]
        self.font = pygame.font.Font(None, config.LEVELS_FONT)

    def draw(self):
        draw_level_selection(self.screen, self.levels, self.font)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    return 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    return 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    return 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    return 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    return 5
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return 'escape'

    def run(self):
        while self.running:
            self.draw()
            difficulty = self.handle_input()
            if difficulty:
                return difficulty
