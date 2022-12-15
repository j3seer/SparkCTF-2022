from os import urandom

from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from ecdsa import NIST256p
from ecdsa.ellipticcurve import PointJacobi


blksize = AES.block_size

G = NIST256p.generator


a1 = bytes_to_long(urandom(32)) 
a2 = bytes_to_long(urandom(32))


secret = bytes_to_long(urandom(32))
key = long_to_bytes(int((secret * G).x()))[:blksize]


def share(id):
    return (a1 * (id**2) + a2 * (id) + secret) * G


s1 = share(1337)
s2 = share(0x1337)
s3 = share(7331)

point_to_lst = lambda P: list(map(int, [P.x(), P.y()]))

print(f"s1 = {point_to_lst(s1)}")
print(f"s2 = {point_to_lst(s2)}")
print(f"s3 = {point_to_lst(s3)}")


flag = open('flag.txt', 'r').read().strip().encode()
cipher = AES.new(key, AES.MODE_ECB)
enc = cipher.encrypt(pad(flag, blksize))

print(f"enc = \"{enc.hex()}\"")
