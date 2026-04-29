#!/usr/bin/env python3
import hashlib, random, sys

def _g(seed, n):
    r = random.Random(seed); l = list(range(n)); r.shuffle(l); return l

_S = _g(0xBEEF1234, 256)
_P = _g(0xCAFEBABE, 32)


class _0:
    def __init__(s, k): s.k = bytes(k)
    def f(s, x):
        k = s.k
        for i in range(len(x)): x[i] ^= k[i % len(k)]

class _1:
    def __init__(s, k): s.k = bytes(k)
    def f(s, x):
        k = s.k
        for i in range(len(x)): x[i] = (x[i] + k[i % len(k)]) & 0xFF

class _2:
    def __init__(s, k): s.k = bytes(k)
    def f(s, x):
        k = s.k
        for i in range(len(x)): x[i] = (x[i] - k[i % len(k)]) & 0xFF

class _3:
    def __init__(s, a): s.a = a & 7
    def f(s, x):
        a = s.a
        if not a: return
        for i in range(len(x)):
            b = x[i]; x[i] = ((b << a) | (b >> (8 - a))) & 0xFF

class _4:
    def __init__(s, p): s.p = list(p)
    def f(s, x):
        n = bytearray(len(x))
        for i, j in enumerate(s.p): n[i] = x[j]
        x[:] = n

class _5:
    def __init__(s, t): s.t = list(t)
    def f(s, x):
        t = s.t
        for i in range(len(x)): x[i] = t[x[i]]

class _6:
    def f(s, x): x.reverse()

class _7:
    def f(s, x):
        n = len(x) // 2
        a = bytes(x[:n]); x[:n] = x[n:]; x[n:] = a

class _8:
    def f(s, x):
        for i in range(1, len(x)): x[i] ^= x[i - 1]

class _9:
    def __init__(s, k):
        s.k = bytes(k)
        for b in s.k: assert b & 1
    def f(s, x):
        k = s.k
        for i in range(len(x)): x[i] = (x[i] * k[i % len(k)]) & 0xFF


def _mh(a):
    def h(d): return hashlib.new(a, d).digest()[:3]
    return h

class _A:
    h = staticmethod(_mh("md5"))
    def __init__(s, i, e=None): s.i = i; s.e = bytes(e) if e else None
    def f(s, x):
        i = s.i; c = bytes(x[i:i + 3]); d = s.h(c)
        x[i:i + 3] = bytes(p ^ q for p, q in zip(c, d))

class _B(_A):
    h = staticmethod(_mh("sha256"))


_Q = [
    _0(b"BUZZBUZZ"),
    _1(b"\x12\x34\x56\x78\x9a\xbc\xde\xf0"),
    _3(3),
    _5(_S),
    _4(_P),
    _8(),
    _2(b"\x42\x13\x37\x99"),
    _7(),
    _0(b"\xab\xcd\xef\x12"),
    _9([3, 5, 7, 11]),
    _3(2),
    _5(_S),
    _6(),
    _1(b"\x01\x02\x03\x04"),
    _A(4, bytes.fromhex("cfafe4")),
    _4(_P),
    _0(b"\x55\xaa\x55\xaa"),
    _3(1),
    _5(_S),
    _2(b"\x11\x22\x33\x44"),
    _8(),
    _7(),
    _9([3, 11, 13, 17]),
    _B(12, bytes.fromhex("f51d49")),
    _4(_P),
    _6(),
    _0(b"\xf0\x0d\xca\xfe"),
    _1(b"\x77\x88\x99\xaa"),
    _9([5, 9, 11, 13]),
    _3(4),
    _5(_S),
    _2(b"\x99\x55\x33\x11"),
]

_T = bytes.fromhex("34ad7a3e4331511d979f075ee8b4619a1aaee35184cb1f1d933e948631ec9f8e")
_PR = b"wreck{"
_SU = b"}"


def _c(f):
    if not (f.startswith(_PR) and f.endswith(_SU)): return False
    if not all(0x20 <= b <= 0x7E for b in f): return False
    x = bytearray(f)
    for o in _Q: o.f(x)
    return bytes(x) == _T


def main():
    d = sys.stdin.buffer.readline().rstrip(b"\n")
    if len(d) != len(_T):
        print("nope"); return 1
    print("correct!" if _c(d) else "nope"); return 0


if __name__ == "__main__":
    sys.exit(main())
