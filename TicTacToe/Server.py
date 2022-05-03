from http import client
from mimetypes import init
import socket

game_server_count = 10
HOST = "127.0.0.1"
PORT = 8800


class GameServer:
    def __init__(self) -> None:
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_socket.bind((HOST, PORT))
        self.game_listen()

    def game_listen(self):
        with self.game_socket as s:
            s.listen()
            conneted, address = s.accept()
            print("Game server connected to address", address)
            while True:
                data = conneted.recv(1024)
                if not data:
                    print("no data")
                    break
                print(data)
                conneted.sendall(data)


class WebServer:
    def __init__(self) -> None:
        pass

    def show_game(data):
        for i in data:
            for j in i:
                print(j, " | ", end=" ")
            print()


game = GameServer()
web = WebServer()
# WebServer.show_game([['X', 'O', ''], ['X', 'X', 'O'], ['', '', '']])
