############ SETUP
with open("day11_input.txt", "r") as file:
    stones = list(file.readlines()[0].strip().split(" "))
stones = {int(stone): 1 for stone in stones}
############ PART 1 AND 2

def stone_blink(stone):
    if stone == 0:
        return [1]
    elif len(str(stone))%2 == 0:
        first_half = int(str(stone)[:int(len(str(stone))/2)])
        second_half = int(str(stone)[int(len(str(stone))/2):])
        return [first_half, second_half]
    else:
        return [stone*2024]

def blink(stones):
    produced_stones = {}
    for stone in stones.keys():
        if stones[stone] != 0:
            new_stones = stone_blink(stone)
            for new_stone in new_stones:
                try:
                    produced_stones[new_stone] += stones[stone]
                except:
                    produced_stones[new_stone] = stones[stone]
            stones[stone] = 0
    
    for stone in produced_stones.keys():
        try:
            stones[stone] += produced_stones[stone]
        except:
            stones[stone] = produced_stones[stone]
    return stones

def all_blinks(stones, num_blinks):
    for _ in range(num_blinks):
        stones = blink(stones)
    return stones

total_stones = 0
stones = all_blinks(stones, 25)
for stone in stones.keys():
    total_stones += stones[stone]
print(f"PART 1 TOTAL STONES: {total_stones}")

total_stones = 0
stones = all_blinks(stones, 75)
for stone in stones.keys():
    total_stones += stones[stone]
print(f"PART 2 TOTAL STONES: {total_stones}")