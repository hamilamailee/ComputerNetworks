from _thread import *
import json
from init import *
import socket
from Message import *


class WebServer:
    last_client = 0
    last_gameserver = 0

    def __init__(self) -> None:
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameservers = dict()
        self.clients = dict()
        self.tuples = dict()
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
                self.handle_game_server(connection)
                return
            case CType.CLIENT:
                connection.send(
                    Message(self.last_client, MType.ID, "").json)
                self.handle_client(connection)

    def handle_game_server(self, connection):
        self.gameservers[connection] = self.last_gameserver
        self.last_gameserver += 1
        connection.send(
            Message("Waiting for a client to connect", MType.INFORM, "").json)
        if len(self.clients) > 0:
            game_server = connection
            game_client = list(self.clients.items())[0][0]
            self.start_game(game_client, game_server)

    def handle_client(self, connection):
        self.clients[connection] = self.last_client
        self.last_client += 1
        connection.send(
            Message("Looking for a gameserver", MType.INFORM, "").json)
        if len(self.gameservers) > 0:
            game_server = list(self.gameservers.items())[0][0]
            game_client = connection
            self.start_game(game_client, game_server)

    def start_game(self, client: socket.socket, server: socket.socket):
        server_id = self.gameservers[server]
        client_id = self.clients[client]
        server.send(Message(
            f"Client {client_id} has been connected.", MType.INFORM, "").json)
        client.send(Message(
            f"You've been connected to GameServer {server_id}", MType.INFORM, "").json)
        self.gameservers.pop(server)
        self.clients.pop(client)

    def show_game(data):
        for i in data:
            for j in i:
                print(j, " | ", end=" ")
            print()


webserver = WebServer()
