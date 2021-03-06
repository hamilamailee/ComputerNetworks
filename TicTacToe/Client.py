import threading
from Message import *
from Game import *
from init import HOST, PORT
import socket


class Client:
    def __init__(self) -> None:
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cs.connect((HOST, PORT))
        except socket.error as e:
            print(str(e))
        self.client_thread()

    def client_thread(self):
        self.cs.send(Message("", MType.CONNECTION, CType.CLIENT).json)
        while True:
            recieved = self.cs.recv(2048)
            if not recieved:
                continue
            for r in recieved.decode('utf-8').split("@"):
                if not r:
                    continue
                r = json.loads(r)
                match r['type']:
                    case MType.INFORM:
                        print(r['message'])
                        continue
                    case MType.ID:
                        print(f"You are Client {r['message']}")
                        self.id = int(r['message'])
                        continue
                    case MType.MOVE:
                        Game.show_game(r['message'])
                        optinos = Game.game_options(r['message'])
                        while True:
                            o = input("Your choice: ")
                            if o == "/exit":
                                self.cs.send(
                                    Message("", MType.END, CType.CLIENT).json)
                                break
                            if int(o) in optinos:
                                self.cs.send(
                                    Message(int(o), MType.MOVE, CType.CLIENT).json)
                                break
                            print("Wrong choice. Please try again.")
                    case MType.END:
                        print("The game has ended. Closing socket ...")
                        self.cs.close()
                        return


gameserver = Client()
