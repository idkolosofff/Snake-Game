import pygame
import socket
from . import config
from .network import Network
import pickle
import threading

class Client:
    def __init__(self, ip, snake_color):
        self.network = Network(ip)
        self.player_id = self.network.get_player_id()
        self.game_state = None
        self.recv_lock = threading.Lock()

    def update_direction(self, new_direction):
        self.network.send_data(('update_direction', self.player_id, new_direction))

    def disconnect(self):
        self.network.send_data(('disconnecting', self.player_id))
        print('Connection lost')
        self.network.connected = False

    def request_game_state(self):
        try:
            self.game_state = self.network.get_game_state()
        except (socket.error, EOFError):
            self.game_state = {'end_reason': 'server_closed'}

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.disconnect()
                return False
            elif event.type == pygame.KEYDOWN:
                if not (self.player_id in self.game_state['snakes']):
                    return False
                snake_direction = self.game_state['snakes'][self.player_id]['direction']
                if event.key == pygame.K_UP and snake_direction != config.UP:
                    self.update_direction(config.DOWN)
                elif event.key == pygame.K_DOWN and snake_direction != config.DOWN:
                    self.update_direction(config.UP)
                elif event.key == pygame.K_LEFT and snake_direction != config.LEFT:
                    self.update_direction(config.RIGHT)
                elif event.key == pygame.K_RIGHT and snake_direction != config.RIGHT:
                    self.update_direction(config.LEFT)
                elif event.key == pygame.K_ESCAPE:
                    self.disconnect()
                    return False
        return True

    def recv_data(self):
        try:
            with self.recv_lock:
                received_magic = self.recvall(4)
                if received_magic != config.MAGIC_NUMBER:
                    raise ValueError("Invalid magic number received.")
                message_length = int.from_bytes(self.recvall(4), 'big')
                if message_length <= 0 or message_length > 10**6:
                    raise ValueError(f"Invalid message length: {message_length}")
                data = self.recvall(message_length)
                received_data = pickle.loads(data)
                #print(f"Received data: {received_data}")
                return received_data
        except (pickle.UnpicklingError, ValueError, EOFError, socket.error) as e:
            print(f"Error network receiving data: {e}")
            self.connected = False
            return {'action': 'game_over', 'reason': 'server_closed'}
