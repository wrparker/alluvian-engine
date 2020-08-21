import bcrypt
from django.db import models

class Player(models.Model):

    class Meta:
        db_table = "players"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def set_password(self, password: str) -> None:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        self.password = hashed


    def check_pw(self, password_input: str) -> bool:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_input.encode('utf-8'), salt)
        return hashed == self.password

