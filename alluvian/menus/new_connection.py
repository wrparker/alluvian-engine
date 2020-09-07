from enum import IntEnum

import logging
import copy
import alluvian.globals
from players.models import Player

from constants import PLAYER_START_ROOM

_LOG = logging.getLogger(__name__)

MAX_PASSWORD_ATTEMPTS = 3

class LoginState(IntEnum):
    GET_NAME = 0
    NEW_PLAYER_PROMPT = 1
    NEW_PLAYER_PASSWORD = 2
    PASSWORD_INPUT = 3
    AUTHENTICATED = 4


class NewConnectionMenu(object):
    id: int
    command: str

    def __init__(self, id, command):
        self.session = alluvian.globals.players[id]
        self.id = id
        self.command = command.lower()

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
            alluvian.globals.mud.send_message(id, "That name is invalid, try again: ")
        try:
            Player.objects.get(name=self.session.name)
            alluvian.globals.mud.send_message(self.id, 'Password: ')
            self.session.login_state = LoginState.PASSWORD_INPUT
        except Player.DoesNotExist:
            alluvian.globals.mud.send_message(self.id, f'Did I get that right, {self.session.name}? (Y/N)')
            self.session.login_state = LoginState.NEW_PLAYER_PROMPT

    def new_player_prompt(self) -> None:
        if self.command == 'y':
            alluvian.globals.mud.send_message(self.id, f"Ok, give me a password for {self.session.name}:")
            self.session.login_state = LoginState.NEW_PLAYER_PASSWORD
        else:
            alluvian.globals.mud.send_message(self.id, 'By what name do you wish to be known?')
            self.session.login_state = LoginState.GET_NAME

    def new_player_password(self) -> None:
        self.session.password = self.command
        try:
            player = Player.objects.create(name=self.session.name,
                                           password=self.session.password)
            alluvian.globals.mud.send_message(self.id, f"Congratulations!  We've registered {player.name}.")
            self.session.player = player
            self.session.player.room = PLAYER_START_ROOM
            self.session.login_state = LoginState.AUTHENTICATED
            alluvian.globals.interpreter.exec_cmd(self.id, 'Look')
        except Exception as e:
            _LOG.error(e)
            alluvian.globals.mud.send_message(self.id, "Error creating player.")

    def password_input(self) -> None:
        player = Player.objects.get(name=self.session.name)
        if self.session.bad_auth_attempts >= MAX_PASSWORD_ATTEMPTS:
            alluvian.globals.mud.send_message(self.id, "Exceeded allowed password attempts, hacking attempt logged...")
            alluvian.globals.mud.close_socket(self.id)
            del (alluvian.globals.players[self.id])
        elif not player.check_pw(self.command):
            self.session.bad_auth_attempts = self.session.bad_auth_attempts + 1
            alluvian.globals.mud.send_message(self.id, "Wrong password, try again: ")
        else:
            alluvian.globals.mud.send_message(self.id, "Logging you in ... \r\n")
            self.session.player = player
            self.session.player.room = PLAYER_START_ROOM
            self.session.login_state = LoginState.AUTHENTICATED
            if not self.check_logged_in():
                alluvian.globals.interpreter.exec_cmd(self.id, 'Look')
            alluvian.globals.mud.send_message(self.id, '\r\n')

    def authenticated(self) -> None:
        return

    def check_logged_in(self):
        for idx, sess in enumerate(alluvian.globals.players):
            sess = alluvian.globals.players.get(idx)
            if not sess:
                return False
            if idx != self.id and sess.login_state == LoginState.AUTHENTICATED and sess.player.name == self.session.name:
                self.session = copy.deepcopy(alluvian.globals.players[idx])
                alluvian.globals.mud.send_message(idx, "Multiple login detected, disconnecting you.")
                alluvian.globals.mud.close_socket(idx)
                alluvian.globals.mud.send_message(self.id, "You take over your own body, already in use!")
                return True
        return False




