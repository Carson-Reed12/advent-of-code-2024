########### SETUP
with open("day12_input.txt", "r") as file:
    lines = file.readlines()
board = [list(line.strip()) for line in lines]

########### PART 1
region = []
regions = []
used = []
SIZE = len(board)

def get_region(head, letter):
    global region

    if not(0 <= head[0] < SIZE and 0 <= head[1] < SIZE):
        return
    current_letter = board[head[0]][head[1]]
    directions = [[0,1], [0,-1], [1,0], [-1,0]]

    if letter == current_letter:
        if head not in region:
            region.append(head)
            for direction in directions:
                get_region([head[0] + direction[0], head[1] + direction[1]], letter)
    else:
        return
    
def get_perimeter_pt1(region):
    perimeter = 0
    directions = [[0,1], [0,-1], [1,0], [-1,0]]

    for plot in region:
        y_1 = plot[0]
        x_1 = plot[1]
        score = 4

        for direction in directions:
            if [y_1 + direction[0], x_1 + direction[1]] in region:
                score -= 1
        perimeter += score
    return perimeter

for y in range(SIZE):
    for x in range(SIZE):
        if [y,x] not in used:
            region = []
            letter = board[y][x]
            get_region([y,x], letter)
            used.extend(region)
            regions.append(region)

total_count = 0
for region in regions:
    total_count += len(region) * get_perimeter_pt1(region)
print(f"PART 1 TOTAL PRICE: {total_count}")

########### PART 2
def get_perimeter_pt2(region):
    walls = {"R": [], "L": [], "U": [], "D": []}
    directions = {"R": [0,1], "L": [0,-1], "U": [-1,0], "D": [1,0]}
    score = 0

    for plot in region:
        y_1 = plot[0]
        x_1 = plot[1]

        for direction in "RLUD":
            if [y_1 + directions[direction][0], x_1 + directions[direction][1]] not in region:
                walls[direction].append([y_1 + directions[direction][0], x_1 + directions[direction][1]])  

    for direction in "RLUD":
        used_walls = []
        if direction == "R" or direction == "L":
            offset = directions["U"]
        else:
            offset = directions["L"]

        for wall in walls[direction]:
            if wall not in used_walls:
                used_walls.append(wall)
                new_wall = [wall[0] + offset[0], wall[1] + offset[1]]  
                while new_wall in walls[direction]:
                    used_walls.append(new_wall)
                    new_wall = [new_wall[0] + offset[0], new_wall[1] + offset[1]]
                new_wall = [wall[0] + (offset[0] * -1), wall[1] + (offset[1] * -1)]   
                while new_wall in walls[direction]:
                    used_walls.append(new_wall)
                    new_wall = [new_wall[0] + (offset[0] * -1), new_wall[1] + (offset[1] * -1)]
                score += 1      

    return score

total_count = 0
for region in regions:
    total_count += len(region) * get_perimeter_pt2(region)
print(f"PART 2 TOTAL PRICE: {total_count}")
