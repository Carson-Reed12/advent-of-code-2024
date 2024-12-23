import itertools
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

############# PART 2
def search_for_sequence(prices, secret, sequence):
    for i in range(len(prices[secret]["changes"])):
        try:
            if prices[secret]["changes"][i] == sequence[0] and prices[secret]["changes"][i+1] == sequence[1] and prices[secret]["changes"][i+2] == sequence[2] and prices[secret]["changes"][i+3] == sequence[3]:
                return prices[secret]["prices"][i+4]
        except:
            return None

def get_prices(secrets):
    prices = {}

    for orig_secret in secrets:
        secret = orig_secret
        prices[orig_secret] = {"prices": [], "changes": []}
        prices[orig_secret]["prices"].append(int(str(orig_secret)[-1]))
        last_val = int(str(orig_secret)[-1])

        for _ in range(2000):
            secret = roll_secret(secret)
            prices[orig_secret]["prices"].append(int(str(secret)[-1]))
            prices[orig_secret]["changes"].append(int(str(secret)[-1]) - last_val)
            last_val = int(str(secret)[-1])

    return prices

def valid_sequence(sequence):
    for i in range(len(sequence) - 1):
        if sequence[i] + sequence[i+1] >= 10 or sequence[i] + sequence[i+1] <= -10:
            return False
    for i in range(len(sequence) - 2):
        if sequence[i] + sequence[i+1] + sequence[i+2] >= 10 or sequence[i] + sequence[i+1] + sequence[i+2] <= -10:
            return False
    if sequence[0] + sequence[1] + sequence[2] + sequence[3] >= 10 or sequence[0] + sequence[1] + sequence[2] + sequence[3] <= -10:
        return False
    return True

prices = get_prices(secret_numbers)
max_count = 0
max_sequence = []
for sequence in itertools.product(range(-9, 10), repeat=4): 
    if not valid_sequence(sequence):
        continue
    test_sequence = list(sequence)
    print(f"\rCURRENT MAX: {max_count} - {test_sequence}", end="", flush=True)

    count = 0
    for secret in secret_numbers:
        price = search_for_sequence(prices, secret, test_sequence)
        if price:
            count += price

    if count > max_count:
        max_count = count
        max_sequence = test_sequence

print(f"\nPART 2 MAX COUNT: {max_count}")
print(f"PART 2 MAX SEQUENCE: {max_sequence}")
    
