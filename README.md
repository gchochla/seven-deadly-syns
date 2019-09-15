# GRE Essential Words

Simple gamified training to help memorize GRE essential words.

## Usage

```bash
$ python3 train.py -h
usage: train.py [-h] [--type {choice,fill,fill_all}] [--edit EDIT_DST]
                [--extra [EXTRA_FINS [EXTRA_FINS ...]]] [--dis] [--mix]
                [bunch [bunch ...]]

Choose game and word bunches.

positional arguments:
  bunch                 Choose `essential-words-{bunch}.txt` files to
                        incorporate. Include -1 for last. Default: all

optional arguments:
  -h, --help            show this help message and exit
  --type {choice,fill,fill_all}
                        Choose type of game. Default: type all synonyms
  --edit EDIT_DST       Edit distance to be forgiven. Default: 2
  --extra [EXTRA_FINS [EXTRA_FINS ...]]
                        Include arbitrarily named files, relative to
                        `essential-words` dir
  --dis                 Exclude all `essential-words-#.txt` files
  --mix                 Mix primary word and synonyms
$ python3 train.py --type choice -1 # -1 refers to bunches

Press `Ctrl+C` to exit.

$$$$$$$$$$$$$$$$$$$$$$$$$$$

Choose synonym of converge:
0. mingle
1. profuce
2. abet
3. connoisseur
4. enigma

Answer: 
```

## Extensions

To incorporate your own words, add a file named `essential-words-#.txt`
with your own words in the `essential-words` directory, where `#` is a natural number.
The format of these txts is: `word-of-interest=translation=synonyms`, where `synonyms=synonym[,synonyms]`
and `synonym`, `translation` can be any string that does not contain `=`.
