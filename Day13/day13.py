import re
############ SETUP
with open("day13_input.txt", "r") as file:
    lines = file.readlines()
machines = {} #[x,y]: {A: [x,y], B:[x,y]}
machine = []
count = 0
for line in lines:
    if "Button A:" in line or "Button B:" in line:
        machine.append([int(re.search("X\+\d+", line.strip()).group()[2:]), int(re.search("Y\+\d+", line.strip()).group()[2:])])
    elif "Prize:" in line:
        machine.append([int(re.search("X=\d+", line.strip()).group()[2:]), int(re.search("Y=\d+", line.strip()).group()[2:])])
        machines[count] = {"prize": machine[2], "A": machine[0], "B": machine[1]}
        count += 1
        machine.clear()

############ PART 1
for id in machines.keys():
    least_tokens = 9999999999
    prize = machines[id]["prize"]
    button_a = machines[id]["A"]
    button_b =  machines[id]["B"]

    for i in range(100):
        x_a = i * button_a[0]
        y_a = i * button_a[1]
        for j in range(100):
            tokens = ((i*3) + j)
            x_total = x_a + (j * button_b[0])
            y_total = y_a + (j * button_b[1])

            if [x_total,y_total] == prize and tokens < least_tokens:
                least_tokens = tokens
    if least_tokens == 9999999999:
        machines[id]["least_tokens"] = 0
    else:
        machines[id]["least_tokens"] = least_tokens

total_tokens = 0
for id in machines.keys():
    total_tokens += machines[id]["least_tokens"]
print(f"PART 1 TOTAL TOKENS: {total_tokens}")

############ PART 2
for id in machines.keys():
    machines[id]["least_tokens"] = 0

for id in machines.keys():
    prize = machines[id]["prize"]
    new_prize = [10000000000000 + prize[0], 10000000000000 + prize[1]]
    button_a = machines[id]["A"]
    button_b =  machines[id]["B"]

    b_pushes = ((button_a[0]*new_prize[1]) - (button_a[1]*new_prize[0]))/((button_a[0]*button_b[1]) - (button_a[1]*button_b[0]))
    a_pushes = (new_prize[0] - (b_pushes*button_b[0]))/button_a[0]

    if a_pushes.is_integer() and b_pushes.is_integer():
        machines[id]["least_tokens"] = (a_pushes*3) + b_pushes

total_tokens = 0
for id in machines.keys():
    total_tokens += machines[id]["least_tokens"]
print(f"PART 2 TOTAL TOKENS: {int(total_tokens)}")