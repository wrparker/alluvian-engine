import bcrypt

class Connection:
    name: str
    password: str
    new_player: bool
    start_room: str

    def __init__(self):
        self.name = None
        self.password = None
        self.new_player = None
        self.start_room = None

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
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            self.__password = hashed
        else:
            self.__password = None

    @property
    def new_player(self) -> bool:
        return self.__new_player

    @new_player.setter
    def new_player(self, new_player) -> None:
        self.__new_player = new_player

    @property
    def start_room(self) -> bool:
        return self.__start_room

    @start_room.setter
    def start_room(self, start_room) -> None:
        self.__start_room = start_room
