from _thread import *
from init import HOST, PORT
import socket


class WebServer:
    last_client = 0
    last_gameserver = 0

    def __init__(self) -> None:
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameservers = []
        self.clients = []
        self.tuples = []
        self.start_server()

    def start_server(self):
        try:
            self.ss.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
        print("WebServer is listening ...")
        self.ss.listen()
        while True:
            connection, address = self.ss.accept()
            start_new_thread(self.server_thread, (connection,))

    def server_thread(self, connection):
        c_type = connection.recv(2048).decode('utf-8')
        if (c_type == "GAMESERVER"):
            print("A gameserver has been connected")
            self.gameservers.append(connection)
            connection.send(str.encode(
                f"You are GameServer {self.last_gameserver}"))
            self.last_gameserver += 1
            self.handle_game_server(connection)
        elif (c_type == "CLIENT"):
            print("A client has been connected")
            self.clients.append(connection)
            connection.send(str.encode(f"You are Client {self.last_client}"))
            self.last_client += 1
            self.handle_client(self, connection)

    def handle_game_server(self, connection):
        while True:
            message = connection.recv(2048).decode('utf-8')
            print("recieved message: ", message)
            if message == "/end":
                break
            reply = f'Server: {message}'
            connection.sendall(str.encode(reply))
        connection.close()

    def handle_client(self, connection):
        while True:
            message = connection.recv(2048).decode('utf-8')
            print("recieved message: ", message)
            if message == "/end":
                break
            reply = f'Server: {message}'
            connection.sendall(str.encode(reply))
        connection.close()

    def show_game(data):
        for i in data:
            for j in i:
                print(j, " | ", end=" ")
            print()


webserver = WebServer()
