from Crypto.PublicKey import ECC
from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b, inverse
import hashlib, os

FLAG = os.environ.get("FLAG", "KSUS{dummy_flag_for_testing}")
FLAG_CMD = b"retrieve_flag"
G = ECC.EccPoint(
    x=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    y=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
    curve="P-256"
)
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

def sign(message: bytes, d: int) -> tuple:
    h_bytes = hashlib.sha256(message).digest()
    h = b2l(h_bytes)
    k_hash = hashlib.sha512(l2b(d) + message).digest()
    k = b2l(k_hash) % (1 << 128)
    
    if k == 0:
        return sign(message + b"\x00", d)
        
    R = k * G
    r = int(R.x) % n
    
    if r == 0:
        return sign(message + b"\x00", d)
        
    s = (inverse(k, n) * (h + d * r)) % n

    if s == 0:
        return sign(message + b"\x00", d)
    
    return (r, s)

def verify(message: bytes, r: int, s: int, P: ECC.EccPoint) -> bool:
    if not (1 <= r < n and 1 <= s < n):
        return False
    
    w = inverse(s, n)
    current_msg = message

    for _ in range(4):
        h_bytes = hashlib.sha256(current_msg).digest()
        h = b2l(h_bytes)
        u1 = (w * h) % n
        u2 = (w * r) % n
        Q = u1 * G + u2 * P

        if int(Q.x) % n == r:
            return True
        
        current_msg += b"\x00"

    return False

def main():
    MAX_SIGNS = 3
    signatures_used = 0
    d = b2l(os.urandom(32)) % n
    P = d * G
    
    print(f"I've generated a completely unforgeable Public Key (x, y): ({hex(int(P.x))}, {hex(int(P.y))})", flush=True)
    
    while True:
        print(f"1. Politely request a signature ({MAX_SIGNS - signatures_used} remaining)", flush=True)
        print("2. Attempt to claim the flag", flush=True)
        print("3. Leave gracefully", flush=True)
        
        choice = input("> ").strip()
            
        if choice == '1':
            if signatures_used >= MAX_SIGNS:
                print("Sorry, the oracle is tired. No more signatures for you.", flush=True)
                continue
                
            msg = bytes.fromhex(input("Feed me your finest hex bytes: ").strip())

            if FLAG_CMD in msg:
                print("Nice try, but I don't sign that specific command. Catch you later! :3", flush=True)
                break

            r, s = sign(msg, d)
            print(f"Behold, a flawless signature (r, s): ({hex(r)}, {hex(s)})", flush=True)

            signatures_used += 1
                
        elif choice == '2':
            print(f"Alright, let's see your 'valid' signature for '{FLAG_CMD.decode()}'...", flush=True)
            r = int(input("Provide r (hex or decimal): ").strip(), 0)
            s = int(input("Provide s (hex or decimal): ").strip(), 0)
            
            if verify(FLAG_CMD, r, s, P):
                print(f"Wait, what? How did you...ugh, fine. Here is your flag: {FLAG}", flush=True)
            else:
                print("Math checks out...as completely invalid. Better luck next time! :3", flush=True)

            break
                
        elif choice == '3':
            print("Giving up so soon? Goodbye.", flush=True)
            break
        else:
            print("That's not even a valid menu option. Focus!", flush=True)

if __name__ == "__main__":
    main()