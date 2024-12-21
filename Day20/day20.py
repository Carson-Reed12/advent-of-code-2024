import networkx as nx
########## SETUP
with open("day20_input.txt", "r") as file:
    lines = file.readlines()
board = [list(line.strip()) for line in lines] #[y][x]

walls = []
open_paths = []

for y in range(len(board)):
    for x in range(len(board[y])):
        if board[y][x] == "#":
            walls.append([y,x])
        elif board[y][x] == ".":
            open_paths.append([y,x])
        elif board[y][x] == "S":
            start_pos = [y,x]
            open_paths.append([y,x])
        elif board[y][x] == "E":
            end_pos = [y,x]
            open_paths.append([y,x])

########## PART 1
G = nx.DiGraph()

print("Building graph...")
nodes = {}
node_count = 0
for path in open_paths:
    nodes[node_count] = path
    G.add_node(node_count)
    node_count += 1

directions = [[1,0], [-1,0], [0,1], [0,-1]]
get_key = lambda a : [i for i in nodes if nodes[i] == a][0]
for node in G.nodes:
    coords = nodes[node]

    for direction in directions:
        new_coords = [coords[0] + direction[0], coords[1] + direction[1]]
        try:
            new_node = get_key(new_coords)
            G.add_edge(node, new_node, weight=1)
        except:
            pass

orig_fastest = nx.shortest_path_length(G, get_key(start_pos), get_key(end_pos), weight="weight")
print(f"DEFAULT FASTEST: {orig_fastest}")

print("Testing wall removal cheats...")
total_cheats = 0
for wall in walls: 
    print(f"\r{wall}", end="", flush=True)
    wall_node = node_count
    nodes[node_count] = wall 
    G.add_node(node_count)
    node_count += 1

    for direction in directions:
        new_coords = [wall[0] + direction[0], wall[1] + direction[1]]
        try:
            new_node = get_key(new_coords)
            G.add_edge(wall_node, new_node, weight=1)
            G.add_edge(new_node, wall_node, weight=1)
        except:
            pass

    cheat_fastest = nx.shortest_path_length(G, get_key(start_pos), get_key(end_pos), weight="weight")
    
    G.remove_node(wall_node)
    del nodes[wall_node]

    if orig_fastest - cheat_fastest >= 100:
        total_cheats += 1

print(f"\nPART 1 TIME SAVING CHEATS: {total_cheats}")

########## PART 2 
def get_close_paths(path):
    close_paths = []

    for y in range(2,21):
        for x in range(y+1):
            if [path[0] + (y-x), path[1] + x] not in close_paths:
                close_paths.append([path[0] + (y-x), path[1] + x])
            if [path[0] - (y-x), path[1] - x] not in close_paths:
                close_paths.append([path[0] - (y-x), path[1] - x])
            if [path[0] + (y-x), path[1] - x] not in close_paths:
                close_paths.append([path[0] + (y-x), path[1] - x])
            if [path[0] - (y-x), path[1] + x] not in close_paths:
                close_paths.append([path[0] - (y-x), path[1] + x])

    return close_paths

key_list = list(nodes.keys())
path_list = list(nodes.values())
get_key = lambda a : key_list[path_list.index(a)]
get_distance = lambda a, b : abs(a[0] - b[0]) + abs (a[1] - b[1])

print("Getting path scores...")
path_scores = {}
for path in open_paths:
        print(f"\r{path}", end="", flush=True)
        path_scores[get_key(path)] = {"from_start": 0, "to_end": 0}
        path_scores[get_key(path)]["from_start"] = nx.shortest_path_length(G, get_key(start_pos), get_key(path), weight="weight")
        path_scores[get_key(path)]["to_end"] = nx.shortest_path_length(G, get_key(path), get_key(end_pos), weight="weight")

print("\nGetting distances...")
total_cheats = 0
for path in [nodes[score_path] for score_path in path_scores.keys() if path_scores[score_path]["from_start"] < orig_fastest]:
    print(f"\r{path}", end="", flush=True)
    path_key = get_key(path)
    for close_path in get_close_paths(path):
        try:
            close_key = get_key(close_path)
        except:
            continue

        new_speed = path_scores[path_key]["from_start"] + get_distance(path, close_path) + path_scores[close_key]["to_end"]
        if orig_fastest - new_speed >= 100:
            total_cheats += 1

print(f"\nPART 2 TIME SAVING CHEATS: {total_cheats}")