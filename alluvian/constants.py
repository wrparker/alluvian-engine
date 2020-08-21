from enum import Enum
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class PlayerType(Enum):
    PLAYER = 1
    IMM = 2
    GOD = 3
    IMPL = 4

