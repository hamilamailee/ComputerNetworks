from Message import *
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
            recieved = json.loads(self.cs.recv(2048))
            match recieved['type']:
                case MType.ID:
                    print(f"You are Client {recieved['message']}")
                    self.id = int(recieved['message'])
                    continue
                case MType.END:
                    print("The game has ended. Closing socket ...")
                    self.cs.close()
                    return


gameserver = Client()
