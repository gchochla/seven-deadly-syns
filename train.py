import argparse
import re
import random
from os import walk
from heapq import nlargest

random.seed(None)

LEVELS = ['choice', 'fill']

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

def pr_red(skk, **kwargs): print(f'\033[91m{skk}\033[00m', **kwargs) 
def pr_green(skk, **kwargs): print(f'\033[92m{skk}\033[00m', **kwargs)
def pr_yellow(skk, **kwargs): print(f'\033[93m{skk}\033[00m', **kwargs)

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

            print(f'Choose synonym of ', end=''); pr_yellow(random_word, end=''); print(':')
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
                pr_green('Correct answer!')
                correct += 1
            else:
                pr_red('Incorrect answer!')
            pr_yellow(random_word, end=''); print(f'\'s translation is: {translation}.')
            pr_yellow(random_word, end=''); print(f'\'s possible synonyms are {", ".join(synonyms)}.\n')

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
    try:
        while True:
            random_word = list(sample_from_iterable(words, 1))[0]
            print(f'Write a synonym of ', end=''); pr_yellow(random_word, end=''); print(':')
            answer = input('Answer: ')
            print()
            total += 1
            prev = correct
            for synonym in words[random_word]:
                if edit_distance(synonym, answer) <= edit_dst:
                    pr_green('Correct answer!')
                    correct += 1
                    break
            if prev == correct:
                pr_red('Wrong answer!')

            pr_yellow(random_word, end=''); print(f'\'s translations is: {translations[random_word]}.')
            pr_yellow(random_word, end=''); print(f'\'s possible synonyms are {", ".join(words[random_word])}.\n')

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
    print('Press `Ctrl+C` to exit.\n')
    kwargs = {'edit_dst': args.edit_dst, 'mix': args.mix}
    game(words, translations, args.type, **kwargs)
