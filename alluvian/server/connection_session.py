import bcrypt
from players.models import Player

from menus.new_connection import LoginState


class ConnectionSession:
    name: str
    password: str
    player: Player
    bad_auth_attempts: int
    login_state: LoginState

    def __init__(self):
        self.name = None
        self.password = None
        self.player = None
        self.bad_auth_attempts = 0
        self.login_state = LoginState.GET_NAME

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name) -> None:
        self.__name = name

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password) -> None:
        if password:
            salt = bcrypt.gensalt(12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            self.__password = hashed.decode('utf-8')
        else:
            self.__password = None

    @property
    def login_state(self) -> LoginState:
        return self.__login_state

    @login_state.setter
    def login_state(self, login_state) -> None:
        self.__login_state = login_state

    @property
    def player(self) -> bool:
        return self.__player

    @player.setter
    def player(self, player) -> None:
        self.__player = player

    @property
    def bad_auth_attempts(self) -> int:
        return self.__bad_auth_attempts

    @bad_auth_attempts.setter
    def bad_auth_attempts(self, attempts) -> None:
        self.__bad_auth_attempts = attempts
