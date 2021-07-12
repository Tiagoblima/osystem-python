import json
import random
import string
import time
from itertools import permutations, combinations

MAX_SIZE = 8


def generate_random():
    return ''.join([random.choice(string.digits) for _ in range(8)])


# Muito custoso
def generate_hash():
    hash_dict = {}
    characters = list(string.ascii_letters + string.punctuation + string.digits)
    for i in range(1, 9):
        key = generate_random()
        while key in hash_dict.keys():
            key = generate_random()

        for password in list(combinations(characters, i)):
            hash_dict[generate_random()] = password
    return hash_dict


def break_code(code, true_word):
    fails = []
    random_code = [random.choice(code) for i in range(MAX_SIZE)]
    match_list = []
    matches = 0
    start_time = time.time()
    while matches != len(code):
        fails.append(random_code)

        random_code = random.choice(code)
        random_attempts = 0
        while random_code != true_word[matches]:
            random_code = random.choice(code)
            random_attempts += 1
            if random_attempts == 8:
                return False
        match_list.insert(matches, random_code)
        matches += 1
    total_time = time.time() - start_time
    return total_time


# Técnica de Júlio Cesar

def cryptography(password, key=2):
    for i in range(0, int(MAX_SIZE / 2)):
        aux = password[(i + key) % MAX_SIZE]
        password[(i + key) % MAX_SIZE] = password[(MAX_SIZE - i) % MAX_SIZE]
        password[(MAX_SIZE - i) % MAX_SIZE] = aux

    return password


def main():
    true_password = list(input('Type a password: '))
    # hash_table = generate_hash()
    # print(len(hash_table))

    # json.dump(hash_table, open('hash.json', 'w'), indent=4)

    assert len(true_password) <= MAX_SIZE, f"Password must have size {MAX_SIZE}"

    code = cryptography(true_password.copy())

    print("Password: ", true_password)
    print("Password codified: ", code)

    total = break_code(code, true_password)
    print("Spent time: ", total)


if __name__ == '__main__':
    main()
