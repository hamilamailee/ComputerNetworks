from http import client
from mimetypes import init
import socket

game_server_count = 10
HOST = "127.0.0.1"
PORT = 8800


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.socket as s:
            s.connect((HOST, PORT))
            s.sendall(b'salam')
            data = s.recv(2048)
            print(f"Received {data!r}")


c1 = Client()
