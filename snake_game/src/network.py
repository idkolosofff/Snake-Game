import socket
import pickle
import logging
from .config import BYTES_RECV, MAGIC_NUMBER
import threading


class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5432  # Choose an appropriate port number
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        self.connected = True
        self.send_lock = threading.Lock()
        self.recv_lock = threading.Lock()

    def get_player_id(self):
        player_id = self.recv_data()
        return int(player_id)

    def get_game_state(self):
        try:
            self.send_data(('request_game_state',))
            return self.recv_data()
        except socket.error as e:
            print('Connection lost')
            self.connected = False
            return {'end_reason': 'server_closed'}


    def send_data(self, data):
        if not self.connected:
            return
        try:
            with self.send_lock:
                message = pickle.dumps(data)
                message_length = len(message)
                #logging.debug(f"Sending data: Length={message_length}, Data={data}")
                self.client.sendall(MAGIC_NUMBER)
                self.client.sendall(message_length.to_bytes(4, 'big'))
                self.client.sendall(message)
        except socket.error as e:
            print(f"Socket error during send: {e}")
            self.connected = False
        except pickle.PickleError as e:
            print(f"Pickle error during send: {e}")
            self.connected = False

    def recvall(self, length):
        data = b''
        while len(data) < length:
            more = self.client.recv(length - len(data))
            if not more:
                raise EOFError('Socket closed before receiving all data')
            data += more
        return data

    def recv_data(self):
        try:
            with self.recv_lock:
                received_magic = self.recvall(4)
                if received_magic != MAGIC_NUMBER:
                    raise ValueError("Invalid magic number received.")
                message_length = int.from_bytes(self.recvall(4), 'big')
                if message_length <= 0 or message_length > 10**6:
                    raise ValueError(f"Invalid message length: {message_length}")
                data = self.recvall(message_length)
                received_data = pickle.loads(data)
                #print(f"Received data: {received_data}")
                return received_data
        except (pickle.UnpicklingError, ValueError, EOFError, socket.error) as e:
            if self.connected:
                print(f"Error network receiving data: {e}")
            self.connected = False
            return {'action': 'game_over', 'reason': 'server_closed'}

