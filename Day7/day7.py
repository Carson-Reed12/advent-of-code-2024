import itertools
############ SETUP
with open("day7_input.txt", "r") as file:
    lines = file.readlines()

evaluation = {}
for line in lines:
    evaluation[line.split(":")[0]] = line.split(":")[1].strip().split(" ")

############ PART 1
total_count = 0
for result in evaluation.keys():
    vals = evaluation[result]
    num_ops = len(vals) - 1

    for op_order in map(''.join, itertools.product('01', repeat=num_ops)):
        count = int(vals[0])
        
        for i in range(len(vals) - 1):
            num = int(vals[i+1])

            if int(op_order[i]) == 0:
                count += num
            else:
                count *= num

        if count == int(result):
            total_count += int(result)
            break        

print(f"PART 1 TOTAL COUNT: {total_count}")

############ PART 2
total_count = 0
for result in evaluation.keys():
    vals = evaluation[result]
    num_ops = len(vals) - 1

    for op_order in map(''.join, itertools.product('012', repeat=num_ops)):
        count = int(vals[0])
        
        for i in range(len(vals) - 1):
            num = int(vals[i+1])

            if int(op_order[i]) == 0:
                count += num
            elif int(op_order[i]) == 1:
                count *= num
            else:
                count = int(str(count) + str(num))

        if count == int(result):
            total_count += int(result)
            break        

print(f"PART 2 TOTAL COUNT: {total_count}")
