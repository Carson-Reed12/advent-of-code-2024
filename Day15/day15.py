import re
######## SETUP
with open("day15_input.txt", "r") as file:
    lines = file.readlines()

box_poses = []
moves = []
walls = []
for y in range(len(lines)): # back to [y,x]
    for match in re.finditer("#", lines[y]):
        walls.append([y, match.start()])
    for match in re.finditer("O", lines[y]):
        box_poses.append([y, match.start()])
    if "@" in lines[y]:
        start_pos = [y, lines[y].index("@")]
    if "<" in lines[y] or "^" in lines[y] or ">" in lines[y] or "v" in lines[y]:
        moves.extend(list(lines[y].strip()))

SIZE = len(lines[0].strip())

######## PART 1
class Robot():
    def __init__(self, pos, moves):
        self.pos = pos
        self.moves = moves
        self.move_marker = 0

    def next_move(self):
        return self.moves[self.move_marker]
    
    def move(self):
        directions = {">": [0,1], "v": [1,0], "<": [0,-1], "^": [-1,0]}
        direction = self.next_move()

        self.pos[0] += directions[direction][0]
        self.pos[1] += directions[direction][1]
        self.move_marker += 1

    def anticipated_move(self):
        directions = {">": [0,1], "v": [1,0], "<": [0,-1], "^": [-1,0]}
        direction = self.next_move()
        return [self.pos[0] + directions[direction][0], self.pos[1] + directions[direction][1]]

    def skip_move(self):
        self.move_marker += 1

class Box():
    def __init__(self, pos):
        self.pos = pos

    def move(self, direction):
        directions = {">": [0,1], "v": [1,0], "<": [0,-1], "^": [-1,0]}
        self.pos[0] += directions[direction][0]
        self.pos[1] += directions[direction][1]

    def anticipated_move(self, move):
        directions = {">": [0,1], "v": [1,0], "<": [0,-1], "^": [-1,0]}
        return [self.pos[0] + directions[move][0], self.pos[1] + directions[move][1]]

def get_affected_boxes(walls, robot, boxes):
    anticipated_move = robot.anticipated_move()
    next_move = robot.next_move()
    affected_boxes = []
    check_boxes = []

    for box in boxes:
        if box.pos == anticipated_move:
            affected_boxes.append(box)
            check_boxes.append(box)
            break

    while check_boxes:
        checked_box = check_boxes.pop()
        anticipated_move = checked_box.anticipated_move(next_move)     

        if anticipated_move in walls:
            return -1
        for box in boxes:
            if checked_box != box:
                if anticipated_move == box.pos and box not in affected_boxes:
                    check_boxes.append(box)
                    affected_boxes.append(box)

    return affected_boxes

def initialize_board(walls, robot, boxes):
    board = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
    for wall in walls:
        board[wall[0]][wall[1]] = "#"
    board[robot.pos[0]][robot.pos[1]] = "@"
    for box in boxes:
        board[box.pos[0]][box.pos[1]] = "O"

    return board

def display_board(walls, robot, boxes):
    board = initialize_board(walls, robot, boxes)
    for line in board:
        print(''.join(line))

robot = Robot(start_pos, moves)
boxes = []
for box_pos in box_poses:
    boxes.append(Box(box_pos))

print("INITIAL STATE")
initial_board = initialize_board(walls, robot, boxes)
display_board(walls, robot, boxes)
for _ in robot.moves:
    anticipated_move = robot.anticipated_move()
    if anticipated_move in walls: # skip move if robot would move into wall
        robot.skip_move()
    elif anticipated_move not in [box.pos for box in boxes]: # make move if not moving into a box
        robot.move()
    else:
        affected_boxes = get_affected_boxes(walls, robot, boxes)
        if affected_boxes == -1: # if robot pushes boxes into a wall
            robot.skip_move()
        else: # make boxes and robot move
            next_move = robot.next_move()
            for box in affected_boxes:
                box.move(next_move)
            robot.move()

print("FINAL STATE")
display_board(walls, robot, boxes)

total_sum = 0
for box in boxes:
    total_sum += (box.pos[0]*100) + box.pos[1]
print(f"PART 1 TOTAL SUM: {total_sum}")

