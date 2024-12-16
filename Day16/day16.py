import networkx as nx
########### SETUP
with open("day16_input.txt", "r") as file:
    lines = file.readlines()
board = [line.strip() for line in lines]

########### PART 1 (rewritten from https://github.com/fuglede/adventofcode/blob/master/2024/day16/solutions.py in a way I understand)
G = nx.DiGraph()
nodes = {}

node_count = 0
for i, line in enumerate(board): # i is the index and line is the value (like for i in len(board) but now you just have both). Handy for the future!
    for j, char in enumerate(line):
        if char == "#":
            continue
        if char == "S":
            start_node = (node_count, "E")
        if char == "E":
            end = node_count
        nodes[node_count] = [i, j]
        for dir in "NESW":
            G.add_node((node_count, dir))
        node_count += 1

get_key = lambda a : [i for i in nodes if nodes[i] == a][0]
directions = {"N": [-1,0], "E":[0,1], "S": [1,0], "W": [0,-1]}

for node, dir in G.nodes:
    coord = nodes[node]
    next_coord = [coord[0] + directions[dir][0], coord[1] + directions[dir][1]]

    try: # won't be able to find next node if the key doesn't exist, and if it does, every direction with that node will exist, so no if statement like reference
        next_node = get_key(next_coord)
        G.add_edge((node, dir), (next_node, dir), weight=1)
    except:
        pass
    if dir == "N" or dir == "S":
        G.add_edge((node, dir), (node, "E"), weight=1000)
        G.add_edge((node, dir), (node, "W"), weight=1000)
    elif dir == "E" or dir == "W":
        G.add_edge((node, dir), (node, "N"), weight=1000)
        G.add_edge((node, dir), (node, "S"), weight=1000)

for dir in "NESW": # map the end location with any direction to node "end" with weight zero so that getting to the end in any direction counts as the same goal
    G.add_edge((end, dir), "end", weight=0)

lowest_score = nx.shortest_path_length(G, start_node, "end", weight="weight")
print(f"PART 1 LOWEST SCORE: {lowest_score}")

########### PART 2 (rewritten from https://github.com/fuglede/adventofcode/blob/master/2024/day16/solutions.py in a way I understand)
tiles = []
for path in nx.all_shortest_paths(G, start_node, "end", weight="weight"):
    for tile in path:
        if tile[0] not in tiles:
            tiles.append(tile[0])
print(f"PART 2 NUMBER OF SITTING TILES: {len(tiles)-1}")