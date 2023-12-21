# 16-patch puzzle solver

starting_patches = "┌┌┐┐└└┘┘┤├┬┼╶╵╷ "

BOX_WIDTH = 6
BOX_HEIGHT = 6

starting_box = (
    "╔═╤══╗" +
    "║XXXX║" +
    "║XXXX╢" +
    "║XXXX║" +
    "║XXXX║" + 
    "╚═╧╧═╝"
)

LEFT = 1
RIGHT = 2
TOP = 4
BOTTOM = 8

# Format of pipe connections is a dictionary of patch symbol and a bitfield of connections
#  e.g. pipe_connections['┌'] = RIGHT | BOTTOM
pipe_connections = {
    ' ': 0,
    'X': 0,
    '┌': RIGHT | BOTTOM,
    '┐': LEFT | BOTTOM,
    '└': RIGHT | TOP,
    '┘': LEFT | TOP,
    '┤': LEFT | TOP | BOTTOM,
    '├': RIGHT | TOP | BOTTOM,
    '┬': LEFT | RIGHT | BOTTOM,
    '┴': LEFT | RIGHT | TOP,
    '┼': LEFT | RIGHT | TOP | BOTTOM,
    '╶': RIGHT,
    '╷': BOTTOM,
    '╴': LEFT,
    '╵': TOP,
    '─': LEFT | RIGHT,
    '│': TOP | BOTTOM,
    '╔': 0, # RIGHT | BOTTOM,
    '╗': 0, # LEFT | BOTTOM,
    '╚': 0, # RIGHT | TOP,
    '╝': 0, # LEFT | TOP,
    '╤': BOTTOM, # LEFT | RIGHT | BOTTOM,
    '╧': TOP, # LEFT | RIGHT | TOP,
    '╢': LEFT, # LEFT | TOP | BOTTOM,
    '╟': RIGHT, # RIGHT | TOP | BOTTOM,
    '║': 0, # TOP | BOTTOM,
    '═': 0, # LEFT | RIGHT,
}

if (False):
    print(f' Testing Pipe Connections')
    print(pipe_connections['╤'])
    print(pipe_connections['╤'] & LEFT > 0)
    print(pipe_connections['╤'] & RIGHT > 0)
    print(pipe_connections['╤'] & TOP > 0)
    print(pipe_connections['╤'] & BOTTOM > 0)

# Determine an arrangement such that all patches fit together in the box, and connect to the box edges.

# Approach:
# Starting at the first available X (in the upper-left corner)
#  For each space, get a list of all valid patches that will fit in that space
#   For each valid patch, add that patch to a temporary box and recurse in for the next space
#    If we fill a box completely, then add it to our list of valid solutions.

solved_boxes = []

def solve_box(box, available_patches):
    #print_box(box)

    # Find the first available X in the box
    next_tile = box.find('X')
    if next_tile == -1:
        # No more X's, so we're done
        # Check to see if it's fully connected
        if check_connections(box):
            # Ensure that solved_boxes doesn't already contain an equivalent box
            if box not in solved_boxes:
                solved_boxes.append(box)
                #print_box(box)
                #input()
        return True
    
    # Get the list of valid patches for this space

    get_valid_patches(box, next_tile, available_patches)

def get_adjacent_tiles(next_tile):
    return [
        (next_tile - 1,         RIGHT, LEFT),
        (next_tile + 1,         LEFT, RIGHT),
        (next_tile - BOX_WIDTH, BOTTOM, TOP),
        (next_tile + BOX_WIDTH, TOP, BOTTOM),
    ]

def get_valid_patches(box, next_tile, available_patches):
    adjacent_tiles = get_adjacent_tiles(next_tile)

    #print(f'## Current box:')
    #print_box(box)
    #print(f' Remaining tiles: {available_patches}')
    #input()

    # For each patch in the list of available patches, check if it fits in the space
    for this_patch in available_patches:
        connect_on_all_edges = True # Assume we connect until proven we don't

        for that_tile, that_edge, this_edge in adjacent_tiles:
            if that_tile >= 0 and that_tile < len(box):
                that_and_this_connect = False

                if box[that_tile] == 'X':
                    that_and_this_connect = True
                else:
                    that_conn = pipe_connections[box[that_tile]] & that_edge > 0
                    this_conn = pipe_connections[this_patch] & this_edge > 0

                    if that_conn == this_conn:
                        that_and_this_connect = True
                    else:
                        connect_on_all_edges = False
                        break

        if connect_on_all_edges:
            # Add this patch to the box and recurse
            new_box = box[:next_tile] + this_patch + box[next_tile+1:]
            new_patches = available_patches.replace(this_patch, '', 1)
            solve_box(new_box, new_patches)


