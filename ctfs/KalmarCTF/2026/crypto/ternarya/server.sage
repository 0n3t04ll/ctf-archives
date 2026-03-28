import json

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
K = GF(p)
F = GF(q)
a = K(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc)
b = K(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b)
E = EllipticCurve(K, (a, b))
E.set_order(q)

G = E(
    0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
)
H = E(
    0x3572dd8996acc4c4b9ea5c61363292dd9b2d36cc4e644fa4454aad7eea6a90ea,
    0xab16f00d7fdc72d4d65401d97d4f1b3d6f5790b67a045e27659b215d7e529690
)

def com(v: F, r: F):
    assert v in F
    assert r in F
    return v * G + r * H

# Ternary Membership Proof
class Prover:
    def __init__(self, m: F, r: F):
        assert m in (0, 1, 2), 'not ternary'
        self.m = m
        self.a = F.random_element()
        self.rC = r
        self.rCa = F.random_element()
        self.rCx = F.random_element()
        self.rC0 = F.random_element()

    def A(self):
        a = self.a
        m = self.m
        Ca = com(a, self.rCa)
        Cx = com(3*a*m - 2*a*m^2, self.rCx)
        C0 = com(-a^2*m, self.rC0)
        return [Ca, Cx, C0]

    def Z(self, x: F):
        f = x * self.m + self.a
        s = (x - f) * (2*x - f)
        za = x * self.rC + self.rCa
        zb = s * self.rC + x * self.rCx + self.rC0
        return [f, za, zb]

def verify(C: E, tx):
    # unpack transcript
    A, x, Z = tx

    # decode A
    Ca, Cx, C0 = A
    Ca, Cx, C0 = E(Ca), E(Cx), E(C0)

    # decode Z
    f, za, zb = Z
    f, za, zb = F(f), F(za), F(zb)

    # check proof
    s = (x - f) * (2*x - f)
    assert x*C + Ca == com(f, za), 'f is invalid'
    assert s*C + x*Cx + C0 == com(0, zb), 'non-zero eval'

def send(m):
    print(json.dumps(m))

def recv():
    return json.loads(input())

# take the commitments
send('provide commitments')
Cs = recv()
Cs = [E(x,y) for (x, y) in Cs]
assert len(Cs) > 0

# get first round msg
send('provide first round messages')
As = recv()
assert len(As) == len(Cs)

# send challenge
x = F.random_element()
send(int(x))

# get response
xs, Zs = recv()
xs = [F(xi) for xi in xs]
assert len(Zs) == len(Cs)
assert len(xs) == len(Cs)
assert sum(xs) == x

# verify every transcript
for (C, pf) in zip(Cs, zip(As, xs, Zs)):
    verify(C, pf)

# now provide openings:
send('proofs okay')
opens = recv()
assert len(opens) == len(Cs)

# every opening should be different from 0/1/2
for (C, (m, r)) in zip(Cs, opens):
    m = F(m)
    r = F(r)
    assert m not in (0, 1, 2)
    assert C == com(m, r)

# okay, you win ;)
send(open('flag.txt', 'r').read())
