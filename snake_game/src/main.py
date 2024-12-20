import os
import sys
import socket
import threading
import pygame
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.game import Game
from src.game_multiplayer import GameMultiplayer
from src.highscore import Highscore
from src.level_selection import LevelSelection
from src.color_selection import ColorSelection
from src.menu import Menu
from src.menu import MultiplayerMenu
from src.server import Server
from src.client import Client
from . import config


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    menu = Menu(screen)
    highscore = Highscore()
    snake_color = config.DEFAULT_SNAKE_COLOR

    while True:
        action = menu.run()

        if action == "Start":
            level_selection = LevelSelection(screen)
            level = level_selection.run()
            if level == 'escape':
                continue
            elif level:
                game = Game(screen, highscore, level, snake_color)
                game.run()
        elif action == "Multiplayer":
            multiplayer_menu = MultiplayerMenu(screen)
            multiplayer_action = multiplayer_menu.run()
            if multiplayer_action == 'Host':
                ip = input("Enter the server IP address: ")
                server = Server(ip) #for local network
                server_thread = threading.Thread(target=server.run)
                server_thread.start()
                time.sleep(0.5)

                client = Client(ip, snake_color) # Assuming server and client are on the same machine
                game_multiplayer = GameMultiplayer(screen, client, snake_color)
                game_multiplayer.run()
                
                server.shutdown()
                server_thread.join()
            elif multiplayer_action == 'Join':
                ip = input("Enter the server IP address: ")
                try:
                    client = Client(ip, snake_color)
                    game_multiplayer = GameMultiplayer(screen, client, snake_color)
                    game_multiplayer.run()
                except socket.gaierror:
                    print("Failed to connect to the server. Please check the IP address and try again.")
                    continue
            elif multiplayer_action == 'Back':
                continue
        elif action == 'Colors':
            color_selection = ColorSelection(screen)
            color_action, selected_color = color_selection.run()
            if color_action == 'escape':
                continue
            elif color_action == 'ColorSelected':
                snake_color = selected_color

        elif action == 'Records':
            highscore.show_personal_records(screen)

        elif action == 'Quit':
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json()['ip']
        return ip
    except:
        print("Error fetching public IP address. Please enter it manually.")
        return None
    