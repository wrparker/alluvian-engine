import bcrypt
from django.db import models

import alluvian.globals

class Player(models.Model):
    room: int

    # Fields saved to database
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None

    def check_pw(self, password_input: str) -> bool:
        return bcrypt.checkpw(password_input.encode('utf-8'), self.password.encode('utf-8'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # In Memory fields
    @property
    def room(self):
        return alluvian.globals.rooms[self.__room]

    @room.setter
    def room(self, room) -> None:
        self.__room = room

