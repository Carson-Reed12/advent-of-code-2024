import itertools
import copy
########## SETUP
with open("day21_input.txt", "r") as file:
    codes = [line.strip() for line in file.readlines()]

########## PART 1
KEYPAD = {"7": [-1, -1], "8": [-1, 0], "9": [-1, 1], # [y, x]
          "4": [0, -1],  "5": [0, 0], "6": [0, 1],
          "1": [1, -1],  "2": [1, 0], "3": [1, 1],
                       "0": [2, 0], "A": [2, 1]}

DIRECTIONAL = {               "^": [-1, 0], "A": [-1, 1],
                "<": [0, -1], "v": [0, 0], ">": [0, 1]}

get_distance = lambda a, b : [b[0] - a[0], b[1] - a[1]]
def code_to_remote(code): # can probably cache stuff for part 2 if it requires optimizing
    head = KEYPAD["A"]
    sequence = ""

    for key in code:
        distance = get_distance(head, KEYPAD[key])
        unordered_sequence = ""
        for _ in range(abs(distance[0])):
            unordered_sequence += "^" if distance[0] < 0 else "v"
        for _ in range(abs(distance[1])):
            unordered_sequence += "<" if distance[1] < 0 else ">"

        sequence += order_seq(unordered_sequence, head, "keypad") + "A"
        head = KEYPAD[key]

    return sequence

def sequence_to_remote(old_sequence, key = None):
    if key:
        head = DIRECTIONAL[key]
    else:
        head = DIRECTIONAL["A"]
    new_sequence = ""

    for button in old_sequence:
        distance = get_distance(head, DIRECTIONAL[button])
        unordered_sequence = ""
        for _ in range(abs(distance[0])):
            unordered_sequence += "^" if distance[0] < 0 else "v"
        for _ in range(abs(distance[1])):
            unordered_sequence += "<" if distance[1] < 0 else ">"

        new_sequence += order_seq(unordered_sequence, head, "directional") + "A"
        head = DIRECTIONAL[button]

    return new_sequence

def validate_seq(sequence, head, pad_type):
    directions = {"^": [-1, 0], "<": [0, -1], "v": [1, 0], ">": [0, 1]}
    error_key = [2, -1] if pad_type == "keypad" else [-1, -1]
    for key in sequence:
        head = [head[0] + directions[key][0], head[1] + directions[key][1]]
        if head == error_key:
            return False
    return True

order_cache = {}
def order_seq(sequence, head, pad_type): # best sequences are < followed by ^ or v followed by A or > (unless invalid)
    try:
        return order_cache[sequence]
    except:

        get_distance = lambda a, b : abs(a[0] - b[0]) + abs(a[1] - b[1])
        min_distance = 999
        min_sequence = ""

        for permutation in list(itertools.permutations(sequence)):
            if validate_seq(permutation, head, pad_type):
                distance = 0
                permutation += ("A",)
                for i in range(len(permutation)-1) :
                    distance += get_distance(DIRECTIONAL[permutation[i]], DIRECTIONAL[permutation[i+1]])

                if distance < min_distance:
                    min_distance = distance
                    min_sequence = ''.join(permutation[:-1])

        order_cache[sequence] = min_sequence
        return min_sequence

total_complexity = 0
for code in codes:
    val = int(code.split("A")[0])
    total_complexity += val * len(sequence_to_remote(sequence_to_remote(code_to_remote(code))))

print(f"PART 1 TOTAL COMPLEXITY: {total_complexity}")

########## PART 2 https://www.reddit.com/r/adventofcode/comments/1hj8380/2024_day_21_part_2_i_need_help_three_days_in_row/
    
button_costs = {}
button_costs2 = {}
for button1 in "<^>vA":
    for button2 in "<^>vA":
        button_costs[button1+button2] = len(sequence_to_remote(button2, button1))
        button_costs2[button1+button2] = 0
def cycle_costs(): 
    global button_costs
    global button_costs2
    button_costs2["AA"] = button_costs["AA"] + 1
    button_costs2["A^"] = button_costs["A<"] + button_costs["<A"]
    button_costs2["A<"] = button_costs["A<"] + button_costs["<v"] + button_costs["v<"] + button_costs["<A"]
    button_costs2["Av"] = button_costs["A<"] + button_costs["<v"] + button_costs["vA"]
    button_costs2["A>"] = button_costs["Av"] + button_costs["vA"]

    button_costs2["^A"] = button_costs["A>"] + button_costs[">A"]
    button_costs2["^^"] = button_costs["^^"] + 1
    button_costs2["^<"] = button_costs["Av"] + button_costs["v<"] + button_costs["<A"]
    button_costs2["^v"] = button_costs["Av"] + button_costs["vA"]
    button_costs2["^>"] = button_costs["Av"] + button_costs["v>"] + button_costs[">A"]

    button_costs2["<A"] = button_costs["A>"] + button_costs[">^"] + button_costs["^>"] + button_costs[">A"]
    button_costs2["<^"] = button_costs["A>"] + button_costs[">^"] + button_costs["^A"]
    button_costs2["<<"] = button_costs["<<"] + 1
    button_costs2["<v"] = button_costs["A>"] + button_costs[">A"]
    button_costs2["<>"] = button_costs["A>"] + button_costs[">>"] + button_costs[">A"]

    button_costs2["vA"] = button_costs["A^"] + button_costs["^>"] + button_costs[">A"]
    button_costs2["v^"] = button_costs["A^"] + button_costs["^A"]
    button_costs2["v<"] = button_costs["A<"] + button_costs["<A"]
    button_costs2["vv"] = button_costs2["vv"] + 1
    button_costs2["v>"] = button_costs["A>"] + button_costs[">A"]

    button_costs2[">A"] = button_costs["A^"] + button_costs["^A"]
    button_costs2[">^"] = button_costs["A<"] + button_costs["<^"] + button_costs["^A"]
    button_costs2["><"] = button_costs["A<"] + button_costs["<<"] + button_costs["<A"]
    button_costs2[">v"] = button_costs["A<"] + button_costs["<A"]
    button_costs2[">>"] = button_costs2[">>"] + 1

    button_costs = copy.deepcopy(button_costs2)


code = "029A"
base1 = code_to_remote(code)
base1 = "A"+base1
length = 0
cycle_costs()
for i in range(len(base1)-1):
    length += button_costs[base1[i]+base1[i+1]]
print(length)
# print(sequence_to_remote("<", "^"))


# total_complexity = 0
# for code in codes:
#     print(code)
#     val = int(code.split("A")[0])
#     code_sequence = code_to_remote(code)
#     for i in range(25):
#         print(i)
#         code_sequence = sequence_to_remote(code_sequence)
#     total_complexity += val * len(code_sequence)

# print(f"PART 2 TOTAL COMPLEXITY: {total_complexity}")