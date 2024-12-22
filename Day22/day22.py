############# SETUP
with open("day22_input.txt", "r") as file:
    lines = file.readlines()
secret_numbers = [int(line.strip()) for line in lines]

############# PART 1
def roll_secret(secret):
    secret = int(secret).__rxor__(secret*64) % 16777216 # step 1
    secret = int(secret).__rxor__(int(secret/32)) % 16777216 # step 2
    secret   = int(secret).__rxor__(secret*2048) % 16777216 # step 3
    return secret

def multi_roll_secret(i, secret):
    for _ in range(i):
        secret = roll_secret(secret)
    return secret

total_sum = 0
for secret in secret_numbers:
    total_sum += multi_roll_secret(2000, secret)
print(f"PART 1 TOTAL SUM: {total_sum}")