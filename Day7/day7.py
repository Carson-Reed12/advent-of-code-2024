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

    for x in map(''.join, itertools.product('01', repeat=num_ops)):
        count = 0
        
        for i in range(len(vals) - 1):
            num1 = int(vals[i])
            num2 = int(vals[i+1])

            if i == 0:
                if int(x[i]) == 0:
                    count += num1+num2
                else:
                    count += num1*num2
            else:
                if int(x[i]) == 0:
                    count += num2
                else:
                    count *= num2

        if count == int(result):
            total_count += int(result)
            break        

print(f"PART 1 TOTAL COUNT: {total_count}")

############ PART 2
total_count = 0
for result in evaluation.keys():
    vals = evaluation[result]
    num_ops = len(vals) - 1

    for x in map(''.join, itertools.product('012', repeat=num_ops)):
        count = 0
        
        for i in range(len(vals) - 1):
            num1 = int(vals[i])
            num2 = int(vals[i+1])

            if i == 0:
                if int(x[i]) == 0:
                    count += num1+num2
                elif int(x[i]) == 1:
                    count += num1*num2
                else:
                    count = int(str(num1) + (str(num2)))
            else:
                if int(x[i]) == 0:
                    count += num2
                elif int(x[i]) == 1:
                    count *= num2
                else:
                    count = int(str(count) + str(num2))

        if count == int(result):
            total_count += int(result)
            break        

print(f"PART 2 TOTAL COUNT: {total_count}")