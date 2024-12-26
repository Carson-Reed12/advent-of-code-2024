########### SETUP
with open("day25_input.txt", "r") as file:
    lines = file.readlines()

########### PART 1
locks = []
keys = []

lock_state = False
key_state = False
distances = [-1,-1,-1,-1,-1]
for i, line in enumerate(lines):
    if all(char == "#" for char in line.strip()) and not lock_state and not key_state:
        lock_state = True
    elif all(char == "." for char in line.strip()) and not lock_state and not key_state:
        key_state = True

    for j, char in enumerate(line.strip()):
        if char == "#":
            distances[j] += 1
    
    if line == "\n" or i == len(lines) - 1:
        locks.append(distances) if lock_state else keys.append(distances)
        lock_state = False
        key_state = False
        distances = [-1,-1,-1,-1,-1]

total_pairs = 0
for lock in locks:
    for key in keys:
        valid_lock = True
        for pin_k, pin_l in zip(key, lock):
            if pin_k + pin_l > 5:
                valid_lock = False
                break
        if valid_lock:
            total_pairs += 1

print(f"PART 1 TOTAL PAIRS: {total_pairs}")

########### PART 2