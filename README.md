# Seven Deadly Syn[onym]s

Simple, gamified ways to memorize synonyms.

## Usage

```bash
$ python3 sds.py -h
usage: sds.py [-h] [--type {choice,fill,fill_all}] [--edit EDIT_DST]
              [--extra [EXTRA_FINS [EXTRA_FINS ...]]] [--dis] [--mix]
              [bunch [bunch ...]]

Choose game and word bunches.

positional arguments:
  bunch                 Choose `words/words-{bunch}.txt` files to incorporate.
                        Include -1 for last. Default: all

optional arguments:
  -h, --help            show this help message and exit
  --type {choice,fill,fill_all}
                        Choose type of game. Default: type all synonyms
  --edit EDIT_DST       Edit distance to be forgiven. Default: 2
  --extra [EXTRA_FINS [EXTRA_FINS ...]]
                        Include arbitrarily named files, relative to `words`
                        dir
  --dis                 Exclude all `words-#.txt` files
  --mix                 Mix primary word and synonyms
$ python3 sds.py --type choice -1 # -1 refers to bunches

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

To incorporate your own words, add a file with your own words
in the `words` directory. If the filename is `words-{bunch}.txt`, then you can
include it in the game by just passing `{bunch}` as an argument.
In any other case, use the `--extra` argument.
The format of these txts is: `word-of-interest=translation=synonyms`,
where `synonyms=synonym[,synonyms]` and `synonym`, `translation`
can be any string that does not contain `=`.
