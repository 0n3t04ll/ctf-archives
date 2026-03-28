from sage.all import *
import sys
from ast import literal_eval

import hashlib
import os
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def double(A24, P):
    X, Z = P
    XpZ=X+Z
    XmZ=X-Z
    a=(XpZ)*(XpZ) 
    b=(XmZ)*(XmZ)
    c=a-b
    X2=a*b
    Z2=c*(b+A24*c)
    return (X2, Z2)

def diff_add(P, Q, PmQ):
    XP, ZP = P
    XQ, ZQ = Q
    XPmQ, ZPmQ = PmQ
    a=XP+ZP
    b=XP-ZP
    c=XQ+ZQ
    d=XQ-ZQ
    da = d*a
    cb = c*b
    dapcb = da+cb
    damcb = da-cb
    XPQ=dapcb*dapcb * ZPmQ
    ZPQ=damcb*damcb * XPmQ
    return (XPQ, ZPQ)

def ladder(A24, P, n):
    n = abs(n)
    P1, P2 = (1, 0), P
    if n == 0:
        return P1, P2
    for bit in bin(n)[2:]:
        Q = diff_add(P2, P1, P)
        if bit == "1":
            P2 = double(A24, P2)
            P1 = Q
        else:
            P1 = double(A24, P1)
            P2 = Q
    return P1

def keygen(A, G, ord_G, s=None):
    if not s:
        s = secrets.randbelow(ord_G)
    A24 = (A+2)/4
    P = ladder(A24, G, s)
    return s, P

def derive_secret(A, Pub, sk):
    A24 = (A+2)/4
    R = ladder(A24, Pub, sk)
    return int(R[0]/R[1])

def encrypt(shared_secret, msg):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(msg, 16))
    return iv.hex(), ciphertext.hex()

FLAG = b"kalmar{???}"

def main():
    p = 340824640496360275329125187555879171429601544029719477817787
    F = GF(p)
    A = F(285261811835788437932082156343256480312664037202203048186662)
    ord_G = 42603080062045034416140648444405950943345472415479119301079

    G = (F(2024), F(1))

    s_A = secrets.randbelow(ord_G)
    print(f"{encrypt(s_A, FLAG)}")
    print(f"Please take good care of the secret above, I need you to deliver it to our allies. It is above your paygrade though...")
    print(f"HoweverI have a message for you too!") 

    msg = b"attack at dawn"
    while True:
        #I won't screw up again! Better include some state of the art side channel protection 8)
        #I'll even use TWO countermeasures from https://schaumont.dyn.wpi.edu/schaum/pdf/papers/2010hostf.pdf

        #Step 1: blinding!
        blind = randint(1, ord_G)
        s_A_protected = s_A*blind

        #Step 2: Add multiple of order!
        s_A_protected += secrets.randbelow(2**64)*ord_G

        #BWAHAHA good luck now!!

        _, p_A = keygen(A, G, ord_G, s=s_A_protected)
        print(f"\nHere is my public key: {p_A}")
        print(f"blinding: {blind}")

        print("Please send yours (format: (X, Z)):")
        answer = literal_eval(sys.stdin.readline().strip())
        p_B = tuple([F(c) for c in answer])

        ss = derive_secret(A, p_B, s_A_protected)
        iv, ct = encrypt(ss, msg)
        print(f"{(iv, ct)}")
        print(f"Did you get the message? If not, I can send again")

if __name__ == "__main__": 
    main()
