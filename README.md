# mangle.py - Tool to generate mangled words. Useful for auth attacks, pentesting

usage: mangle.py [-h] [-a] [-p] [-b] [-l] [-o [FILE]] string [string ...]

positional arguments:
  string

optional arguments:
  -h, --help            show this help message and exit
  -a, --append          Append stuff
  -p, --prepend         Prepend stuff
  -b, --bad             Include a list of bad passwords
  -l, --leet            l3371fy
  -o [FILE], --outfile [FILE]
                        Write output to FILE, append if already exists
