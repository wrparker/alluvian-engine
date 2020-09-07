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

# import the MUD server class
from alluvian.server.mudserver import MudServer
from alluvian.commands.interpreter import Interpreter
from menus.new_connection import NewConnectionMenu, LoginState
from alluvian.server.connection_session import ConnectionSession
from world.models import Room

import alluvian.globals

# Initialize global variables
alluvian.globals.players = {}
alluvian.globals.rooms = {}
alluvian.globals.interpreter = Interpreter()

PROMPT = '> '

# Start Mud
alluvian.globals.mud = MudServer()
mud = alluvian.globals.mud

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

        # Character Login/Creation Handler
        if not connection_session.login_state == LoginState.AUTHENTICATED:  # Login Menu
            NewConnectionMenu(id, command)

        # Command Handler for default state.
        else:
            # Send player prompt
            mud.send_message(id, f'{PROMPT}\r\n')

            if not command:
                mud.send_message(id, "\r\n")
                continue
            cmd = alluvian.globals.interpreter.cmd_search(command, alluvian.globals.players[id].player)
            if cmd:
                cmd(actor=id,
                    arguments=params).execute()
            else:
                mud.send_message(id, "Huh?!\r\n")
            mud.send_message(id, f'\r\n{PROMPT}')
