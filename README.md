# GRE Essential Words

Simple game to help memorize GRE essential words.

## Usage

```bash
$ python3 game.py -h
usage: game.py [-h] [--lvl {0,1}] [bunch [bunch ...]]

Choose level and word bunches.

positional arguments:
  bunch        Choose `essential-words-#.txt` files to incorporate. Default:
               all

optional arguments:
  -h, --help   show this help message and exit
  --lvl {0,1}  Difficulty choice, ascending. Default: max difficulty
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
The format of these txts is: `word-of-interest=synonyms`, where `synonyms=synonym[,synonyms]` and `synonym` can be any string.
