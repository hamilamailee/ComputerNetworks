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
        self.gs.send(str.encode("GAMESERVER"))
        message = self.gs.recv(2048).decode('utf-8')
        print(message)
        self.id = int(message.split(" ")[-1])
        while True:
            send = input("Your message: ")
            self.gs.send(str.encode(send))
            reply = self.gs.recv(2048)
            de_reply = reply.decode('utf-8')
            print(de_reply)
            if de_reply == "/end":
                break
        self.gs.close()


gameserver = GameServer()
