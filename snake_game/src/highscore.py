import pygame
import os
import json
from .drawing import draw_highscore
from . import config

class Highscore:
    def __init__(self, filename='snake_game/records/highscores.json'):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)

    def add_score(self, score):
        scores = self.get_scores()
        scores.append(score)
        scores.sort(reverse=True)
        scores = scores[:config.TOP_SELECTION]  # Keep only the top 10 scores

        with open(self.filename, 'w') as file:
            json.dump(scores, file)

    def get_scores(self):
        with open(self.filename, 'r') as file:
            scores = json.load(file)
        return scores

    def show_personal_records(self, screen):
        scores = self.get_scores()
        font = pygame.font.Font(None, config.SCORE_FONT)
        running = True

        while running:
            draw_highscore(screen, scores, font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_q):
                        running = False


