import enum
import json


class Message:
    def __init__(self, message, m_type, c_type):
        self.message = message
        self.type = m_type
        self.sender = c_type
        self.json = json.dumps(self.__dict__).encode()


class MType(str, enum.Enum):
    CONNECTION = 'CONNECTION'   # messages showing connection
    ID = 'ID'                   # getting id from webserver
    START = 'START'             # start of the game
    MOVE = 'MOVE'               # movement for the game
    END = 'END'                 # close sockets


class CType(str, enum.Enum):
    GAMESERVER = 'GAMESERVER'
    CLIENT = 'CLIENT'
