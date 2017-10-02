'''
Marcel Gerardino <goetia@sentineldr.com>

Generates a dictionary of mangled words according to basic rules of permutation,
case combinations and so on.
'''

import sys
import datetime
import argparse
from itertools import permutations


def caps(pword, case):
    pword = pword.lower()
    if case == 1:
        upperfpw = list(pword)
        upperfpw[0] = upperfpw[0].upper()
        capsl = ''.join(upperfpw)
    elif case == 2:
        upperpw = pword.upper()
        togglelu, toggleul = [list(pword) for i in range(2)]
        for l in xrange(len(togglelu)):
            if l % 2 == 0:
                togglelu[l] = togglelu[l].upper()
            else:
                toggleul[l] = toggleul[l].upper()
        capsl = [upperpw, ''.join(togglelu), ''.join(toggleul)]
    return capsl


def leetify(pword):
    dic = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    leeted = False
    pchars = list(pword)
    for x in xrange(len(pchars)):
        if dic.get(pchars[x].lower(), None):
            pchars[x] = dic[pchars[x].lower()]
            leeted = True
    if leeted:
        return ''.join(pchars)
    else:
        return None


def mangler(args):
    mangled = list(args.string)
    series = ('1', '12', '123', '1234', '12345', '123456', '!', '@', '#', '$', '%')
    year = datetime.datetime.now().year
    series += tuple((str(year - i) for i in xrange(3)))
    perm = False
    l = len(mangled)
    if l > 1:
        perml, mang2, perml2 = [[] for i in range(3)]
        mang2 = [caps(mangled[i], 1) for i in xrange(len(mangled))]
        for i in xrange(2, l + 1):
            perml += list(permutations(mangled, i))
            perml2 += list(permutations(mang2, i))
        mangled += [''.join(perml[i]) for i in xrange(len(perml))]
        perm = True
    for i in xrange(len(mangled)):
        mangled += [caps(mangled[i], 1)] + caps(mangled[i], 2)
    if perm:
        mangled += [''.join(perml2[i]) for i in xrange(len(perml2))]
    if args.leet:
        for i in xrange(len(mangled)):
            leeted = leetify(mangled[i])
            if (leeted is not None) and (leeted not in mangled):
                mangled.append(leetify(mangled[i]))
    for i in xrange(len(mangled)):
        mangled += [(mangled[i] + k) for k in series] + [(k + mangled[i]) for k in series]
    return mangled


def main():
    parser = argparse.ArgumentParser(description='Simple brute-force / fuzzing dictionary generator')
    parser.add_argument('string', nargs='+')
    parser.add_argument('-b', '--bad', action='store_true', default=False, help='Include a list of bad passwords')
    parser.add_argument('-l', '--leet', action='store_true', default=False, help='l3371fy')
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('a'), dest='FILE', const='mangle.dic',
    default=sys.stdout, help='Write output to FILE, append if already exists')
    args = parser.parse_args()
    mangled = mangler(args)
    if args.bad:
        badpws = ('123456', '1234567', '12345678', '123456789', '1234567890', 'password', 'password1', 'password12',
        'password123', 'passw0rd', 'qwerty', 'abc123', '121212', '123123', '111111', '654321')
        mangled += badpws
    args.FILE.writelines("%s\n" % i for i in mangled)


if __name__ == "__main__":
    main()
