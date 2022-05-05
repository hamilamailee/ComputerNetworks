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
            recieved = self.gs.recv(2048)
            for r in recieved.decode('utf-8').split("@"):
                if not r:
                    continue
                r = json.loads(r)
                match r['type']:
                    case MType.INFORM:
                        print(r['message'])
                        continue
                    case MType.ID:
                        print(f"You are GameServer {r['message']}")
                        self.id = int(r['message'])
                        continue
                    case MType.END:
                        print("The game has ended. Closing socket ...")
                        self.gs.close()
                        return


gameserver = GameServer()
