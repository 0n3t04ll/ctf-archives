import json
import secrets
from hashlib import sha256


FLAG = open("flag.txt", "rb").read().strip()
Q_BITS = 192
DEGREE = 6
NUM_SIGS = DEGREE + 2


def long_to_bytes(value):
    if value == 0:
        return b"\x00"
    return value.to_bytes((value.bit_length() + 7) // 8, "big")


def is_probable_prime(n, rounds=16):
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def get_prime(bits):
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate


def safe_prime(bits):
    while True:
        q = get_prime(bits - 1)
        p = 2 * q + 1
        if is_probable_prime(p):
            return p, q


def subgroup_generator(p, q):
    while True:
        h = secrets.randbelow(p - 3) + 2
        g = pow(h, 2, p)
        if g != 1 and pow(g, q, p) == 1:
            return g


def H(R, msg, q):
    digest = sha256(long_to_bytes(R) + msg).digest()
    value = int.from_bytes(digest, "big") % q
    return value or 1


def xor_stream(key, nonce, data):
    out = bytearray()
    counter = 0
    while len(out) < len(data):
        block = sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        take = min(len(block), len(data) - len(out))
        out.extend(block[:take])
        counter += 1
    return bytes(a ^ b for a, b in zip(data, out))


def eval_poly(coeffs, x, mod):
    acc = 0
    for coeff in reversed(coeffs):
        acc = (acc * x + coeff) % mod
    return acc


def main():
    p, q = safe_prime(Q_BITS)
    g = subgroup_generator(p, q)

    x = secrets.randbelow(q - 1) + 1
    y = pow(g, x, p)
    coeffs = [secrets.randbelow(q) for _ in range(DEGREE + 1)]

    seen = set()
    records = []
    while len(records) < NUM_SIGS:
        t = secrets.randbelow(q - 1) + 1
        if t in seen:
            continue
        seen.add(t)
        msg = secrets.token_bytes(24)
        k = eval_poly(coeffs, t, q)
        if k == 0:
            continue
        R = pow(g, k, p)
        e = H(R, msg, q)
        s = (k + e * x) % q
        records.append(
            {
                "timestamp": str(t),
                "msg": msg.hex(),
                "R": str(R),
                "s": str(s),
            }
        )

    key = sha256(long_to_bytes(x)).digest()
    nonce = secrets.token_bytes(16)
    ct = xor_stream(key, nonce, FLAG)

    blob = {
        "p": str(p),
        "q": str(q),
        "g": str(g),
        "y": str(y),
        "records": records,
        "nonce": nonce.hex(),
        "ct": ct.hex(),
    }

    with open("output.txt", "w") as f:
        json.dump(blob, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
