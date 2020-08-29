import bcrypt
from django.db import models

class Player(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=1)


    def check_pw(self, password_input: str) -> bool:
        return bcrypt.checkpw(password_input.encode('utf-8'), self.password.encode('utf-8'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
