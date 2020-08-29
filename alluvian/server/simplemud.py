#!/usr/bin/env python

"""A simple Multi-User Dungeon (MUD) game. Players can talk to each
other, examine their surroundings and move between rooms.

Some ideas for things to try adding:
    * More rooms to explore
    * An 'emote' command e.g. 'emote laughs out loud' -> 'Mark laughs
        out loud'
    * A 'whisper' command for talking to individual players
    * A 'shout' command for yelling to players in all rooms
    * Items to look at in rooms e.g. 'look fireplace' -> 'You see a
        roaring, glowing fire'
    * Items to pick up e.g. 'take rock' -> 'You pick up the rock'
    * Monsters to fight
    * Loot to collect
    * Saving players accounts between sessions
    * A password login
    * A shop from which to buy items

author: Mark Frimston - mfrimston@gmail.com
"""

import json
import os

# import the MUD server class
from alluvian.server.mudserver import MudServer
from alluvian.commands.command_interpreter import CommandInterpreter
from players.models import Player
from alluvian.server.connection_session import ConnectionSession
from constants import LoginState
from world.models import Room

import alluvian.globals

# Initialize global variables
alluvian.globals.players = {}
alluvian.globals.rooms = {}

# Start Mud
mud = MudServer()

# Load rooms
alluvian.globals.rooms = dict((o.pk, o) for o in Room.objects.all())

# Main Game Loop
while True:

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    # go through any newly connected players
    for id in mud.get_new_players():

        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. We set their room to
        # None initially until they have entered a name
        # Try adding more player stats - level, gold, inventory, etc
        alluvian.globals.players[id] = ConnectionSession()

        # send the new player a prompt for their name
        mud.send_message(id, "By what name do you wish to be known?")

    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in alluvian.globals.players:
            continue

        # go through all the players in the game
        for pid, pl in alluvian.globals.players.items():
            # send each player a message to tell them about the diconnected
            # player
            mud.send_message(pid, "{} quit the game".format(
                                                        alluvian.globals.players[id].name))

        # remove the player's entry in the player dictionary
        del(alluvian.globals.players[id])

    # go through any new commands sent from players
    for id, command, params in mud.get_commands():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in alluvian.globals.players:
            continue

        connection_session = alluvian.globals.players[id]
        if not connection_session.login_state == LoginState.AUTHENTICATED:  # Login Menu
            if connection_session.login_state == LoginState.GET_NAME:
                connection_session.name = command.title()
                if not command.isalpha():
                    mud.send_message(id, "That name is invalid, try again: ")
                elif Player.objects.filter(name=connection_session.name).count() == 0:
                    mud.send_message(id, f'Did I get that right, {connection_session.name}? (Y/N)')

                    connection_session.login_state = LoginState.NEW_PLAYER_PROMPT
                else:
                    mud.send_message(id, 'Password: ')
                    connection_session.name = connection_session.name
                    connection_session.login_state = LoginState.PASSWORD_INPUT
            elif connection_session.login_state == LoginState.NEW_PLAYER_PROMPT:
                if command.lower() == 'y':
                    mud.send_message(id, f"Ok, give me a password for {connection_session.name}:")
                    connection_session.login_state = LoginState.NEW_PLAYER_PASSWORD
                else:
                    mud.send_message(id, 'By what name do you wish to be known?')
                    connection_session.login_state = LoginState.GET_NAME

            elif connection_session.login_state == LoginState.NEW_PLAYER_PASSWORD:
                connection_session.password = command
                try:
                    player = Player.objects.create(name=connection_session.name,
                                                   password=connection_session.password)
                    mud.send_message(id, f"Congratulations!  We've registered {player.name}.")
                    connection_session.room = 1
                    connection_session.player = player
                    connection_session.login_state = LoginState.AUTHENTICATED
                    mud.send_message(id, alluvian.globals.rooms[alluvian.globals.players[id].room].description)
                except:
                    mud.send_message(id, "Error creating player.")

            elif connection_session.login_state == LoginState.PASSWORD_INPUT:
                player = Player.objects.get(name=connection_session.name)
                if not player.check_pw(command):  # have to check unhashed.
                    connection_session.bad_auth_attempts = connection_session.bad_auth_attempts + 1
                    mud.send_message(id, "Wrong password, try again: ")
                    if connection_session.bad_auth_attempts >= 3:
                        mud.send_message(id, "Exceeded allowed password attempts, hacking attempt logged...")
                        mud.close_socket(id)
                        del (alluvian.globals.players[id])
                else:
                    mud.send_message(id, "Logging you in ... \r\n")
                    connection_session.room = 1
                    connection_session.player = player
                    connection_session.login_state = LoginState.AUTHENTICATED
                    mud.send_message(id, alluvian.globals.rooms[alluvian.globals.players[id].room].description)


        # Command Handler for default state.
        else:
            if not command:
                mud.send_message(id, "\n")
                continue
            cmd = CommandInterpreter.cmd_search(command)
            if cmd:
                cmd(mud_server=mud,
                    actor=id,
                    arguments=params).execute()
            else:
                mud.send_message(id, "Huh?!")

