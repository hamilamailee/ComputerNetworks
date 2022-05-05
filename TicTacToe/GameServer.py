from Message import *
from init import HOST, PORT
import socket


class GameServer:
    def __init__(self) -> None:
        self.gs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.gs.connect((HOST, PORT))
        except socket.error as e:
            print(str(e))
        self.game_thread()

    def game_thread(self):
        self.gs.send(Message("", MType.CONNECTION, CType.GAMESERVER).json)
        while True:
            recieved = json.loads(self.gs.recv(2048))
            match recieved['type']:
                case MType.ID:
                    print(f"You are GameServer {recieved['message']}")
                    self.id = int(recieved['message'])
                    continue
                case MType.END:
                    print("The game has ended. Closing socket ...")
                    self.gs.close()
                    return


gameserver = GameServer()
