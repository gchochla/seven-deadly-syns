# GRE Essential Words

Simple gamified training to help memorize GRE essential words.

## Usage

```bash
$ python3 train.py -h
usage: game.py [-h] [--lvl {0,1}] [--edit EDIT_DST] [bunch [bunch ...]]

Choose level and word bunches.

positional arguments:
  bunch            Choose `essential-words-#.txt` files to incorporate.
                   Default: all

optional arguments:
  -h, --help       show this help message and exit
  --lvl {0,1}      Difficulty choice, ascending. Default: max difficulty
  --edit EDIT_DST  Edit distance to be forgiven. Default: 2
$ python3 game.py --lvl 0
Press `Ctrl+C` to exit.

Choose synonym of `alleviate`:
0. secret
1. soothe
2. repudiate
3. equivocal
4. reduce

Answer:
```

## Extensions

To incorporate your own words, add a file named `essential-words-#.txt`
with your own words in the `essential-words` directory, where `#` is a natural number.
The format of these txts is: `word-of-interest=translation=synonyms`, where `synonyms=synonym[,synonyms]`
and `synonym`, `translation` can be any string that does not contain `=`.
