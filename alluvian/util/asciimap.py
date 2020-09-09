from world.models import Room
import alluvian.globals as globs

DEFAULT_CHAR = '.'

def blank_map():
    room_map = []
    for x in range(0,3):
        tmp = []
        for y in range(0,3):
            tmp.append(DEFAULT_CHAR)
        room_map.append(' ')
    return room_map

def build_map(room: Room):
    room_map = []
    for x in range(0,3):
        tmp = []
        for y in range(0,3):
            tmp.append(DEFAULT_CHAR)
        room_map.append(tmp)

    room_map[1][1] = '@'

    if not room.exit_north:
        room_map[0][1] = '#'

    if not room.exit_south:
        room_map[2][1] = '#'

    if not room.exit_west:
        room_map[1][0] = '#'

    if not room.exit_east:
        room_map[1][2] = '#'

    if room.exit_up:
        room_map[0][0] = '^'
    else:
        if room.exit_north and room.exit_west:
            room_map[0][0] = '.'
        else:
            room_map[0][0] = '#'

    if room.exit_down:
        room_map[2][2] = 'V'
    else:
        if room.exit_south and room.exit_east:
            room_map[2][2] = '.'
        else:
            room_map[2][2] = '#'

    # Weird ones...
    if room.exit_west and room.exit_south:
        room_map[2][0] = '.'
    else:
        room_map[2][0] = '#'

    if room.exit_east and room.exit_north:
        room_map[0][2] = '.'
    else:
        room_map[0][2] = '#'
    return room_map

def show_map(room: Room):
    map_data = build_map(room)
    msg = ''
    for i in range(0,3):
        for y in range(0,3):
            msg += map_data[i][y]
        msg += '\n\r'
    return msg

def show_blank_map():
    map_data = blank_map()
    msg = ''
    for i in range(0,3):
        for y in range(0,3):
            msg += map_data[i][y]
        msg += '\n\r'
    return msg

def traverse_room(room: Room):
    nroom = blank_map()
    wroom = blank_map()
    eroom = blank_map()
    sroom = blank_map()

    if room.exit_north:
        nroom = build_map(globs.rooms[room.exit_north])
    if room.exit_south:
        sroom = build_map(globs.rooms[room.exit_south])
    if room.exit_west:
        wroom = build_map(globs.rooms[room.exit_west])
    if room.exit_east:
        eroom = build_map(globs.rooms[room.exit_east])

    this_room = show_map(room)

    return this_room, nroom, sroom, wroom, eroom

