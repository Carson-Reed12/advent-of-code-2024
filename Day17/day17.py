########### SETUP
with open("day17_input.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    if "Register A" in line:
        reg_a = int(line.split(": ")[1].strip())
    if "Register B" in line:
        reg_b = int(line.split(": ")[1].strip())
    if "Register C" in line:
        reg_c = int(line.split(": ")[1].strip())
    if "Program" in line:
        instructions = [int(item) for item in line.split(": ")[1].strip().split(",")]

########### PART 1
class Program():
    def __init__(self, reg_a, reg_b, reg_c, instructions):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.instructions = instructions
        self.prog_counter = 0
        self.halted = False
        self.output = []

    def execute_program(self):
        while not self.halted:
            self.execute_instruction()

    def check_halted(self):
        if self.halted:
            return True
        if self.prog_counter >= len(self.instructions):
            self.halted = True
            return True
        return False

    def execute_instruction(self):
        if self.check_halted():
            return

        opcode = self.instructions[self.prog_counter]
        operand = self.instructions[self.prog_counter + 1]

        if opcode == 0:
            self.adv(operand)
        if opcode == 1:
            self.bxl(operand)
        if opcode == 2:
            self.bst(operand)
        if opcode == 3:
            self.jnz(operand)
        if opcode == 4:
            self.bxc(operand)
        if opcode == 5:
            self.out(operand)
        if opcode == 6:
            self.bdv(operand)
        if opcode == 7:
            self.cdv(operand)

        if opcode != 3:
            self.prog_counter += 2

    def adv(self, operand):
        if 0 <= operand <= 3:
            self.reg_a = int(self.reg_a/2**operand)
        elif operand == 4:
            self.reg_a = int(self.reg_a/2**self.reg_a)
        elif operand == 5:
            self.reg_a = int(self.reg_a/2**self.reg_b)
        elif operand == 6:
            self.reg_a = int(self.reg_a/2**self.reg_c)

    def bxl(self, operand):
        self.reg_b = int(self.reg_b).__rxor__(operand)

    def bst(self, operand):
        if 0 <= operand <= 3:
            self.reg_b = operand % 8
        elif operand == 4:
            self.reg_b = self.reg_a % 8
        elif operand == 5:
            self.reg_b = self.reg_b % 8
        elif operand == 6:
            self.reg_b = self.reg_c % 8

    def jnz(self, operand):
        if self.reg_a == 0:
            self.prog_counter += 2
            return
        self.prog_counter = operand

    def bxc(self, operand):
        self.reg_b = int(self.reg_b).__rxor__(self.reg_c)

    def out(self, operand):
        if 0 <= operand <= 3:
            self.output.append(operand % 8)
        elif operand == 4:
            self.output.append(self.reg_a % 8)
        elif operand == 5:
            self.output.append(self.reg_b % 8)
        elif operand == 6:
            self.output.append(self.reg_c % 8)

    def bdv(self, operand):
        if 0 <= operand <= 3:
            self.reg_b = int(self.reg_a/2**operand)
        elif operand == 4:
            self.reg_b = int(self.reg_a/2**self.reg_a)
        elif operand == 5:
            self.reg_b = int(self.reg_a/2**self.reg_b)
        elif operand == 6:
            self.reg_b = int(self.reg_a/2**self.reg_c)

    def cdv(self, operand):
        if 0 <= operand <= 3:
            self.reg_c = int(self.reg_a/2**operand)
        elif operand == 4:
            self.reg_c = int(self.reg_a/2**self.reg_a)
        elif operand == 5:
            self.reg_c = int(self.reg_a/2**self.reg_b)
        elif operand == 6:
            self.reg_c = int(self.reg_a/2**self.reg_c)

def display_stats(program):
    print("PROGRAM STATS")
    print("--------------------")
    print(f"REGISTER A: {program.reg_a}")
    print(f"REGISTER B: {program.reg_b}")
    print(f"REGISTER C: {program.reg_c}")
    print(f"OUTPUT: {program.output}")
    print(f"PROGRAM COUNTER: {program.prog_counter}")

program = Program(reg_a, reg_b, reg_c, instructions)
program.execute_program()
display_stats(program)
print(f"PART 1 OUTPUT STRING: {','.join([str(output) for output in program.output])}")

########### PART 2
reg_a = 1
position = len(instructions) - 1
while True:
    program = Program(reg_a, reg_b, reg_c, instructions)
    program.execute_program()
    print(f"\rREG A: {reg_a} - Output: {program.output}", end="", flush=True)
    if program.output == instructions:
        break
    if program.output == instructions[position:]:
        reg_a *= 8
        position -= 1
    else:
        reg_a += 1

print(f"\nPART 2 REG A VAL: {reg_a}")
