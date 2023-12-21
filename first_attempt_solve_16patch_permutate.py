# 16-patch puzzle solver

# 
# ┐ ┌ ┘ └ ─ │ ┼
# ┤ ├ ┴ ┬ ┼ ─
# ╶ ╷ ╵ ╴ ┼ ─
# ┌ ─ ┐ ┌ ─ ┐ ┌ ─ ┐


patches = "┌┌┐┐└└┘┘┤├┬┼╶╵╷ "

box = [
    "╔═╤══╗",
    "║XXXX║",
    "║XXXX╢",
    "║XXXX║",
    "║XXXX║",
    "╚═╧╧═╝"
]

LEFT = 1
RIGHT = 2
TOP = 4
BOTTOM = 8

# Format of pipe connections is a dictionary of patch symbol and a bitfield of connections
#  e.g. pipe_connections['┌'] = RIGHT | BOTTOM
pipe_connections = {
    ' ': 0,
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
    '╔': RIGHT | BOTTOM,
    '╗': LEFT | BOTTOM,
    '╚': RIGHT | TOP,
    '╝': LEFT | TOP,
    '╤': LEFT | RIGHT | BOTTOM,
    '╧': LEFT | RIGHT | TOP,
    '╢': LEFT | TOP | BOTTOM,
    '╟': RIGHT | TOP | BOTTOM,
    '║': TOP | BOTTOM,
    '═': LEFT | RIGHT,
}

print(pipe_connections['╤'])

# Determine an arrangement such that all patches fit together in the box, and connect to the box edges.

# Approach:
#  1. Find all possible arrangements of patches
#  2. For each arrangement, check if it fits in the box
#  3. If it fits, check if it connects to the box edges
#  4. If it connects, print the arrangement

# Step 1: Find all possible arrangements of patches
#  Patches cannot be rotated -- only rearranged.  So, we can just permute the characters in the string.

def permute_patches(patches):
    if len(patches) == 1:
        yield patches
    else:
        for i in range(len(patches)):
            for p in permute_patches(patches[:i] + patches[i+1:]):
                yield patches[i] + p

print(f'## Testing permutations')
cnt = 0
for p in permute_patches("abcdefghijklmnop"):
    print(f' {cnt} - {p}')
    cnt += 1

print(f' {cnt} permutations')
exit()

# Step 2: For each arrangement, check if all pipes connect to each other
# `box` is a list of strings, each string is a row of the box

def check_connections(box):
    for x in range(len(box[0])):
        for y in range(len(box)):
            this_patch = box[y][x]
            # Check against the patch to the right, and the patch below
            if x < len(box[0])-1:
                right_patch = box[y][x+1]
                if not pipe_connections[this_patch] & RIGHT == pipe_connections[right_patch] & LEFT:
                    return False, f"Patch {this_patch} at ({x},{y}) does not connect to patch {right_patch} to the right"
            if y < len(box)-1:
                bottom_patch = box[y+1][x]
                if not pipe_connections[this_patch] & BOTTOM == pipe_connections[bottom_patch] & TOP:
                    return False, f"Patch {this_patch} at ({x},{y}) does not connect to patch {bottom_patch} below"
    return True, "All patches connect"

def print_box(box):
    for row in box:
        for col in row:
            print(col, end='')
        print()

test_box1 = [
    "┌┐",
    "└┘"
]

test_box2 = [
    "┌─┐",
    "│ │",
    "└─┘"
]

test_box3 = [
    "┌─┐",
    "│ ╵",
    "└─┘"
]

test_box4 = [
    "┌─┐",
    "│ │",
    "└╴┘"
]

print_box(test_box1)
print(check_connections(test_box1))
print_box(test_box2)
print(check_connections(test_box2))
print_box(test_box3)
print(check_connections(test_box3))
print_box(test_box4)
print(check_connections(test_box4))
