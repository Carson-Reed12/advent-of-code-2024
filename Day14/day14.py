############ SETUP
with open("day14_input.txt", "r") as file:
    lines = file.readlines()

WIDTH = 100 # subtracted 1 from 101 so I don't have to do "WIDTH-1" for array spacing
HEIGHT = 102 # subtracted 1 from 103 so I don't have to do "HEIGHT-1" for array spacing

############ PART 1
class Robot():
    def __init__(self, pos, vector):
        self.pos = pos
        self.vector = vector

    def move(self):
        if self.pos[0] + self.vector[0] > WIDTH:
            self.pos[0] = (self.pos[0] + self.vector[0]) - WIDTH - 1
        elif self.pos[0] + self.vector[0] < 0:
            self.pos[0] = WIDTH + (self.pos[0] + self.vector[0]) + 1
        else:
            self.pos[0] += self.vector[0]

        if self.pos[1] + self.vector[1] > HEIGHT:
            self.pos[1] = (self.pos[1] + self.vector[1]) - HEIGHT - 1
        elif self.pos[1] + self.vector[1] < 0:
            self.pos[1] = HEIGHT + (self.pos[1] + self.vector[1]) + 1
        else:
            self.pos[1] += self.vector[1]

    def quadrant(self):
        if self.pos[0] == WIDTH/2 or self.pos[1] == HEIGHT/2:
            return "N/A"
        elif self.pos[0] < WIDTH/2 and self.pos[1] < HEIGHT/2:
            return "Q1"
        elif self.pos[0] > WIDTH/2 and self.pos[1] < HEIGHT/2:
            return "Q2"
        elif self.pos[0] < WIDTH/2 and self.pos[1] > HEIGHT/2:
            return "Q3"
        elif self.pos[0] > WIDTH/2 and self.pos[1] > HEIGHT/2:
            return "Q4"

def initialize_robots():
    robots = []
    for line in lines:
        pos = [int(line.strip().split(" ")[0][2:].split(",")[0]), int(line.strip().split(" ")[0][2:].split(",")[1])]
        vector = [int(line.strip().split(" ")[1][2:].split(",")[0]), int(line.strip().split(" ")[1][2:].split(",")[1])]

        robots.append(Robot(pos, vector))
    return robots

robots = initialize_robots()
for robot in robots:
    for _ in range(100):
        robot.move()

quadrant_count = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0, "N/A": 0}
for robot in robots:
    quadrant_count[robot.quadrant()] += 1

safety_factor = 1
for quadrant in quadrant_count.keys():
    if quadrant != "N/A":
        safety_factor *= quadrant_count[quadrant]
print(f"PART 1 SAFETY FACTOR: {safety_factor}")

############ PART 2 (6493 moves)
def initialize_board():
    board = [['.' for _ in range(WIDTH+1)] for _ in range(HEIGHT+1)]
    return board

def display_bots(robots):
    board = initialize_board()

    for robot in robots:
        board[robot.pos[1]][robot.pos[0]] = "#"

    for line in board:
        print(''.join(line))

robots = initialize_robots()
# print("INITIAL STATE") Found by noticing pattern of localized points every 101 moves from 29 and just looking manually
# display_bots(robots)
# print("--------------\n\n")
# moves = 0
# t_count = 29
# while True:
#     for robot in robots:
#         robot.move()
#     moves += 1
    
#     quadrant_count = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0, "N/A": 0}
#     for robot in robots:
#         quadrant_count[robot.quadrant()] += 1

#     if moves == t_count:
#         display_bots(robots)
#         print(f"MOVES: {moves}")
#         t_count += 101
#         input()

for _ in range(6493):
    for robot in robots:
        robot.move()
display_bots(robots)
print(f"PART 2 MOVES: 6493")
