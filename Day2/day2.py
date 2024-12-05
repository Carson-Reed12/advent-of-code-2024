import copy

def check_gradient(num_report):
    sign = 0
    
    for i in range(len(num_report)-1):
        num1 = num_report[i]
        num2 = num_report[i+1]

        if i == 0:
            if num1 > num2:
                sign = 1
            elif num1 < num2:
                sign = 2
            else:
                return False
        else:
            if num1 > num2 and sign == 2:
                return False
            elif num1 < num2 and sign == 1:
                return False
            elif num1 == num2:
                return False
            
    return True

def check_difference(num_report):
    for i in range(len(num_report)-1):
        num1 = num_report[i]
        num2 = num_report[i+1]

        difference = abs(num1-num2)

        if difference == 0 or difference > 3:
            return False
        
    return True

def check_safety(num_report):
    if check_gradient(num_report):
        if check_difference(num_report):
            # print(f"REPORT SAFE: {num_report}")
            return True
        else:
            # print(f"REPORT UNSAFE (difference): {num_report}")
            return False

    else:
        # print(f"REPORT UNSAFE (gradient): {num_report}")
        return False

with open("day2_input.txt", "r") as file:
    reports = file.readlines()

reports = [report.strip().split(" ") for report in reports]

safe_count = 0
unsafe_count = 0

for report in reports:
    num_report = [int(item) for item in report]

    if check_safety(num_report):
        safe_count += 1
    else:
        unsafe_count += 1

print("PART 1")
print(f"SAFE COUNT: {safe_count}")
print(f"UNSAFE COUNT: {unsafe_count}")
print("----------------")

############## PART 2

safe_count = 0
unsafe_count = 0

for report in reports:
    num_report = [int(item) for item in report]

    if check_safety(num_report):
        safe_count += 1
        continue
    else:
        safe = False
        
        for i in range(len(num_report)):
            chopped_report = copy.deepcopy(num_report)
            chopped_report.pop(i)

            if check_safety(chopped_report):
                safe = True
                break

        if safe:
            safe_count += 1
        else:
            unsafe_count += 1

print("PART 2")
print(f"SAFE COUNT: {safe_count}")
print(f"UNSAFE COUNT: {unsafe_count}")
