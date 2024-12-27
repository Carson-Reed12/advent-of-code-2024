import networkx as nx
########### SETUP
with open("day23_input.txt", "r") as file:
    connections = file.readlines()

connections = [connection.strip() for connection in connections]

########### PART 1
# adjacent = {}
# for connection in connections:
#     pc1 = connection.split("-")[0]
#     pc2 = connection.split("-")[1]

#     try:
#         adjacent[pc1].append(pc2)
#     except:
#         adjacent[pc1] = [pc2]
#     try:
#         adjacent[pc2].append(pc1)
#     except:
#         adjacent[pc2] = [pc1]

# groups = []
# for pc in adjacent.keys():
#     print(f"\rChecking {pc}'s connections...", end="", flush=True)
#     for connected_pc in adjacent[pc]:
#         for connected_pc2 in adjacent[pc]:
#             if connected_pc2 in adjacent[connected_pc]:
#                 group = [pc, connected_pc, connected_pc2]
#                 group.sort()
#                 if group not in groups:
#                     groups.append(group)

# t_count = 0
# for group in groups:
#     for pc in group:
#         if str(pc)[0] == "t":
#             t_count += 1
#             break
# print(f"\nPART 1 'T' COUNT: {t_count}")

########### PART 2
G = nx.Graph()

for connection in connections:
    pc1 = connection.split("-")[0]
    pc2 = connection.split("-")[1]

    if pc1 not in G.nodes:
        G.add_node(pc1)
    if pc2 not in G.nodes:
        G.add_node(pc2)

    G.add_edge(pc1, pc2)

cliques = list(nx.find_cliques(G))
longest_index = 0
longest = 0
for i, clique in enumerate(cliques):
    if len(clique) > longest:
        longest = len(clique)
        longest_index = i

lan_clique = cliques[longest_index]
lan_clique.sort()
print(','.join(lan_clique))