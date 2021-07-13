import json
import random
import string
import time
from itertools import permutations, combinations

MAX_SIZE = 8


def generate_random():
    return ''.join([random.choice(string.digits) for _ in range(8)])


# Muito custoso
def generate_hash(characters):
    start = time.time()

    hash_dict = {}
    miro_dict = {}
    characters = list(characters)
    for i in range(1, 9):
        key = generate_random()
        while key in hash_dict.keys():
            key = generate_random()

        for password in list(combinations(characters, i)):
            hash_dict[generate_random()] = ''.join(password)
            miro_dict[''.join(password)] = generate_random()
    print(f"Rodando: {characters}", (time.time() - start) / 60)
    return hash_dict, miro_dict


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

        match_list.insert(matches, random_code)
        matches += 1
    total_time = time.time() - start_time
    print(f"Tempo gasto: {total_time}")
    return True


# Técnica de Júlio Cesar

def cryptography(password, key=2):

    pass_size = len(password)
    for i in range(0, int(pass_size / 2)):
        aux = password[(i + key) % pass_size]
        password[(i + key) % pass_size] = password[(pass_size - i) % pass_size]
        password[(pass_size - i) % pass_size] = aux

    return password


def main():
    true_password = list(input('Type a password: '))

    # print(len(hash_table))

    assert len(true_password) <= MAX_SIZE, f"Password must have max size of {MAX_SIZE}"
    #
    code = cryptography(true_password.copy())
    #
    print("Password: ", true_password)
    print("Password codified: ", code)
    #
    if break_code(code, true_password):
        print("We break it!")
    # print("Spent time: ", total)


if __name__ == '__main__':
    main()
