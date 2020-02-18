from math import gcd


def get_greatest_common_divisor(a, b):
    return gcd(a, b)


def get_longest_substring(a, b):
    candidates = [
        a[i:j]
        for i in range(len(a))
        for j in range(i, len(a))
        if a[i:j] in b
    ] + ['']
    return max(candidates, key=lambda x: len(x))


def get_common_letters(a, b):
    return ''.join(sorted(set(a) & set(b)))

genfuncs = {
    'gcd': get_greatest_common_divisor,
    'common': get_common_letters,
    'substr': get_longest_substring,
}