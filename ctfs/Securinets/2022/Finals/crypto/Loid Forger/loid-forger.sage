#!/usr/bin/env sage
import json, hashlib, string
from secret import FLAG

"""
I read that BLS Signature scheme is strongly unforgeable.
I couldn't find any ressources on its implementation,
so i did implemented it by myself to test it for our Authentication System.
"""

# BLS12-381 Parameters
p = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
r = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001
h1 = 0x396c8c005555e1568c00aaab0000aaab
h2 = 0x5d543a95414e7f1091d50792876a202cd91de4547085abaa68a205b2e5a7ddfa628f1cb4d9e82ef21537e293a6691ae1616ec6e786f0c70cf1c38e31c7238e5

F1 = GF(p)
F2.<i> = GF(p^2, modulus=x^2 + 1)
F12.<ii> = GF(p^12, modulus=x^12 - 2*x^6 + 2)

E1 = EllipticCurve(F1, [0, 4])
E2 = EllipticCurve(F2, [0, 4*(1+i)])
E12 = EllipticCurve(F12, [0, 4])

G1x = 0x17f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb
G1y = 0x8b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1
G2x0 = 0x24aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8
G2x1 = 0x13e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e
G2y0 = 0xce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801
G2y1 = 0x606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be
G1 = E1(G1x, G1y)
G2 = E2(G2x0 + i*G2x1, G2y0 + i*G2y1)

class BLS():
    def __init__(self):
        self.d = randint(1, p-1)
        self.pub = self.public()

    def lift_E1_to_E12(self, P):
        if P.curve() != E1:
            print(f"Point is not on the curve E1.")
            sys.exit()
        return E12(P)

    def lift_E2_to_E12(self, P):
        if P.curve() != E2:
            print(f"Point is not on the curve E2.")
            sys.exit()
        x, y = [c.polynomial().coefficients() for c in (h2*P).xy()]
        X = F12(x[0] - x[1] + ii ^ 6*x[1])
        Y = F12(y[0] - y[1] + ii ^ 6*y[1])
        return E12(X / (ii ^ 2), Y / (ii ^ 3))

    def public(self):
        return self.d*G1

    def hash(self, pad, msg):
        return hashlib.sha512(str(msg + pad).encode()).hexdigest()

    def hash_to_point(self, msg):
        pad = 0
        m = int(msg, 16)
        H = self.hash(pad, m)
        while True:
            try:
                Hx = int(H, 16) % p
                return m*E2.lift_x(Hx)
            except:
                pad += 1
                pad %= 256
                H = self.hash(pad, Hx)

    def pairing(self, A, B):
        return A.ate_pairing(B, r, 12, E12.trace_of_frobenius())

    def sign(self, msg):
        P = self.hash_to_point(msg)
        S = self.d*P
        if S.is_zero():
            return 0x0, 0x0, 0x1, 0x0
        Sx, Sy = [c.polynomial().coefficients() for c in S.xy()]
        return Sx[0], Sx[1], Sy[0], Sy[1]

    def verify(self, msg, sig):
        _P = self.lift_E2_to_E12(self.hash_to_point(msg))
        _pub = self.lift_E1_to_E12(self.pub)
        _G1 = self.lift_E1_to_E12(G1)
        _sig = self.lift_E2_to_E12(sig)
        return self.pairing(_pub, _P) == self.pairing(_G1, _sig)

welcome = """
  ┌─────────────────────┐
  | ┌──(SD@ctf)-[~]     |
  | └─$ ./loid-forger   |
  |                     |
  |       By Aptx       |
  └─────────────────────┘"""
print(welcome)

if __name__ == "__main__":
    bls = BLS()
    challenge = b"Securiday2K22"

    while True:
        print("\n1- Sign")
        print("2- Verify")
        print("3- Exit")
        c = input("> ")

        if c == '1':
            try:
                resp = json.loads(input("Send your message to sign (hex format) : "))
                msg = bytes.fromhex(resp["message"])
            except:
                print("You must send data using the expected format.")
                sys.exit()

            if challenge in msg:
                print("Sorry, i can't sign this message for you.")
                sys.exit()

            Sx0, Sx1, Sy0, Sy1 = bls.sign(msg.hex())
            print({"signature": [Sx0, Sx1, Sy0, Sy1]})

        elif c == '2':
            try:
                resp = json.loads(input(f"Send the signature for '{challenge.decode()}' : "))
                sig = resp["signature"]
                assert all(int(coord) for coord in sig)
                Sx0, Sx1, Sy0, Sy1 = sig
            except:
                print("You must send data using the expected format.")
                sys.exit()

            try:
                S = E2(Sx0 + i*Sx1, Sy0 + i*Sy1)
            except:
                print(f"Point is not on the curve E2.")
                sys.exit()

            if bls.verify(challenge.hex(), S):
                print(f"YOU FORGED IT! Here is your flag {FLAG}")
            else:
                print("Invalid Signature.")
            sys.exit()

        elif c == '3':
            print("Goodbye.")
            sys.exit()

        else:
            print("Invalid choice.")