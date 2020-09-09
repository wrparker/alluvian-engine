from world.models import Room
import alluvian.globals as globs

DEFAULT_CHAR = '.'

def blank_room_map():
    return [[' ' for y in range(3)] for x in range(3)]

def build_room_characters(room: Room):
    room_map = []
    for x in range(0,3):
        tmp = []
        for y in range(0,3):
            tmp.append(DEFAULT_CHAR)
        room_map.append(tmp)

    room_map[1][1] = '.'

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

def generate_map_display_data(room_id, x, y, map_display_data):
    cluster_offsets = [0,0,1,4,7,10,13]

    center_x = cluster_offsets[x]
    center_y = cluster_offsets[y]

    if isinstance(room_id, int):  # special check from room 0... if 0 == False
        rmap = build_room_characters(globs.rooms[room_id])
    else:
        rmap = blank_room_map()
    map_display_data[center_x-1][center_y-1] = rmap[0][0]
    map_display_data[center_x - 1][center_y] = rmap[1][0]
    map_display_data[center_x-1][center_y+1] = rmap[0][2]

    map_display_data[center_x][center_y - 1] = rmap[0][1]
    map_display_data[center_x][center_y + 1] = rmap[2][1]
    map_display_data[center_x][center_y] = rmap[1][1]

    map_display_data[center_x+1][center_y-1] = rmap[0][2]
    map_display_data[center_x + 1][center_y] = rmap[1][2]
    map_display_data[center_x+1][center_y+1] = rmap[2][2]

    return map_display_data



def show_map(room: Room):
    map_data = traverse_room(room,4,3,8,6,0,0)
    map_display_data = initialize_map_display_data()
    msg = '+---------------+\r\n'

    for x in range(2, 7):
        for y in range(2, 5):
            map_display_data = generate_map_display_data(map_data[x][y], x, y, map_display_data)

    map_display_data[7][4] = '@'
    for y in range(0, 9):
        msg += '|'
        for x in range(0, 15):
            msg += map_display_data[x][y]
        msg += '|\r\n'
    msg += '+---------------+\r\n'
    return msg


def initialize_map_data(max_x, max_y):
    return [[None for y in range(max_y)] for x in range(max_x)]

def initialize_map_display_data():
    return [[' ' for y in range(9)] for x in range(15)]


def traverse_room(room, x, y, max_x, max_y, min_x, min_y, map_data=None):
    if not isinstance(map_data, list): # initialize
        map_data = initialize_map_data(max_x, max_y)

    if(x > max_x) or (y > max_y) or (x < min_x) or (y < min_y):
        return map_data
    if map_data[x][y]:
        return map_data
    else:
        map_data[x][y] = room.id

    if room.exit_north:
        map_data = traverse_room(globs.rooms[room.exit_north], x, y-1, max_x, max_y, min_x, min_y, map_data)

    if room.exit_south:
        map_data = traverse_room(globs.rooms[room.exit_south], x, y+1, max_x, max_y, min_x, min_y, map_data)

    if room.exit_east:
        map_data = traverse_room(globs.rooms[room.exit_east], x+1, y, max_x, max_y, min_x, min_y, map_data)

    if room.exit_west:
        map_data = traverse_room(globs.rooms[room.exit_west], x-1, y, max_x, max_y, min_x, min_y, map_data)

    return map_data

