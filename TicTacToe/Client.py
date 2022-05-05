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
        self.cs.send(str.encode("CLIENT"))
        message = self.cs.recv(2048).decode('utf-8')
        print(message)
        self.id = int(message.split(" ")[-1])
        while True:
            send = input("Your message: ")
            self.cs.send(str.encode(send))
            reply = self.cs.recv(2048)
            de_reply = reply.decode('utf-8')
            print(de_reply)
            if de_reply == "/end":
                break
        self.cs.close()


client = Client()