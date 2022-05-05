from _thread import *
import json
import threading
from init import *
import socket
from Message import *
from Game import *


class WebServer:
    last_client = 0
    last_gameserver = 0

    def __init__(self) -> None:
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameservers = dict()
        self.clients = dict()
        self.games = []
        self.start_server()

    def start_server(self):
        try:
            self.ss.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
        print("WebServer is listening ...")
        threading.Thread(target=self.interactive_console, args=()).start()
        self.ss.listen()
        while True:
            connection, address = self.ss.accept()
            start_new_thread(self.server_thread, (connection,))

    def interactive_console(self):
        while True:
            string = input()
            match string:
                case "/users":
                    print(
                        f"Number of clients participating in a game: {len(self.games)}")

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

    def handle_client(self, connection):
        self.clients[connection] = self.last_client
        self.last_client += 1
        connection.send(
            Message("Looking for a gameserver", MType.INFORM, "").json)
        self.find_game_server(connection)

    def handle_game_server(self, connection):
        self.gameservers[connection] = self.last_gameserver
        self.last_gameserver += 1
        connection.send(
            Message("Waiting for a client to connect", MType.INFORM, "").json)
        self.find_client(connection)

    def find_client(self, connection):
        if len(self.clients) > 0:
            game_server = connection
            game_client = list(self.clients.items())[0][0]
            self.start_game(game_client, game_server)

    def find_game_server(self, connection):
        if len(self.gameservers) > 0:
            game_server = list(self.gameservers.items())[0][0]
            game_client = connection
            self.start_game(game_client, game_server)

    def check_game(self):
        if len(self.gameservers) > 0 and len(self.clients) > 0:
            self.start_game(list(self.clients.items())[
                            0][0], list(self.gameservers.items())[0][0])
        return

    def start_game(self, client: socket.socket, server: socket.socket):
        server_id = self.gameservers[server]
        client_id = self.clients[client]
        server.send(Message(
            f"Client {client_id} has been connected.", MType.INFORM, "").json)
        client.send(Message(
            f"You've been connected to GameServer {server_id}", MType.INFORM, "").json)
        self.gameservers.pop(server)
        self.clients.pop(client)
        game = Game(server, client)
        self.games.append(game)
        game.server_client_game()
        game.player2.send(Message("", MType.END, "").json)
        self.games.remove(game)
        self.gameservers[server] = server_id
        self.check_game()


webserver = WebServer()
