from enum import IntEnum

import alluvian.globals
from alluvian.server.mudserver import MudServer
from players.models import Player

MAX_PASSWORD_ATTEMPTS = 3

class LoginState(IntEnum):
    GET_NAME = 0
    NEW_PLAYER_PROMPT = 1
    NEW_PLAYER_PASSWORD = 2
    PASSWORD_INPUT = 3
    AUTHENTICATED = 4


class NewConnectionMenu(object):
    id: int
    mud: MudServer
    command: str

    def __init__(self, id, mud, command):
        self.session = alluvian.globals.players[id]
        self.id = id
        self.mud = mud
        self.command = command

        self.switch = {
            LoginState.GET_NAME: self.get_name,
            LoginState.NEW_PLAYER_PROMPT: self.new_player_prompt,
            LoginState.NEW_PLAYER_PASSWORD: self.new_player_password,
            LoginState.PASSWORD_INPUT: self.password_input,
            LoginState.AUTHENTICATED: self.authenticated
        }

        self.switch.get(LoginState(self.session.login_state))()


    def get_name(self) -> None:
        self.session.name = self.command.title()
        if not self.command.isalpha():
            self.mud.send_message(id, "That name is invalid, try again: ")
        try:
            Player.objects.get(name=self.session.name)
            self.mud.send_message(self.id, 'Password: ')
            self.session.login_state = LoginState.PASSWORD_INPUT
        except Player.DoesNotExist:
            self.mud.send_message(self.id, f'Did I get that right, {self.session.name}? (Y/N)')
            self.session.login_state = LoginState.NEW_PLAYER_PROMPT

    def new_player_prompt(self) -> None:
        if self.command.lower() == 'y':
            self.mud.send_message(self.id, f"Ok, give me a password for {self.session.name}:")
            self.session.login_state = LoginState.NEW_PLAYER_PASSWORD
        else:
            self.mud.send_message(self.id, 'By what name do you wish to be known?')
            self.session.login_state = LoginState.GET_NAME

    def new_player_password(self) -> None:
        self.session.password = self.command
        try:
            player = Player.objects.create(name=self.session.name,
                                           password=self.session.password)
            self.mud.send_message(self.id, f"Congratulations!  We've registered {player.name}.")
            self.session.room = 1
            self.session.player = player
            self.session.login_state = LoginState.AUTHENTICATED
            self.mud.send_message(self.id, alluvian.globals.rooms[alluvian.globals.players[self.id].room].description)
        except:
            self.mud.send_message(self.id, "Error creating player.")

    def password_input(self) -> None:
        player = Player.objects.get(name=self.session.name)
        if self.session.bad_auth_attempts >= MAX_PASSWORD_ATTEMPTS:
            self.mud.send_message(self.id, "Exceeded allowed password attempts, hacking attempt logged...")
            self.mud.close_socket(self.id)
            del (alluvian.globals.players[self.id])
        elif not player.check_pw(self.command):
            self.session.bad_auth_attempts = self.session.bad_auth_attempts + 1
            self.mud.send_message(self.id, "Wrong password, try again: ")
        else:
            self.mud.send_message(self.id, "Logging you in ... \r\n")
            self.session.room = 1
            self.session.player = player
            self.session.login_state = LoginState.AUTHENTICATED
            self.mud.send_message(self.id, alluvian.globals.rooms[alluvian.globals.players[self.id].room].description)

    def authenticated(self) -> None:
        return



