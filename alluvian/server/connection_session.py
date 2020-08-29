import bcrypt
import players

class ConnectionSession:
    name: str
    password: str
    new_player: bool
    room: str
    player: players.models.Player

    def __init__(self):
        self.name = None
        self.password = None
        self.new_player = None
        self.room = None

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
    def new_player(self) -> bool:
        return self.__new_player

    @new_player.setter
    def new_player(self, new_player) -> None:
        self.__new_player = new_player

    @property
    def room(self) -> bool:
        return self.__room

    @room.setter
    def room(self, room) -> None:
        self.__room = room

    @property
    def player(self) -> bool:
        return self.__player

    @player.setter
    def player(self, player) -> None:
        self.__player = player

