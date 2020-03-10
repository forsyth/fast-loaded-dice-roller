# Released under Apache 2.0; refer to LICENSE.txt

from collections import namedtuple
from math import ceil
from math import log2
from random import getrandbits

fldr_s = namedtuple('fldr_s', ['n', 'm', 'k', 'r', 'h', 'H'])

def flip():
    return getrandbits(1)

def fldr_preprocess(a):
    n = len(a)
    m = sum(a)
    k = ceil(log2(m))
    r = (1 << k) - m

    h = [0] * k
    H = [[-1]*k for _i in range(n+1)]
    for j in range(k):
        d = 0
        for i in range(n):
            w = (a[i] >> ((k-1) - j)) & 1
            h[j] += (w > 0)
            if w > 0:
                H[d][j] = i
                d += 1
        w = (r >> ((k-1) - j)) & 1
        h[j] += (w > 0)
        if w > 0:
            H[d][j] = n

    return fldr_s(n, m, k, r, h, H)

def fldr_sample(x):
    n, h, H = x.n, x.h, x.H
    if n == 1:
        return 0
    d = 0
    c = 0
    while True:
        b = flip()
        d = 2*d + (1 - b)
        if d < h[c]:
            z = H[d][c]
            if z < n:
                return z
            else:
                d = 0
                c = 0
        else:
            d = d - h[c]
            c = c + 1