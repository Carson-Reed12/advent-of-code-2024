import re

# SETUP AND IMPORTING DATA
with open("day3_input.txt", "r") as file:
    lines = file.readlines()
input_line = ""
for line in lines:
    input_line += line

# MULTI-PART FUNCTIONS
def multiply(multiplier):
    num1 = int(multiplier.split("mul(")[1].split(",")[0])
    num2 = int(multiplier.split(",")[1][:-1])
    return num1*num2

def check_in_range(range, index):
    if index > range[0] and index < range[1]:
        return True
    else:
        return False

# PART 1
multipliers = re.findall("mul\(\d{1,3},\d{1,3}\)", input_line)

total_count = 0
for multiplier in multipliers:
    total_count += multiply(multiplier)

print(f"PART 1 TOTAL COUNT: {total_count}")

# PART 2
active_range = []
do_indices = []
dont_indices = []

for match in re.finditer("do\(\)", input_line):
    do_indices.append(match.start())

for match in re.finditer("don't\(\)", input_line):
    dont_indices.append(match.start())

do_indices.sort()
dont_indices.sort()

print(do_indices)
print(dont_indices)

marker = 0
active = True
for dont in dont_indices:
    if active and dont > marker:
        active_range.append([marker, dont-1])
        active = False
        marker = dont
    
    if not active:
        for do in do_indices:
            if do > marker:
                marker = do
                active = True
                break

multipliers = []
for match in re.finditer("mul\(\d{1,3},\d{1,3}\)", input_line):
    multipliers.append([match.start(), match.group()])

total_count = 0
for multiplier in multipliers:
    index = multiplier[0]

    for range in active_range:
        if check_in_range(range, index):
            total_count += multiply(multiplier[1])
            break

print(f"PART 2 TOTAL COUNT: {total_count}")
