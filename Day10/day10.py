import re
############ SETUP
with open("day10_input.txt", "r") as file:
    lines = file.readlines()
board = [list(line.strip()) for line in lines]

############ PART 1
def get_trailheads(board):
    trailheads = []
    for y in range(len(board)):
        row = ''.join(board[y])
        for match in re.finditer("0", row):
            trailheads.append([y, match.start()])
    return trailheads

def get_trails(head, board):
    trailends = []
    directions = [[0,1], [0,-1], [1,0], [-1,0]]
    val = int(board[head[0]][head[1]])

    if val == 9: 
        return head

    next_val = val+1
    for direction in directions:
        next_y = head[0] + direction[0]
        next_x = head[1] + direction[1]
        if 0 <= next_y < len(board) and 0 <= next_x < len(board[0]):
            if next_val == int(board[next_y][next_x]):
                child_trailends = get_trails([head[0] + direction[0], head[1] + direction[1]], board)
                if child_trailends:
                    if isinstance(child_trailends[0], list):
                        for trail in child_trailends:
                            if trail not in trailends:
                                trailends.append(trail)
                    else:
                        trailends.append(child_trailends)

    return trailends

total_score = 0
trailheads = get_trailheads(board)
for trail in trailheads:
    trails = get_trails(trail, board)
    total_score += len(trails)

print(f"PART 1 TRAIL COUNT: {total_score}")

############ PART 2
def get_score(head, board):
    score = 0
    directions = [[0,1], [0,-1], [1,0], [-1,0]]
    val = int(board[head[0]][head[1]])

    if val == 9: 
        return 1

    next_val = val+1
    for direction in directions:
        next_y = head[0] + direction[0]
        next_x = head[1] + direction[1]
        if 0 <= next_y < len(board) and 0 <= next_x < len(board[0]):
            if next_val == int(board[next_y][next_x]):
                score += get_score([next_y, next_x], board)

    return score

total_score = 0
for trail in trailheads:
    trail_score = get_score(trail, board)
    total_score += trail_score

print(f"PART 2 TRAIL SCORE: {total_score}")