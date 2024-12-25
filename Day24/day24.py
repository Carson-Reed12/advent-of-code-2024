import itertools
import copy
########## SETUP
with open("day24_input.txt", "r") as file:
    lines = file.readlines()

wires = {}
orig_gates = []
for line in lines:
    if ":" in line:
        wires[line.split(":")[0]] = int(line.split(": ")[1])
    elif line != "\n":
        orig_gates.append(line.strip())

for gate in orig_gates:
    wire1 = gate.split(" ")[0]
    wire2 = gate.split(" ")[2]
    wire3 = gate.split("-> ")[1]

    for wire in [wire1, wire2, wire3]:
        if wire not in wires.keys():
            wires[wire] = None

########## PART 1
def evaluate_gate(gate):
    pieces = gate.split(" ")

    if wires[pieces[0]] is not None and wires[pieces[2]] is not None:
        if pieces[1] == "XOR":
            wires[pieces[4]] = wires[pieces[0]] ^ wires[pieces[2]]
        elif pieces[1] == "OR":
            wires[pieces[4]] = int(wires[pieces[0]] or wires[pieces[2]])
        elif pieces[1] == "AND":
            wires[pieces[4]] = int(wires[pieces[0]] and wires[pieces[2]])

def simulate_gates(wires, gates):
    while not all(wires[wire] is not None for wire in wires.keys()):
        last_wires = copy.deepcopy(wires)
        for gate in gates:
            evaluate_gate(gate)
        if last_wires == wires:
            return 0

    z_wires = [wire for wire in wires.keys() if wire.startswith("z")]
    z_wires.sort()

    z_bits = ""
    for wire in reversed(z_wires):
        z_bits += str(wires[wire])

    return int(z_bits, 2)

z_val = simulate_gates(wires, orig_gates)
print(f"PART 1 Z VAL: {z_val}")

########## PART 2
def initialize_wires(wires):
    for wire in wires.keys():
        if not wire.startswith("x") and not wire.startswith("y"):
            wires[wire] = None
            
def swap_gates(gates, swaps):
    for i in range(0,8,2):
        buffer = gates[swaps[i]].split(" ")[-1]

        gates[swaps[i]] = ' '.join(gates[swaps[i]].split(" ")[:-1]) + " " + gates[swaps[i+1]].split(" ")[-1]
        gates[swaps[i+1]] = ' '.join(gates[swaps[i+1]].split(' ')[:-1]) + " " + buffer


x_wires = [wire for wire in wires.keys() if wire.startswith("x")]
x_wires.sort()

x_bits = ""
for wire in reversed(x_wires):
    x_bits += str(wires[wire])

y_wires = [wire for wire in wires.keys() if wire.startswith("y")]
y_wires.sort()

y_bits = ""
for wire in reversed(y_wires):
    y_bits += str(wires[wire])

expected_value = int(x_bits, 2) + int(y_bits, 2)

for i, swaps in enumerate(itertools.permutations(range(0, len(orig_gates)), 8)):
    print(f"\r{swaps} - {i}                       ", end="", flush=True)
    gates = copy.deepcopy(orig_gates)
    swap_gates(gates, swaps)

    initialize_wires(wires)
    if simulate_gates(wires, gates) == expected_value:
        final_swaps = swaps
        break

swapped_wires = []
for swap in final_swaps:
    swapped_wires.append(orig_gates[swap].split(" ")[-1])

swapped_wires.sort()

print("\n---------")
print(f"{final_swaps}")
print(','.join(swapped_wires))
