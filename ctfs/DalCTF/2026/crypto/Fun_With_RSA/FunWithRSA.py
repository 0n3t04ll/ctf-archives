from Cryptodome import *
from Cryptodome.Util.number import *
from pwn import *

FLAG = b"dalctf{REDACTED}"

e = 65537

m = bytes_to_long(FLAG)

while True:
	p = getPrime(256)
	q = getPrime(256)
	n = p*q
	phi = (p-1) * (q-1)

	d = inverse(e, phi)
	if (math.gcd(d,e) == 1):
		break

dp = d % (p-1)
dq = d % (q-1)
qinv = inverse(q, p)

sp = pow(m, dp, p)
sq = pow(m, dq, q)

h = (qinv * (sp - sq)) % p
s = sq + h*q

spz = sp ^ 1

hf = (qinv * (spz - sq)) % p
spz = sq + hf*q


c = pow(m,e,n)
ct = int(xor(bin(c), bin(p), bin(q)),2)

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")
print(f"s = {s}")
print(f"spz = {spz}")