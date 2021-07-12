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

    match_list = []
    matches = 0

    while matches != len(code):

        random_code = random.choice(code)
        random_attempts = 0
        while random_code != true_word[matches]:
            random_code = random.choice(code)
            random_attempts += 1
            if random_attempts == 8:
                return False
        match_list.insert(matches, random_code)
        matches += 1

    return True


# Técnica de Júlio Cesar

def cryptography(password, key=2):
    for i in range(0, int(MAX_SIZE / 2)):
        aux = password[(i + key) % MAX_SIZE]
        password[(i + key) % MAX_SIZE] = password[(MAX_SIZE - i) % MAX_SIZE]
        password[(MAX_SIZE - i) % MAX_SIZE] = aux

    return password
