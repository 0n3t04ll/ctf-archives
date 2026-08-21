from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
from itertools import batched
import hashlib
import os
import secrets

class PaillierSystem:
    def __init__(self, p, q):
        self.n = p * q
        self.n_sq = self.n * self.n
        self.g = self.n + 1
        self.lmb = (p - 1) * (q - 1)
        self.mu = pow(self.lmb, -1, self.n)

    def encrypt(self, m):
        r = secrets.randbelow(self.n - 2) + 2
        
        gm = 1 + m * self.n
        rn = pow(r, self.n, self.n_sq)
        
        return (gm * rn) % self.n_sq

    def decrypt(self, c):
        u = pow(c, self.lmb, self.n_sq)
        L_u = (u - 1) // self.n
        return (L_u * self.mu) % self.n

class Damwan:
    def __init__(self, p, q, ratings):
        self.paillier = PaillierSystem(p, q)
        self.ratings = ratings

    def step_1_encrypt_profile(self):
        profile = []
        for val in self.ratings:
            if val != 0:
                profile.append(self.paillier.encrypt(val))
        return profile


class Tao:
    def __init__(self, table):
        self.table = table

    def generate_recommendations(self, damwan_pub, profile):
        payload = []
        totals = []
        n_sq = damwan_pub.n_sq
        
        for row in self.table:
            acc = 1
            total = 0
            
            for c, s in zip(profile, row):
                assert s >= 0

                acc = (acc * pow(c, s, n_sq)) % n_sq
                total += s
            
            payload.append(acc)
            totals.append(total)
            
        return payload, totals

ROWS = 5
COLS = 40
PRIME_BITS = 1024
FLAG = os.environ.get("FLAG", "flag").encode()

# Implementation of https://publications.tno.nl/publication/102853/WnMly5/erkin-2012-privacy.pdf
if __name__ == "__main__":
    # We are semi-honest, so we must follow the protocol exactly as described
    assert ROWS > 0
    assert COLS >= 2

    p = getPrime(PRIME_BITS)
    q = getPrime(PRIME_BITS)
    while p == q:
        q = getPrime(PRIME_BITS)

    assert p.bit_length() == PRIME_BITS
    assert q.bit_length() == PRIME_BITS
    print(p)
    print(q)
    
    seed = secrets.token_bytes(ROWS * COLS)
        
    prefs = []
    for i in range(COLS):
        print(f"rating i{i} = ")
        rating = int(input())
        assert 1 <= rating <= 5
        prefs.append(rating)

    table = [[b + 1 for b in row] for row in batched(seed, COLS)]

    damwan = Damwan(p, q, prefs)
    tao = Tao(table)

    profile = damwan.step_1_encrypt_profile()
    print(profile)

    payload, totals = tao.generate_recommendations(
        damwan.paillier,
        profile,
    )

    print(payload)
    print(totals)
    key = hashlib.sha256(seed).digest()
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
    ct = cipher.encrypt(FLAG).hex()
    print(ct)
