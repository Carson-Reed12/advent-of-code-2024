total_count = 0

with open("day1_input.txt", "r") as file:
    line_lists = file.readlines()

# PART 1
list1 = []
list2 = []
for lines in line_lists:
    num1 = int(lines.split("   ")[0])
    num2 = int(lines.split("   ")[1].strip())

    list1.append(num1)
    list2.append(num2)

list1.sort()
list2.sort()

for num1, num2 in zip(list1, list2):
    total_count += abs(num1-num2)

print(f"TOTAL DISTANCE: {total_count}")

# PART 2
list1 = []
list2 = []
for lines in line_lists:
    num1 = int(lines.split("   ")[0])
    num2 = int(lines.split("   ")[1].strip())

    list1.append(num1)
    list2.append(num2)

total_score = 0

for num1 in list1:
    count = 0
    for num2 in list2:
        if num1 == num2:
            count += 1

    total_score += num1*count

print(f"TOTAL SIMILARITY SCORE: {total_score}")