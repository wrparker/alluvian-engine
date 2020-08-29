from enum import Enum
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class PlayerType(Enum):
    PLAYER = 1
    IMM = 2
    GOD = 3
    IMPL = 4


class LoginState(Enum):
    GET_NAME = 0
    NEW_PLAYER_PROMPT = 1
    NEW_PLAYER_PASSWORD = 2
    PASSWORD_INPUT = 3
    BAD_PASSWORD = 4
    AUTHENTICATED = 5
