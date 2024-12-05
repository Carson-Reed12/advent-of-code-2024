import re

with open("day4_input.txt", "r") as file:
    lines = file.readlines()

############# PART 1
char_array = [list(line.strip()) for line in lines] # [y][x]
SIZE = len(char_array)

total_count = 0
# LEFT TO RIGHT:
for line in lines:
    total_count += len(re.findall("XMAS", line.strip()))

# RIGHT TO LEFT:
for line in lines:
    total_count += len(re.findall("XMAS", line.strip()[::-1]))

# TOP TO BOTTOM:
t2b_strings = []
for x in range(SIZE):
    col = ""
    for y in range(SIZE):
        col += char_array[y][x]
    t2b_strings.append(col)

for line in t2b_strings:
    total_count += len(re.findall("XMAS", line.strip()))

# BOTTOM TO TOP:
for line in t2b_strings:
    total_count += len(re.findall("XMAS", line.strip()[::-1]))

# TL 2 BR DIAGONAL (locations saved for use in PART 2):
tl2br_strings = []
for x in range(SIZE):
    diag = ""
    first = True
    location = []

    for step in range(SIZE-x):
        diag += char_array[step][step+x]

        if first:
            location = [step, step+x]
            first = False

    tl2br_strings.append([diag, location])

for y in range(SIZE):
    diag = ""
    first = True
    location = []

    for step in range(SIZE-y):
        diag += char_array[step+y][step]
        if first:
            location = [step+y, step]
            first = False

    if [diag, location] not in tl2br_strings:
        tl2br_strings.append([diag, location])

for line in tl2br_strings:
    total_count += len(re.findall("XMAS", line[0].strip()))

# BR 2 TL DIAGONAL:
for line in tl2br_strings:
    total_count += len(re.findall("XMAS", line[0].strip()[::-1]))

# TR 2 BL DIAGONAL (locations saved for use in PART 2):
rev_char_arary = [line[::-1] for line in char_array]
tr2bl_strings = []
for x in range(SIZE):
    diag = ""
    first = True
    location = []
    
    for step in range(SIZE-x):
        diag += rev_char_arary[step][step+x]
        if first:
            location = [step, step+x]
            first = False

    tr2bl_strings.append([diag, location])

for y in range(SIZE):
    diag = ""
    first = True
    location = []
    
    for step in range(SIZE-y):
        diag += rev_char_arary[step+y][step]
        if first:
            location = [step+y, step]
            first = False

    if [diag, location] not in tr2bl_strings:
        tr2bl_strings.append([diag, location])

for line in tr2bl_strings:
    total_count += len(re.findall("XMAS", line[0].strip()))

# BR 2 TL DIAGONAL:
for line in tr2bl_strings:
    total_count += len(re.findall("XMAS", line[0].strip()[::-1]))

print(f"PART 1 TOTAL COUNT: {total_count}")


########### PART 2

tl2br_mas = []
for line in tl2br_strings:
    for match in re.finditer("MAS", line[0]):
        start_y = line[1][0]
        start_x = line[1][1]
        offset = match.start()+1

        tl2br_mas.append([start_y+offset, start_x+offset])

br2tl_mas = []
for line in tl2br_strings:
    for match in re.finditer("MAS", line[0][::-1]):
        start_y = line[1][0]
        start_x = line[1][1]
        offset = (len(line[0]) - (match.start()+1)) - 1

        br2tl_mas.append([start_y+offset, start_x+offset])

tr2bl_mas = []
for line in tr2bl_strings:
    for match in re.finditer("MAS", line[0]):
        start_y = line[1][0]
        start_x = (SIZE - 1) - line[1][1]
        offset = match.start()+1

        tr2bl_mas.append([start_y+offset, start_x-offset])

bl2tr_mas = []
for line in tr2bl_strings:
    for match in re.finditer("MAS", line[0][::-1]):
        start_y = line[1][0]
        start_x = (SIZE - 1) - line[1][1]
        offset = (len(line[0]) - (match.start()+1)) - 1

        bl2tr_mas.append([start_y+offset, start_x-offset])


total_count = 0
for mas in tl2br_mas:
    if mas in tr2bl_mas or mas in bl2tr_mas:
        total_count += 1

for mas in br2tl_mas:
    if mas in tr2bl_mas or mas in bl2tr_mas:
        total_count += 1

print(f"PART 2 TOTAL COUNT: {total_count}")