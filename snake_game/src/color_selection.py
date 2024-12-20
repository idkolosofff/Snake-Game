import pygame
from .drawing import draw_color_selection
from . import config

class ColorSelection:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(None, config.TITLE_FONT)
        self.caption_font = pygame.font.Font(None, config.MENU_FONT)
        self.font = pygame.font.Font(None, config.MENU_FONT)
        self.running = True
        self.color_options = config.COLOR_OPTIONS

    def draw(self):
        draw_color_selection(self.screen, self.color_options, self.title_font, self.font)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return 'Quit', None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return 'escape', None
                for i, color in enumerate(self.color_options, 1):
                    if event.key == getattr(pygame, f"K_{i}") or event.key == getattr(pygame, f"K_KP{i}"):
                        return 'ColorSelected', color
        return None, None

    def run(self):
        while self.running:
            self.draw()
            action, color = self.handle_input()
            if action:
                return action, color
