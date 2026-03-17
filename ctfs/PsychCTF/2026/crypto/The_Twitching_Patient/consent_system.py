#!/usr/bin/env python3
# FIPS 186-4 compliant ECDSA implementation for consent management

import hashlib
import hmac
import struct
import sys
import os

# ─── secp256k1 curve parameters ───────────────────────────────────────────────
PRIME  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A      = 0
B      = 7
Gx     = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy     = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
ORDER  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
BIT_LENGTH = 256
G = (Gx, Gy)


# ─── ECC primitives ───────────────────────────────────────────────────────────

def modinv(a: int, m: int) -> int:
    """Extended Euclidean Algorithm — modular inverse of a mod m."""
    if m == 1:
        return 0
    m0, x0, x1 = m, 0, 1
    a = a % m
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0


def is_on_curve(point) -> bool:
    """Verify that point lies on the curve."""
    if point is None:
        return True
    x, y = point
    return (y * y - x * x * x - A * x - B) % PRIME == 0


def point_add(P1, P2):
    """Standard Weierstrass point addition."""
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2:
        if y1 != y2:
            return None
        return point_double(P1)
    lam = (y2 - y1) * modinv(x2 - x1, PRIME) % PRIME
    x3 = (lam * lam - x1 - x2) % PRIME
    y3 = (lam * (x1 - x3) - y1) % PRIME
    return (x3, y3)


def point_double(P1):
    """Standard Weierstrass point doubling."""
    if P1 is None:
        return None
    x1, y1 = P1
    if y1 == 0:
        return None
    lam = (3 * x1 * x1 + A) * modinv(2 * y1, PRIME) % PRIME
    x3 = (lam * lam - 2 * x1) % PRIME
    y3 = (lam * (x1 - x3) - y1) % PRIME
    return (x3, y3)


def scalar_mult(k: int, point) -> tuple:
    """Double-and-add scalar multiplication."""
    if not is_on_curve(point):
        raise ValueError("Point is not on curve")
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_double(addend)
        k >>= 1
    return result


# ─── Utilities ────────────────────────────────────────────────────────────────

def constant_time_compare(a: bytes, b: bytes) -> bool:
    """Constant-time byte comparison to prevent timing side-channels."""
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0


def verify_signature(message: bytes, r: int, s: int, public_key) -> bool:
    """Verify an ECDSA signature following SEC 1 v2.0 §4.1.4."""
    if not (1 <= r < ORDER and 1 <= s < ORDER):
        return False
    z = int.from_bytes(hashlib.sha256(message).digest(), 'big')
    z >>= (256 - BIT_LENGTH)
    w = modinv(s, ORDER)
    u1 = z * w % ORDER
    u2 = r * w % ORDER
    point = point_add(scalar_mult(u1, G), scalar_mult(u2, public_key))
    if point is None:
        return False
    return point[0] % ORDER == r


# ─── PRNG ─────────────────────────────────────────────────────────────────────

class SigningPRNG:
    """Deterministic nonce generator based on HMAC-DRBG (simplified).
    Produces cryptographically unpredictable values bound to the
    signing key and message for replay resistance."""

    def __init__(self, private_key_bytes: bytes, curve_order: int):
        self.state = hashlib.sha256(private_key_bytes + b"consent_prng_v3").digest()
        self.order = curve_order
        self.counter = 0

    def generate_k(self, message_hash: bytes) -> int:
        """Generate a per-signature nonce k."""
        self.counter += 1

        # HMAC-based extraction
        h = hmac.new(
            self.state,
            message_hash + struct.pack(">Q", self.counter),
            hashlib.sha256,
        ).digest()

        # Additional mixing round for "extra security"
        v = hmac.new(h, self.state + b"\x01", hashlib.sha256).digest()

        # Update internal state
        self.state = hashlib.sha256(self.state + v + h).digest()

        k_int = int.from_bytes(v[:30], "big")

        # Ensure nonce is within valid range for curve operations
        k = k_int % self.order
        if k == 0:
            k = 1
        return k


# ─── ECDSA ────────────────────────────────────────────────────────────────────

def ecdsa_sign(message_bytes: bytes, private_key_int: int, prng: SigningPRNG):
    z = int.from_bytes(hashlib.sha256(message_bytes).digest(), "big")
    z >>= 256 - BIT_LENGTH

    while True:
        k = prng.generate_k(hashlib.sha256(message_bytes).digest())
        R = scalar_mult(k, G)
        if R is None:
            continue
        r = R[0] % ORDER
        if r == 0:
            continue
        s = modinv(k, ORDER) * (z + r * private_key_int) % ORDER
        if s == 0:
            continue
        return (r, s)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    flag = open("flag.txt", "rb").read().strip()
    d = int.from_bytes(flag, "big")
    Q = scalar_mult(d, G)
    Qx, Qy = Q

    prng = SigningPRNG(flag, ORDER)

    print("=" * 60)
    print("  PSYCH WARD CONSENT MANAGEMENT SYSTEM v3.7")
    print("  Digital Signature Terminal")
    print("=" * 60)
    print()
    print(f"Curve: y^2 = x^3 + {A}*x + {B} (mod {PRIME})")
    print(f"Generator G = ({Gx}, {Gy})")
    print(f"Curve order n = {ORDER}")
    print(f"Head Doctor's verification key Q = ({Qx}, {Qy})")
    print()
    print("Commands:")
    print("  SIGN <message_hex>  — Sign a consent form")
    print("  PUBKEY              — Show public key")
    print("  EXIT                — Terminate session")
    print()
    print(f"You may request up to 200 signatures.")
    print()

    sig_count = 0
    MAX_SIGS = 200

    while sig_count < MAX_SIGS:
        try:
            line = input("> ").strip()
            if not line:
                continue

            parts = line.split(maxsplit=1)
            cmd = parts[0].upper()

            if cmd == "EXIT":
                print("Session terminated. All consent records archived.")
                break
            elif cmd == "PUBKEY":
                print(f"Q = ({Qx}, {Qy})")
            elif cmd == "SIGN":
                if len(parts) < 2:
                    print("CONSENT ERROR: No form data provided.")
                    continue
                msg_hex = parts[1].strip()
                try:
                    msg = bytes.fromhex(msg_hex)
                except Exception:
                    print("CONSENT ERROR: Invalid hex encoding.")
                    continue

                r, s = ecdsa_sign(msg, d, prng)
                sig_count += 1
                print(f"Form #{sig_count} signed.")
                print(f"r = {r}")
                print(f"s = {s}")
            else:
                print("CONSENT ERROR: Unknown command.")
        except EOFError:
            break
        except Exception as e:
            print(f"SYSTEM ERROR: {e}")

    if sig_count >= MAX_SIGS:
        print("Maximum signatures reached. Session terminated.")
    print("DISPENSARY LOCKED.")


if __name__ == "__main__":
    main()
