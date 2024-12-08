import re
import copy
############ SETUP
with open("day8_input.txt", "r") as file:
    lines = file.readlines()

board = [list(line.strip()) for line in lines]
refresh_board = copy.deepcopy(board)

############ PART 1
uniq_chars = []
for y in range(len(board)):
    for x in range(len(board[0])):
        if board[y][x] not in uniq_chars and board[y][x] != ".":
            uniq_chars.append(board[y][x])

locations = {char: [] for char in uniq_chars}
for y in range(len(board)):
    for char in uniq_chars:
        row = ''.join(board[y])
        for match in re.finditer(char, row):
            locations[char].append([y, match.start()])

for char in locations.keys():
    for node1 in locations[char]:
        for node2 in locations[char]:
            if node1 != node2:
                slope_y = node1[0] - node2[0]
                slope_x = node1[1] - node2[1]

                if 0 <= node1[0] + slope_y < len(board) and 0 <= node1[1] + slope_x < len(board[0]):
                    board[node1[0] + slope_y][node1[1] + slope_x] = "#"
                if 0 <= node2[0] - slope_y < len(board) and 0 <= node2[1] - slope_x < len(board[0]):
                    board[node2[0] - slope_y][node2[1] - slope_x] = "#"

total_count = 0
for y in range(len(board)):
    for x in range(len(board[0])):
        if board[y][x] == "#":
            total_count += 1
print(f"PART 1 TOTAL COUNT: {total_count}")

############ PART 2
board = refresh_board
for char in locations.keys():
    for node1 in locations[char]:
        for node2 in locations[char]:
            if node1 != node2:
                slope_y = node1[0] - node2[0]
                slope_x = node1[1] - node2[1]
                valid = True
                count = 1

                while valid:
                    if 0 <= node1[0] + slope_y*count < len(board) and 0 <= node1[1] + slope_x*count < len(board[0]):
                        board[node1[0] + slope_y*count][node1[1] + slope_x*count] = "#"
                        count +=1
                    else:
                        valid = False
                        count = 0

                valid = True
                while valid:
                    if 0 <= node2[0] - slope_y*count < len(board) and 0 <= node2[1] - slope_x*count < len(board[0]):
                        board[node2[0] - slope_y*count][node2[1] - slope_x*count] = "#"
                        count += 1
                    else:
                        valid = False
                        count = 0

for char in locations.keys():
    if len(locations[char]) > 1:
        for location in locations[char]:
            board[location[0]][location[1]] = "#"

total_count = 0
for y in range(len(board)):
    for x in range(len(board[0])):
        if board[y][x] == "#":
            total_count += 1
print(f"PART 2 TOTAL COUNT: {total_count}")