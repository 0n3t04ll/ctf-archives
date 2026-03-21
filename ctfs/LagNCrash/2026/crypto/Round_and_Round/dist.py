import base64 as _b
import random

def __(): return 1337

class _PRNG:
    def __init__(s, x): s._ = x & 0xFFFFFFFF
    def __call__(s):
        s._ ^= (s._ << 13) & 0xFFFFFFFF
        s._ ^= (s._ >> 17)
        s._ ^= (s._ << 5) & 0xFFFFFFFF
        return s._ & 0xFFFFFFFF

def _F(r, k, st):
    z = (r ^ (k & 0xFF))
    z = (z * 173 + 41) & 0xFF
    q = st & 7
    return ((z << q) | (z >> (8 - q))) & 0xFF

def _f(data, g, rounds=6):
    s = g()
    out = []
    if len(data) & 1: data.append(0)
    i = 0
    while i < len(data):
        L, R = data[i], data[i+1]
        for _ in range(rounds):
            k = g()
            L, R = R, L ^ _F(R, k, s)
            s = (s + k + R) & 0xFFFFFFFF
        out.extend([L,R])
        i += 2
    return out

def _p(data, g):
    n = len(data)
    idx = list(range(n))
    for i in range(n):
        j = g() % n
        idx[i], idx[j] = idx[j], idx[i]
    out = [0]*n
    for i,p in enumerate(idx):
        out[p] = data[i]
    return out

def _enc(flag):
    seed = random.randint(0, 0xFFFF)
    prng = _PRNG(seed)
    
    y = list(map(ord, flag))
    y = _f(y, prng, rounds=6)
    y = _p(y, prng)
    y = [(b % 95) + 32 for b in y]
    
    return _b.b64encode(bytes(y)).decode()

if __name__ == "__main__":
    F = "LNC26{fake_flag}"
    ef = _enc(F)
    
    with open("flag.enc", "w") as f:
        f.write(ef)