def print_box(box):
    print(box_to_str(box))

def box_to_str(box):
    box_str = ''
    for row in range(BOX_HEIGHT):
        box_str += box[row*BOX_WIDTH:(row+1)*BOX_WIDTH] + '\n'
    return box_str

# Ensure a box is fully connected
def check_connections(box):
    next_inx = 0
    # Find the first tile in a box that can make a connection
    for tile_inx, tile in enumerate(box):
        if pipe_connections[tile] != 0:
            next_inx = tile_inx
            break

    tile_inx = next_inx

    # Replace that tile with an X
    box = box[:tile_inx] + 'X' + box[tile_inx+1:]

    iteration_cnt = 0
    num_replacements = 1

    while num_replacements > 0:
        iteration_cnt += 1
        #print(f'Flood fill step {iteration_cnt}. {num_replacements} last step:')
        #print_box(box)
        #input()
        # For every tile
        #  See if it connects to an X
        #   If so, then make this tile an X

        num_replacements = 0

        for tile_inx, tile in enumerate(box):
            new_symbol = ''
            if tile == 'X' or tile == ' ':
                # If this tile is already an X or a space, then we don't want to mess with it anymore
                continue
            elif pipe_connections[tile] == 0:
                # If this tile has no connections, then it can't be an X
                new_symbol = ' '
            else:
                adjacent_tiles = get_adjacent_tiles(tile_inx)
                for that_tile, that_edge, this_edge in adjacent_tiles:
                    if that_tile >= 0 and that_tile < len(box):
                        that_tile_symbol = box[that_tile]
                        if this_edge & pipe_connections[tile] > 0 and that_tile_symbol == 'X':
                            new_symbol = 'X'
                            break
            
            if new_symbol != '':
                box = box[:tile_inx] + new_symbol + box[tile_inx+1:]
                num_replacements += 1

    #print(f'Flood fill step {iteration_cnt}. {num_replacements} last step:')
    #print_box(box)
    #print(f' No replacements, final box!  Checking to ensure everything is blank or X...')
    #input()

    # If there is anything other than spaces and X's, then it's not fully connected
    for tile in box:
        if tile != ' ' and tile != 'X':
            return False
        
    return True

if (False):
    test_boxes = [
"""
╔═╤══╗
║╶┘┌┐║
║┌┬┤└╢
║└┼┘╷║
║ ├┐╵║
╚═╧╧═╝
""",
"""
╔═╤══╗
║╶┤╶╴║
║┌┤ ┌╢
║└┤┌┤║
║ ├┼┘║
╚═╧╧═╝
""",
"""
╔═╤══╗
║ ├┬┐║
║╶┼┤└╢
║┌┘└┐║
║└┐┌┘║
╚═╧╧═╝
"""
        ]    
    print(f' Testing boxes for connection')
    for box in test_boxes:
        print(f'Checking box:')
        box = box.replace('\n', '')
        print_box(box)
        print(f'Fully connected: {check_connections(box)}')
        print()
        print()
        input()

#exit()
print(f' Starting with box:')
print_box(starting_box)

print(f' Available tiles:')
print(starting_patches)

import math
print()
print(f' Number of possible combinations of {len(starting_patches)} tiles:')
print(f'{ math.factorial(len(starting_patches))}')
print()
print(f' Solving for potential solutions...')

solve_box(starting_box, starting_patches)

print(f' ...done!')
for box in solved_boxes:
    print_box(box)
    print()

print(f' Found {len(solved_boxes)} solutions.')

# Write each valid solution to a file
for i in range(len(solved_boxes)):
    with open(f'box{i}.txt', 'w') as f:
        f.write(box_to_str(solved_boxes[i]))

