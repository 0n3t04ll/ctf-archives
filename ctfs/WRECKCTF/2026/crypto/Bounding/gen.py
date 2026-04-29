"""
Out on the red-dirt plains of Z_p*, an old bushman keeps two kangaroos.

  - Tame Roo bounds predictably from a known paddock.
  - Wild Roo was sighted somewhere downrange, and hops only a modest number
    of times before bedding down for the night.

The bushman refuses to say where Wild Roo started, but he'll swear on his
akubra that she hopped no more than MAX_HOPS times from the front gate.

He left his flag in the pouch of Wild Roo, encrypted to her silhouette.
"""

from Crypto.Util.number import getPrime, bytes_to_long, isPrime
import secrets


def safe_prime(bits):
    while True:
        q = getPrime(bits - 1)
        p = 2 * q + 1
        if isPrime(p):
            return p, q


p, q = safe_prime(1024)

# the paddock's front gate: a generator of the order-q subgroup
while True:
    h = secrets.randbelow(p - 3) + 2
    g = pow(h, 2, p)
    if g != 1 and pow(g, q, p) == 1:
        break

# Wild Roo hops no more than this many times before turning in
MAX_HOPS = 1 << 44

# the hidden hop count
hops = secrets.randbelow(MAX_HOPS)

# where Wild Roo was last seen (her silhouette on the horizon)
silhouette = pow(g, hops, p)

# ElGamal-wrap the flag to Wild Roo's silhouette
flag = open("flag.txt", "rb").read().strip()
m = bytes_to_long(flag)
assert m < p

k = secrets.randbelow(q - 1) + 1
c1 = pow(g, k, p)
c2 = (m * pow(silhouette, k, p)) % p

with open("output.txt", "w") as f:
    f.write(f"p = {p}\n")
    f.write(f"g = {g}\n")
    f.write(f"MAX_HOPS = {MAX_HOPS}\n")
    f.write(f"silhouette = {silhouette}\n")
    f.write(f"c1 = {c1}\n")
    f.write(f"c2 = {c2}\n")
