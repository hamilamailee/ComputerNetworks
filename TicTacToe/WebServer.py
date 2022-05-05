from _thread import *
from ast import match_case
import json
from init import HOST, PORT
import socket
from Message import *


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
        c_type = json.loads(connection.recv(2048))
        match c_type['sender']:
            case CType.GAMESERVER:
                connection.send(
                    Message(self.last_gameserver, MType.ID, "").json)
                self.last_gameserver += 1
                self.handle_game_server(connection)
                return

            case CType.CLIENT:
                connection.send(
                    Message(self.last_client, MType.ID, "").json)
                self.last_client += 1
                self.handle_client(connection)
                return

    def handle_game_server(self, connection):
        self.gameservers.append(connection)
        while True:
            message = connection.recv(2048).decode('utf-8')
            print("recieved message: ", message)
            if message == "/end":
                break
            reply = f'Server: {message}'
            connection.sendall(str.encode(reply))
        connection.close()

    def handle_client(self, connection):
        self.clients.append(connection)
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
