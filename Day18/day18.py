import networkx as nx
############ SETUP
with open("day18_input.txt", "r") as file:
    lines = file.readlines()
bytes = [[int(item.strip().split(",")[0]), int(item.strip().split(",")[1])] for item in lines]

############ PART 1
G = nx.DiGraph()
nodes = {}
node_count = 0
SIZE = 71

print("Building graph...")
for x in range(SIZE):
    for y in range(SIZE):
        if [x,y] not in bytes[:1024]:
            if x == 0 and y == 0:
                start_node = node_count
            if x == SIZE - 1 and y == SIZE - 1:
                end_node = node_count
            G.add_node(node_count)
            nodes[node_count] = [x,y]
            node_count += 1

directions = [[0,1], [0,-1], [-1,0], [1,0]]
get_key = lambda a : [i for i in nodes if nodes[i] == a][0]
for node in G.nodes:
    coord = nodes[node]
    for direction in directions:
        new_coord = [coord[0] + direction[0], coord[1] + direction[1]]
        try:
            next_node = get_key(new_coord)
            G.add_edge(node, next_node, weight=1)
        except:
            pass

minimum_steps = nx.shortest_path_length(G, start_node, end_node, weight="weight")
print(f"PART 1 MINIMUM STEPS: {minimum_steps}")

############ PART 2
for byte in bytes[1024:]:
    node = get_key(byte)
    print(f"\rRemoving node {node} at byte {byte}...", end="", flush=True)
    G.remove_node(node)

    try:
        minimum_steps = nx.shortest_path_length(G, start_node, end_node, weight="weight")
    except:
        print(f"\nPART 2 BREAKING NODE: {node} - {byte}")
        break