import copy
################ SETUP
with open("day6_input.txt", "r") as file:
    lines = file.readlines()

board = [list(line) for line in lines]
dir_map = {"U": [-1,0], "R": [0,1], "D": [1,0], "L": [0, -1]}
SIZE = len(board[0])

################ PART 1

def walkthrough_map(start, board):
    locations = []
    dir_locations = []
    guard_pos = start
    valid = True
    directions = "URDL"
    turns = 0

    while valid:
        if guard_pos not in locations:
            locations.append(guard_pos)
        if [guard_pos, directions[turns%4]] not in dir_locations:
            dir_locations.append([guard_pos, directions[turns%4]])
        else:
            return locations, True

        next_pos_y = guard_pos[0] + dir_map[directions[turns%4]][0]
        next_pos_x = guard_pos[1] + dir_map[directions[turns%4]][1]
        if not ((0 <= next_pos_y < SIZE -1) and (0 <= next_pos_x < SIZE - 1)):
            valid = False
        elif board[next_pos_y][next_pos_x] == "#":
            turns += 1
        else:
            guard_pos = [next_pos_y, next_pos_x]

    return locations, False


for y in range(SIZE):
    try:
        start = [y, board[y].index("^")]
    except:
        pass

locations = walkthrough_map(start, board)

print(f"TOTAL LOCATIONS: {len(locations)}")

################ PART 2
loop_count = 0
for y in range(SIZE - 1):
    for x in range(SIZE - 1):
        if board[y][x] == "#" or board[y][x] == "^" or [y,x] not in locations[0]:
            continue
        print(f"Testing obstacle placement at [{y}, {x}]...")
        new_board = copy.deepcopy(board)
        new_board[y][x] = "#"

        returned_locations, loop = walkthrough_map(start, new_board)

        if loop:
            loop_count += 1

print(f"LOOP COUNT: {loop_count}")