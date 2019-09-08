import argparse
import re
import random
from os import walk
from heapq import nlargest

random.seed(None)

LEVELS = [0, 1]

BUNCHES = []
txtre = re.compile(r'essential-words-\d+.txt')
for (dirpath, dirnames, filenames) in walk('./essential-words'):
    for filename in filenames:
        mo = txtre.search(filename)
        if mo:
            BUNCHES.append(int(mo.group().split('-')[-1].split('.')[0]))

parser = argparse.ArgumentParser(description='Choose level and word bunches.')
parser.add_argument(
    'bunches', metavar='bunch', type=int, nargs='*', default=BUNCHES,
    help='Choose `essential-words-#.txt` files to incorporate. Default: all'
)
parser.add_argument(
    '--lvl', dest='level', type=int, default=LEVELS[-1], choices=LEVELS,
    help='Difficulty choice, ascending. Default: max difficulty'
)
parser.add_argument(
    '--edit', dest='edit_dst', type=int, default=2,
    help='Edit distance to be forgiven. Default: 2'
)

def pr_red(skk, **kwargs): print(f'\033[91m{skk}\033[00m', **kwargs) 
def pr_green(skk, **kwargs): print(f'\033[92m{skk}\033[00m', **kwargs)
def pr_yellow(skk, **kwargs): print(f'\033[93m{skk}\033[00m', **kwargs)

def sample_from_iterable(it, k):
    return (x for _, x in nlargest(k, ((random.random(), x) for x in it)))

def shuffle_iterable(it):
    return sample_from_iterable(it, len(it))

def game(words, translation, level, **kwargs):
    games = [game_easy, game_hard]
    if len(games) != len(LEVELS):
        raise NotImplementedError('Correct `LEVELS` variable.')
    games[level](words, translation, **kwargs)

def game_easy(words, translation, **kwargs):
    synonyms_presented = 5
    total = 0
    correct = 0
    try:
        while True:
            random_word = list(sample_from_iterable(words, 1))[0]
            correct_synonym = list(sample_from_iterable(words[random_word], 1))[0]
            choices = [correct_synonym]

            wrong_words = list(sample_from_iterable(words, synonyms_presented - 1))
            for wrong_word in wrong_words:
                while wrong_word == random_word:
                    wrong_word = list(sample_from_iterable(words, 1))[0]
                choices.append(list(sample_from_iterable(words[wrong_word], 1))[0])
            
            choices = list(shuffle_iterable(choices))

            print(f'Choose synonym of ', end=''); pr_yellow(random_word, end=''); print(':')
            for i, choice in enumerate(choices):
                print(f'{i}. {choice}')

            answer = -2
            while answer not in list(range(synonyms_presented)):
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
            pr_yellow(random_word, end=''); print(f'\'s translation is: {translation[random_word]}.')
            pr_yellow(random_word, end=''); print(f'\'s possible synonyms are {", ".join(words[random_word])}.\n')

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

def game_hard(words, translation, **kwargs):
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

            pr_yellow(random_word, end=''); print(f'\'s translation is: {translation[random_word]}.')
            pr_yellow(random_word, end=''); print(f'\'s possible synonyms are {", ".join(words[random_word])}.\n')

    except KeyboardInterrupt:
        print('\b\b  ') # remove ^C from screen
        print(f'\n\nResult: {correct} / {total}')
        print('Exiting...')

if __name__ == '__main__':
    args = parser.parse_args()
    words = {}
    translation = {}
    for txt in [f'essential-words/essential-words-{i}.txt' for i in args.bunches]:
        with open(txt) as txtf:
            for line in txtf.readlines():
                line = line.split('=')
                words[line[0]] = line[2][:-1].split(',') # [:-1] to remove '\n'
                translation[line[0]] = line[1]
    print('Press `Ctrl+C` to exit.\n')
    kwargs = {'edit_dst': args.edit_dst}
    game(words, translation, args.level, **kwargs)