######## PART 2
class BigBox():
    def __init__(self, pos):
        self.left_pos = pos
        self.right_pos = [pos[0], pos[1] + 1]

    def move(self, direction):
        directions = {">": [0,1], "v": [1,0], "<": [0,-1], "^": [-1,0]}
        self.left_pos[0] += directions[direction][0]
        self.left_pos[1] += directions[direction][1]
        self.right_pos[0] += directions[direction][0]
        self.right_pos[1] += directions[direction][1]

    def batched_pos(self):
        return [self.left_pos, self.right_pos]
    
    def anticipated_move(self, move):
        directions = {">": [0,1], "v": [1,0], "<": [0,-1], "^": [-1,0]}
        return [self.left_pos[0] + directions[move][0], self.left_pos[1] + directions[move][1]], [self.right_pos[0] + directions[move][0], self.right_pos[1] + directions[move][1]]
    
def convert_to_wide_board(board):
    wide_board = []
    for y in range(len(board)):
        line = []
        for x in range(len(board[y])):
            if board[y][x] == "#":
                line.extend(["#", "#"])
            elif board[y][x] == "O":
                line.extend(["[", "]"])
            elif board[y][x] == "@":
                line.extend(["@", "."])
            else:
                line.extend([".", "."])
        wide_board.append(line)
    return wide_board

def initialize_wide_board(walls, robot, boxes):
    board = [['.' for _ in range(SIZE*2)] for _ in range(SIZE)]
    for wall in walls:
        board[wall[0]][wall[1]] = "#"
    board[robot.pos[0]][robot.pos[1]] = "@"
    for box in boxes:
        board[box.left_pos[0]][box.left_pos[1]] = "["
        board[box.right_pos[0]][box.right_pos[1]] = "]"

    return board

def display_wide_board(walls, robot, boxes):
    board = initialize_wide_board(walls, robot, boxes)
    for line in board:
        print(''.join(line))

def get_affected_big_boxes(walls, robot, big_boxes):
    anticipated_move = robot.anticipated_move()
    next_move = robot.next_move()
    affected_boxes = []
    check_boxes = []

    for box in big_boxes:
        if anticipated_move in box.batched_pos():
            affected_boxes.append(box)
            check_boxes.append(box)
            break

    while check_boxes:
        checked_box = check_boxes.pop()
        anticipated_left_move, anticipated_right_move = checked_box.anticipated_move(next_move)

        if anticipated_left_move in walls or anticipated_right_move in walls:
            return -1
        for big_box in big_boxes:
            if checked_box != big_box:
                if (anticipated_left_move in big_box.batched_pos() or anticipated_right_move in big_box.batched_pos()) and big_box not in affected_boxes:
                    check_boxes.append(big_box)
                    affected_boxes.append(big_box)

    return affected_boxes


initial_wide_board = convert_to_wide_board(initial_board)
box_poses = []
walls = []
for y in range(len(initial_wide_board)): # back to [y,x]
    line = ''.join(initial_wide_board[y])
    for match in re.finditer("#", line):
        walls.append([y, match.start()])
    for match in re.finditer("\[", line):
        box_poses.append([y, match.start()])
    if "@" in line:
        start_pos = [y, initial_wide_board[y].index("@")]

robot = Robot(start_pos, moves)
big_boxes = []
for box_pos in box_poses:
    big_boxes.append(BigBox(box_pos))

print("INITIAL STATE")
display_wide_board(walls, robot, big_boxes)
for _ in robot.moves:
    anticipated_move = robot.anticipated_move()
    if anticipated_move in walls: # skip move if robot would move into wall
        robot.skip_move()
    elif anticipated_move not in [box.left_pos for box in big_boxes] and anticipated_move not in [box.right_pos for box in big_boxes]: # make move if not moving into a box
        robot.move()
    else:
        affected_boxes = get_affected_big_boxes(walls, robot, big_boxes)
        if affected_boxes == -1: # if robot pushes boxes into a wall
            robot.skip_move()
        else: # make boxes and robot move
            next_move = robot.next_move()
            for big_box in affected_boxes:
                big_box.move(next_move)
            robot.move()

print("FINAL STATE")
display_wide_board(walls, robot, big_boxes)

total_sum = 0
for big_box in big_boxes:
    total_sum += (big_box.left_pos[0]*100) + big_box.left_pos[1]
print(f"PART 2 TOTAL SUM: {total_sum}")