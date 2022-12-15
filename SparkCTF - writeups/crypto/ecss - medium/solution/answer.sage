from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from ecdsa import NIST256p
from ecdsa.ellipticcurve import PointJacobi

blksize = AES.block_size

curve = NIST256p.curve
G = NIST256p.generator
n = NIST256p.order

lines = open('../dist/output.txt', 'r').readlines()
for line in lines:
    exec(line.strip())

ids = [1337, 0x1337, 7331]

matele = []
for id in ids:
    matele += [id ** 2, id, 1]
mat = Matrix(Zmod(n), 3, 3, matele)
matinv = mat ** (-1)

shares = list(map(lambda P: PointJacobi(curve, P[0], P[1], 1), [s1, s2, s3]))
secret_G = PointJacobi(curve, 0, 1, 0)
for i in range(3):
    secret_G += int(matinv[2,i].lift()) * shares[i]
key = long_to_bytes(int((secret_G).x()))[:blksize]

cipher = AES.new(key, AES.MODE_ECB)
plain = unpad(cipher.decrypt(bytes.fromhex(enc)), blksize)

print(plain)
