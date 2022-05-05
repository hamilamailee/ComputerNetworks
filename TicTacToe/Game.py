import enum
from time import sleep
from typing_extensions import Self
from Message import *


class Game:
    def __init__(self, player1, player2) -> None:     # player1 will be server in AI mode
        self.player1 = player1
        self.player2 = player2
        self.data = [["" for i in range(3)] for j in range(3)]
        self.server_client_game()

    def server_client_game(self):
        while self.game_end_message():
            self.player2.send(self.game_start_msg('X'))
            self.player2.send(Message(self.data, MType.MOVE, "").json)
            move = json.loads(self.player2.recv(2048))
            self.data[move//3][move % 3] = 'X'
            if not self.game_end_message():
                return
            self.player1.send(self.game_start_msg('O'))
            self.player1.send(Message(self.data, MType.MOVE, "").json)
            move = json.loads(self.player1.recv(2048))
            self.data[move//3][move % 3] = 'O'
        return

    def show_game(data):
        for i in data:
            for j in i:
                print(str(j) + " | ", end=" ")
            print()

    def game_options(data):
        options = []
        for i in range(3):
            for j in range(3):
                if data[i][j] == "":
                    print(f"{i*3+j}\t->\t({i},{j})")
                    options.append(i*3 + j)
        return options

    def check_win(self):
        for i in range(3):
            if self.data[i][0] == self.data[i][1] == self.data[i][2] and self.data[i][0] != "":
                return self.data[i][0]
            elif self.data[0][i] == self.data[1][i] == self.data[2][i] and self.data[0][i] != "":
                return self.data[0][i]
        if self.data[0][0] == self.data[1][1] == self.data[2][2] and self.data[0][0] != "":
            return self.data[0][0]
        if self.data[0][2] == self.data[1][1] == self.data[2][2] and self.data[0][2] != "":
            return self.data[0][2]
        for i in range(3):
            for j in range(3):
                if self.data[i][j] == "":
                    return ""
        return 'E'

    def game_end_message(self):
        end = self.check_win()
        match end:
            case 'X':
                self.player2.send(Message("YOU WON!", MType.INFORM, "").json)
                self.player1.send(Message("YOU LOST!", MType.INFORM, "").json)
                return 0
            case 'O':
                self.player2.send(Message("YOU LOST!", MType.INFORM, "").json)
                self.player1.send(Message("YOU WON!", MType.INFORM, "").json)
                return 0
            case 'E':
                self.player2.send(Message("TIE!", MType.INFORM, "").json)
                self.player1.send(Message("TIE!", MType.INFORM, "").json)
                return 0
            case '':
                return 1

    def game_start_msg(self, piece):
        return Message(f"Choose the place you want to insert \"{piece}\"", MType.INFORM, "").json


class GType(enum.Enum):
    AI = "AI"
    PLAYER = "PLAYER"
