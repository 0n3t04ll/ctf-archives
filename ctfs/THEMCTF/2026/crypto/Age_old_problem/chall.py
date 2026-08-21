import secrets
from math import gcd
from Crypto.Util.number import isPrime, bytes_to_long


def egcd(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    return old_r, old_x, old_y


def find_c2_d2(c1: int, d1: int):
    """
    Find integers (c2, d2) such that c1*c2 - d1*d2 == 1.
    """
    if gcd(c1, d1) != 1:
        raise ValueError

    g, x, y = egcd(c1, d1)
    assert g == 1

    c2 = x
    d2 = -y

    assert c1 * c2 - d1 * d2 == 1
    return c2, d2


# https://math.stackexchange.com/questions/4653735/given-an-integer-n-how-to-locate-divisors-p-q-such-that-pq-bmod-pq
BITS = 1024

while True:
    c1 = secrets.randbits(BITS) | (1 << (BITS - 1))
    d1 = secrets.randbits(BITS) | (1 << (BITS - 1))

    if gcd(c1, d1) != 1:
        continue

    try:
        c2, d2 = find_c2_d2(c1, d1)
    except ValueError:
        continue

    k = c1 * d2 + c2 * d1
    a = c1 * c1 + d1 * d1
    b = c2 * c2 + d2 * d2

    p = a + k
    q = b + k

    if p <= 0 or q <= 0:
        continue

    if p % 4 != 3 or q % 4 != 3:
        continue

    if not isPrime(p) or not isPrime(q):
        continue

    N = p * q

    e = (1 - (k * b % a)) % a

    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        continue

    assert N % (p + q) == 1

    flag = bytes_to_long(open("flag.txt", "rb").read())
    assert flag < N

    ct = pow(flag, e, N)
    print("N =", N)
    print("e =", e)
    print("ct =", ct)
    break