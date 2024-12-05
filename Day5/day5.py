############## SETUP
with open("day5_input.txt", "r") as file:
    lines = file.readlines()

rules = []
updates = []
for line in lines:
    if "|" in line:
        vals = line.split("|")
        rules.append([int(val) for val in vals])
    if "," in line:
        updates.append([[int(val) for val in line.strip().split(",")], True])

############## FUNCTIONS
def check_update(rules, update_vals):
    for rule in rules:
        num1 = rule[0]
        num2 = rule[1]

        try:
            index1 = update_vals.index(num1)
        except:
            index1 = -1
        try:
            index2 = update_vals.index(num2)
        except:
            index2 = -1

        if index1 != -1 and index2 != -1:
            if index2 < index1:
                return [False, index1, index2]
    return [True]

def get_middle_page(update_vals):
    return update_vals[int(len(update_vals)/2)]
    
############## PART 1
for update in updates:
    if not check_update(rules, update[0])[0]:
        update[1] = False


total_count = 0
for update in updates:
    if update[1]:
        total_count += get_middle_page(update[0])

print(f"PART 1 TOTAL COUNT: {total_count}")

############## PART 2
bad_updates = []
for update in updates:
    if not update[1]:
        bad_updates.append(update)

total_count = 0
for update in bad_updates:
    valid = False

    while not valid:
        valid = True
 
        result = check_update(rules, update[0])
        if not result[0]:
            valid = False

            index1 = result[1]
            index2 = result[2]
            buffer = update[0][index1]

            update[0][index1] = update[0][index2]
            update[0][index2] = buffer
        else:
            total_count += get_middle_page(update[0])

print(f"PART 2 TOTAL COUNT: {total_count}")

