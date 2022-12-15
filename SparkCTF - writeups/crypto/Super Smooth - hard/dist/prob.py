from os import urandom
from random import randint
from Crypto.Util.number import *


def gen_two_primes():
    while (True):
        smallps = [getPrime(24) for _ in range(10)]
        if len(set(smallps)) != 10:
            continue
        smallps = sorted(smallps)
        pm1 = (smallps[0] ** 4) * (smallps[1] ** 3) * (smallps[8] ** 5) * (smallps[9] ** 6) * smallps[2] * smallps[4] * smallps[6]
        qm1 = (smallps[0] ** 4) * (smallps[1] ** 3) * (smallps[8] ** 5) * (smallps[9] ** 6) * smallps[3] * smallps[5] * smallps[7]
        pm1 *= 2
        qm1 *= 2
        p = pm1 + 1
        q = qm1 + 1
        if isPrime(p) and isPrime(q):
            return (p, q)
        continue

p, q = gen_two_primes()
n = p * q
e = 0x10001

nbytelen = (n.bit_length() + 7) // 8

flag = open("flag.txt", "rb").read().strip()
padlenup = randint(1, nbytelen - len(flag) - 1)
flag_ = urandom(padlenup) + flag + urandom(nbytelen - len(flag) - padlenup - 1)

ct = pow(bytes_to_long(flag_), e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

