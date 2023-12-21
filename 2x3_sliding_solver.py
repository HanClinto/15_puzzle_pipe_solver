# Given a sliding puzzle that looks like:
# " └┐" +
# "┬╶┼"

# We want to arrive at:
# " └┐" +
# "╶┬┼"

# Goal: Generate a list of steps that will solve the puzzle.

all_states = {}

board_width = 3
board_height = 2

starting_state = "X└┐" + "┬╶┼"
target_state   = "X└┐" + "╶┬┼"

def get_child_states(state):
    child_states = []
    # Find the blank space
    blank_index = state.find('X')

    adjacent_tile_idxs = get_adjacent_tile_indices(blank_index)

    # For each orthogonal tile to the blank space
    for adjacent_idx in adjacent_tile_idxs:
        # Set the blank tile to be equal to the value of the adjacent idx
        child_state = state[:blank_index] + state[adjacent_idx] + state[blank_index+1:]
        # Set the adjacent tile to be equal to the blank square
        child_state = child_state[:adjacent_idx] + 'X' + child_state[adjacent_idx+1:]

        # Add to list of possible states
        child_states.append(child_state)

    # Return list of possible states
    return child_states

def get_adjacent_tile_indices(index):
    adjacent_tile_idxs = []
    # Check for valid left
    if (index % board_width > 0):
        adjacent_tile_idxs.append(index - 1)
    # Check for valid right
    if (index % board_width < board_width - 1):
        adjacent_tile_idxs.append(index + 1)
    # Check for valid up
    if (index >= board_width):
        adjacent_tile_idxs.append(index - board_width)
    # Check for valid down
    if (index < board_width * (board_height - 1)):
        adjacent_tile_idxs.append(index + board_width)
    return adjacent_tile_idxs

def print_board(state, tab=0):
    for row in range(board_height):
        print(" " * tab + state[row*board_width:row*board_width+board_width])

print(f' Starting state:')
print_board(starting_state)

last_new_children = get_child_states(starting_state)

all_states[starting_state] = last_new_children

while len(last_new_children) > 0:
    new_children = []
    # Check each child and see if it's the target state
    for child in last_new_children:
        if child == target_state:
            print(f' Found target state:')
            print_board(child)
            exit()
        elif child not in all_states:
            this_children = get_child_states(child)
            all_states[child] = this_children
            new_children.extend(this_children)
    
    last_new_children = new_children

print(f' Found {len(all_states)} possible states:')
import math
print(f' Total permutations: {math.factorial(board_width * board_height)}')
#print(all_states)

#exit()

# Get all keys in all_states

# Print each state in the list and its children
if (False):
    for state in all_states:
        print(f' State:')
        print_board(state, 0)
        for child in all_states[state]:
            print(f'  Child:')
            print_board(child, 0)
