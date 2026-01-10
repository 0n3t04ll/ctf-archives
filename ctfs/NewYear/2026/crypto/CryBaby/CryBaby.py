import random
import binascii
import base64

def xor_bytes(a: bytes, b: bytes) -> bytes:
    length = min(len(a), len(b))
    return bytes([a[i] ^ b[i] for i in range(length)])

def encrypt_round(s: str) -> str:
    b = s.encode('utf-8')
    if random.randrange(2) == 0:
        return base64.encodebytes(b).decode('ascii')
    else:
        return binascii.hexlify(b).decode('ascii')

def main():
    flag = b"REDACTED"
    assert len(flag) == 28

    l = flag[:14]
    r = flag[14:]
    xored = xor_bytes(l, r)             
    c = binascii.hexlify(xored).decode('ascii')
    rounds = random.randint(1, 20)

    for _ in range(rounds):
        c = encrypt_round(c)

    with open('chall.txt', 'w', encoding='utf-8') as f:
        f.write(c)

if __name__ == "__main__":
    main()
