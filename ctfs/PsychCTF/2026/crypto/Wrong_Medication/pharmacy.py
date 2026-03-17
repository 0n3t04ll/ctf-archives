#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║   PSYCH WARD AUTOMATED PHARMACY v2.1                    ║
║   Patient Authentication Terminal                       ║
╚══════════════════════════════════════════════════════════╝

Authenticate via Elliptic-Curve Diffie–Hellman key exchange.
The pharmacy server holds the private key; you hold the public key.
Exchange a point to derive the shared secret.
"""
import sys

# ===== Curve parameters (public) =======================================
P     = 281474976710677          # field prime (48-bit)
A     = 2                        # curve coefficient a
B     = 3                        # curve coefficient b  ← displayed only
G     = (0, 177681339988538)     # generator point
ORDER = 8278676010679            # generator order

# ===== Pharmacy private key (SECRET) ====================================
d     = 597561114
Q     = (119507153144501, 37069259253313)   # d * G

# ===== Encrypted flag ====================================================
# Decrypt with: AES-ECB( SHA256(d.to_bytes(16,'big'))[:16] , enc )
ENCRYPTED_FLAG_HEX = (
    "cdae39f8460cceafc1b2a14af55b831f"
    "7ffa1badaec839ee8f3f616f22125cab"
    "2b8272079e459db6c9bd1825218eeea9"
    "da840108443416de5a883251ad349dfb"
)

# ===== ECC arithmetic (pure Python, no external deps) ====================

def modinv(a, m):
    """Modular inverse via built-in pow (Python 3.8+)."""
    return pow(a, -1, m)

def point_add(P1, P2):
    """Add two points on the curve.  Uses only A and P — never B."""
    if P1 is None: return P2
    if P2 is None: return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2:
        if y1 == y2:
            return point_double(P1)
        return None             # P + (−P) = point at infinity
    lam = (y2 - y1) * modinv(x2 - x1, P) % P
    x3  = (lam * lam - x1 - x2) % P
    y3  = (lam * (x1 - x3) - y1) % P
    return (x3, y3)

def point_double(pt):
    """Double a point on the curve.  Uses only A and P — never B."""
    if pt is None: return None
    x, y = pt
    if y == 0: return None
    lam = (3 * x * x + A) * modinv(2 * y, P) % P
    x3  = (lam * lam - 2 * x) % P
    y3  = (lam * (x - x3) - y) % P
    return (x3, y3)

def scalar_mult(k, pt):
    """Double-and-add scalar multiplication."""
    result  = None
    addend  = pt
    while k > 0:
        if k & 1:
            result = point_add(result, addend)
        addend = point_double(addend)
        k >>= 1
    return result

# ===== Server loop =======================================================

def banner():
    print("=" * 58)
    print("  PSYCH WARD AUTOMATED PHARMACY v2.1")
    print("  Patient Authentication Terminal")
    print("=" * 58)
    print()
    print(f"  Curve: y² = x³ + {A}·x + {B}  (mod {P})")
    print(f"  Generator  G = {G}")
    print(f"  Curve order  = {ORDER}")
    print(f"  Pharmacy key Q = {Q}")
    print()
    print(f"  Encrypted master record:")
    print(f"  {ENCRYPTED_FLAG_HEX}")
    print()
    print("  Authenticate by performing an ECDH key exchange.")
    print(f"  You have 100 attempts.")
    print()

def main():
    banner()
    for i in range(100):
        try:
            print(f"[Query {i+1}/100]")
            sys.stdout.flush()
            x = int(input("Enter point x: ").strip())
            y = int(input("Enter point y: ").strip())

            S = scalar_mult(d, (x, y))

            if S is None:
                print("Shared secret: Point at infinity")
            else:
                print(f"Shared secret: ({S[0]}, {S[1]})")
            print()
        except (ValueError, KeyboardInterrupt, EOFError) as e:
            print(f"Error: {e}")
            print()

    print("Maximum queries reached.  DISPENSARY LOCKED.")

if __name__ == "__main__":
    main()
