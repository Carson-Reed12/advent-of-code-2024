import re
############ SETUP
with open("day19_input.txt", "r") as file:
    lines = file.readlines()

patterns = lines[0].strip().split(", ")
designs = {design.strip(): {} for design in lines[2:]}

############ PART 1
def build_towel(index, substring, design):
    if substring == design:
        return True
    if len(substring) > len(design) or substring not in design:
        checked_substrings.append(substring)
        return False
    
    for pattern in designs[design]:
        if index in designs[design][pattern][0]:
            if substring + pattern not in checked_substrings:
                if build_towel(index + len(pattern), substring + pattern, design):
                    return True
                else:
                    checked_substrings.append(substring + pattern)
    return False

towel_id = 0
for design in designs.keys():
    for pattern in patterns:
        designs[design][pattern] = [[match.start() for match in re.finditer(pattern, design)], str(towel_id)]
        towel_id += 1

total_designs = 0
for design in designs.keys():
    checked_substrings = []
    if build_towel(0, "", design):
        total_designs += 1
    checked_substrings.clear()

print(f"PART 1 TOTAL DESIGNS: {total_designs}")

############ PART 2
# def possible_towels(index, substring, config, design):
    
#     # print(substring)
#     # print(config)
#     # input()

#     if substring == design:
#         return 1
#     if substring in pattern_cache.keys():
#         return pattern_cache[substring]
#     # if len(substring) > len(design) or substring not in design:
#     #     checked_substrings.append(substring)
#     #     return 0
#     score = 0
#     for pattern in designs[design]:
#         if index in designs[design][pattern][0]:

#             new_score = possible_towels(index + len(pattern), substring + pattern, config + designs[design][pattern][1], design)
            

#             score += new_score
#     pattern_cache[substring + pattern] = score
#     return score

def possible_towels(substring): # adapted from https://github.com/hugseverycat/aoc2024/blob/master/day19.py. Need to figure out why my version didn't work
    if substring == '':
        return 1
    if substring in pattern_cache.keys():
        return pattern_cache[substring]
    
    score = 0
    for pattern in patterns:
        if substring.startswith(pattern):
            new_substring = substring[len(pattern):]
            score += possible_towels(new_substring)

    pattern_cache[substring] = score
    return score

pattern_cache = {}
total_towels = 0
for design in designs.keys():
    total_towels += possible_towels(design)

print(f"PART 2 TOTAL DESIGNS: {total_towels}")