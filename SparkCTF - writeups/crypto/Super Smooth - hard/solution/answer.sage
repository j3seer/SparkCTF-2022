from sage.all import *

import sympy
from Crypto.Util.number import *

from sage.rings.factorint import factor_trial_division

# n, e, ct
lines = open("../dist/output.txt", "r").readlines()
for line in lines:
    exec(line.strip())

p_24bit = list(sympy.primerange(2**23, 2**24))

g = 3

fact = []

## find largest factor
g_pow = pow(g, 2**2, n)
g_pow_lst = []
for smallp in p_24bit:
    for _ in range(6):
        g_pow = pow(g_pow, smallp, n)
    g_pow_lst.append((smallp, g_pow))
    if g_pow == 1:
        fact.append(smallp)
        break

## find second large factor
for idx in range(len(g_pow_lst)-2, -1, -1):
    smallp, g_pow = g_pow_lst[idx]
    for _ in range(6):
        g_pow = pow(g_pow, fact[0], n)
    if g_pow != 1:
        fact.append(presmallp)
        break
    presmallp = smallp
    
assert len(fact) == 2

print("compute two factor is done")
print(fact)

partfactphi = n // ((fact[0]**(6*2)) * (fact[1]**(5*2))) # equals phi / ((fact[0]**(6*2)) * (fact[1]**(5*2)))
print(partfactphi)

print(factor_trial_division(partfactphi, 2**24))

phi = partfactphi * ((fact[0]**(6*2)) * (fact[1]**(5*2)))
d = pow(e, -1, phi)

print(long_to_bytes(int(pow(ct, int(d), n))))
