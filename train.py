import argparse
import re
import random
from os import walk
from heapq import nlargest

random.seed(None)

LEVELS = ['choice', 'fill', 'fill_all']

def get_default_bunches():
    bunches = []
    txtre = re.compile(r'essential-words-\d+.txt')
    for (dirpath, dirnames, filenames) in walk('./essential-words'):
        for filename in filenames:
            mo = txtre.search(filename)
            if mo:
                bunches.append(int(mo.group().split('-')[-1].split('.')[0]))
    return bunches

BUNCHES = get_default_bunches()

parser = argparse.ArgumentParser(description='Choose game and word bunches.')
parser.add_argument(
    'bunches', metavar='bunch', type=int, nargs='*', default=BUNCHES,
    help='Choose `essential-words-{bunch}.txt` files to incorporate. Include -1 for last.' + \
    ' Default: all'
)
parser.add_argument(
    '--type', type=str, default=LEVELS[-1], choices=LEVELS,
    help='Choose type of game. Default: fill blanks'
)
parser.add_argument(
    '--edit', dest='edit_dst', type=int, default=2,
    help='Edit distance to be forgiven. Default: 2'
)
parser.add_argument(
    '--extra', dest='extra_fins', type=str, nargs='*', default=[],
    help='Include arbitrarily named files, relative to `essential-words` dir'
)
parser.add_argument(
    '--dis', action='store_true', help='Exclude all `essential-words-#.txt` files'
)
parser.add_argument(
    '--mix', action='store_true', help='Mix primary word and synonyms'
)

def purple(skk): return f'\033[35m{skk}\033[00m'
def red(skk): return f'\033[91m{skk}\033[00m' 
def green(skk): return f'\033[92m{skk}\033[00m'
def yellow(skk): return f'\033[93m{skk}\033[00m'

def sample_from_iterable(it, k):
    return [x for _, x in nlargest(k, ((random.random(), x) for x in it))]

def shuffle_iterable(it):
    return sample_from_iterable(it, len(it))

def game(words, translations, type, **kwargs):
    globals()[type](words, translations, **kwargs)

def choice(words, translations, **kwargs):
    synonyms_presented = 5
    mix = kwargs['mix']
    total = 0
    correct = 0
    max_len = 0
    try:
        while True:
            init_random = sample_from_iterable(words, 1)[0]
            if mix:
                synonyms = shuffle_iterable([init_random] + words[init_random])
                [random_word, correct_synonym] = synonyms[0:2]
                translation = translations[init_random]
                synonyms = synonyms[1:]
            else:
                random_word = init_random
                correct_synonym = sample_from_iterable(words[init_random], 1)[0]
                translation = translations[init_random]
                synonyms = words[init_random]

            choices = [correct_synonym]

            wrong_words = sample_from_iterable(words, synonyms_presented - 1)
            for wrong_word in wrong_words:
                while wrong_word == init_random:
                    wrong_word = sample_from_iterable(words, 1)[0]
                choices.append(sample_from_iterable(words[wrong_word], 1)[0])
            
            choices = shuffle_iterable(choices)

            question = f'Choose synonym of {yellow(random_word)}:'
            max_len = max_len if max_len > len(question) - 10 else len(question) - 10
            print('\n' + purple('$' * max_len) + '\n')
            print(question)

            for i, choice in enumerate(choices):
                print(f'{i}. {choice}')

            answer = -2
            while answer not in range(synonyms_presented):
                if answer != -2:
                    print('Incorrect input. Try again :(')
                try:
                    answer = int(input('\nAnswer: '))
                except ValueError:
                    answer = -1
            print()

            total += 1
            if choices[answer] == correct_synonym:
                print(green('Correct answer!'))
                correct += 1
            else:
                print(red('Incorrect answer!'))
            print(f'{yellow(random_word)}\'s translation are: {translation}.')
            print(f'{yellow(random_word)}\'s possible synonyms are {", ".join(synonyms)}.\n')

    except KeyboardInterrupt:
        print('\b\b  ') # remove ^C from screen
        print(f'\n\nResult: {correct} / {total}')
        print('Exiting...')

def edit_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def fill(words, translations, **kwargs):
    edit_dst = kwargs['edit_dst']
    total = 0
    correct = 0
    max_len = 0
    try:
        while True:
            random_word = list(sample_from_iterable(words, 1))[0]
            question = f'Write a synonym of {yellow(random_word)}:'
            max_len = max_len if max_len > len(question) - 10 else len(question) - 10
            print('\n' + purple('$' * max_len) + '\n')
            print(question)
            answer = input('Answer: ')
            print()
            total += 1
            prev = correct
            for synonym in words[random_word]:
                if edit_distance(synonym, answer) <= edit_dst:
                    print(green('Correct answer!'))
                    correct += 1
                    break
            if prev == correct:
                print(red('Wrong answer!'))

            print(f'{yellow(random_word)}\'s translation are: {translations[random_word]}.')
            print(f'{yellow(random_word)}\'s possible synonyms are {", ".join(words[random_word])}.\n')

    except KeyboardInterrupt:
        print('\b\b  ') # remove ^C from screen
        print(f'\n\nResult: {correct} / {total}')
        print('Exiting...')

def fill_all(words, translations, **kwargs):
    edit_dst = kwargs['edit_dst']
    total = 0
    correct = 0
    max_len = 0
    try:
        while True:
            random_word = list(sample_from_iterable(words, 1))[0]
            question = f'Write all the synonyms of {yellow(random_word)} (separated by comma):'
            max_len = max_len if max_len > len(question) - 10 else len(question) - 10
            print('\n' + purple('$' * max_len) + '\n')
            print(question)
            synonyms = words[random_word]
            answers = input('Answer: ').split(',')
            answers = [answer.strip() for answer in answers]
            while True:
                if len(answers) <= len(synonyms):
                    break
                print(f'Number of correct synonyms: {len(synonyms)}. Try again!')
                answers = input('Answer: ').split(',')

            print()
            total += 1
            count = 0
            for synonym in synonyms:
                for answer in answers:
                    if edit_distance(synonym, answer) <= edit_dst:
                        count += 1
                        break

            if count < len(synonyms):
                print(f'{red("You got")} {count} {red("correct")}.')
            else:
                print(green('Correct answers!'))
                correct += 1

            print(f'{yellow(random_word)}\'s translation are: {translations[random_word]}.')
            print(f'{yellow(random_word)}\'s possible synonyms are {", ".join(synonyms)}.')

    except KeyboardInterrupt:
        print('\b\b  ') # remove ^C from screen
        print(f'\n\nResult: {correct} / {total}')
        print('Exiting...')

if __name__ == '__main__':
    args = parser.parse_args()
    words = {}
    translations = {}

    if args.dis:
        bunches = []
    else:
        bunches = args.bunches

    for txt in [f'essential-words/essential-words-{i if i != -1 else BUNCHES[-1]}.txt' for i in bunches] \
        + [f'essential-words/{fin}' for fin in args.extra_fins]:
        with open(txt) as txtf:
            for line in txtf.readlines():
                line = line.split('=')
                words[line[0]] = line[2][:-1].split(',') # [:-1] to remove '\n'
                translations[line[0]] = line[1]
    if len(words) == 0:
        raise ValueError('No words were found, try reading the help message (-h)') 
    print('Press `Ctrl+C` to exit.')
    kwargs = {'edit_dst': args.edit_dst, 'mix': args.mix}
    game(words, translations, args.type, **kwargs)
