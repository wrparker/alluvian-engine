import bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def set_password(self, password: str) -> None:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        self.password = hashed


    def check_pw(self, password_input: str) -> bool:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_input, salt)
        if hashed == self.password:
            return True
        return False
