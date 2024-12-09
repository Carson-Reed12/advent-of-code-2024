########### SETUP
with open("day9_input.txt", "r") as file:
    disk_map = file.readlines()[0].strip()

########### PART 1
def get_last_id(extended_map, end):
    for i in range(end, 0, -1):
        if extended_map[i] != ".":
            return i

def decompress_map(disk_map):
    extended_map = []
    id_key = {}

    for i in range(len(disk_map)):
        block_size = int(disk_map[i])

        if i%2 == 0: # file block
            id_key[int(i/2)] = {"indicies": []}
            for _ in range(block_size):
                extended_map.append(int(i/2))
                id_key[int(i/2)]["indicies"].append(len(extended_map)-1)
        else: # free space
            for _ in range(block_size): extended_map.append(".")
    return extended_map, id_key

def reorder_map_pt1(extended_map):
    free_index = extended_map.index(".")
    num_index = get_last_id(extended_map, len(extended_map)-1)

    while free_index < num_index:
        extended_map[free_index] = extended_map[num_index]
        extended_map[num_index] = "."

        free_index = extended_map.index(".")
        num_index = get_last_id(extended_map, len(extended_map)-1)

    return extended_map

def calculate_checksum(ordered_map):
    count = 0
    for i in range(len(ordered_map)):
        if ordered_map[i] != ".":
            count += i*ordered_map[i]
    return count

extended_map, id_key = decompress_map(disk_map)
ordered_map = reorder_map_pt1(extended_map)
checksum = calculate_checksum(ordered_map)
print(f"PART 1 CHECKSUM: {checksum}")

########### PART 2
def get_open_space(needed_space, extended_map, end):
    count = 0
    ids = []

    for i in range(end):
        if extended_map[i] != ".":
            count = 0
            ids.clear()
        else:
            count += 1
            ids.append(i)

            if count == needed_space:
                return ids
            
def reorder_map_pt2(extended_map, id_key):
    for id in reversed(id_key.keys()):
        needed_space = len(id_key[id]["indicies"])

        open_space = get_open_space(needed_space, extended_map, id_key[id]["indicies"][0])
        if open_space:
            for space in open_space:
                extended_map[space] = id
            for index in id_key[id]["indicies"]:
                extended_map[index] = "."
        
    return extended_map

extended_map, id_key = decompress_map(disk_map)
ordered_map = reorder_map_pt2(extended_map, id_key)
checksum = calculate_checksum(ordered_map)
print(f"PART 2 CHECKSUM: {checksum}")