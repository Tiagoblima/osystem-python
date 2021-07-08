import random
import string


def break_code(code, true_word):
    fails = []
    random_code = [random.choice(code) for i in range(len(code))]
    match_list = []
    matches = 0
    while matches != len(code):
        fails.append(random_code)

        random_code = random.choice(code)
        while random_code != true_word[matches]:
            random_code = random.choice(code)

        match_list.insert(matches, random_code)
        matches += 1
    print(match_list)
    return True


def main():
    true_password = list(input('Type a password: '))
    code = true_password.copy()
    random.shuffle(code)
    print(code)
    print(true_password)

    if break_code(code, true_password):
        print("We broke de code!")




if __name__ == '__main__':
    main()
