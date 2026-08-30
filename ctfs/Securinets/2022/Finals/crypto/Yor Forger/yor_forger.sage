#!/usr/bin/env sage
import json, hashlib
from secret import FLAG, SECRET

def hash(msg):
    return hashlib.sha256(msg.encode()).hexdigest()

class Shamir:
    def __init__(self, p, n, k):
        """
        p = prime number for modulo operations in Z_p
        n = number of shares
        k = minimum number of shares required to reconstruct the secret
        """
        self.p = p
        self.n = n
        self.k = k
        self.secret = int(hash(SECRET), 16)
        self.coeffs = [self.secret]
        self.shares = []
        self.poly = None

    def generate_shares(self):
        for _ in range(self.k-1):
            self.coeffs.append(randint(1, round(sqrt(self.p))))

        P = PolynomialRing(GF(self.p), "x")
        x = P.gen()
        self.poly = sum(c*x^i for i, c in enumerate(self.coeffs))

        for _ in range(self.n):
            xs = randint(1, 2^54)
            ys = self.poly(x=xs)
            self.shares.append((xs, ys))

    def get_share(self, i):
        return self.shares[i]

    def reconstruct_secret(self, shares):
        P = PolynomialRing(GF(self.p), 'x')
        x = P.gen()
        try:
            reconst_poly = P.lagrange_polynomial(shares)
            return reconst_poly(0)
        except:
            print("Invalid shares.")
            sys.exit()


if __name__ == "__main__":
    p = random_prime(2^512-1, False, 2^(512-1))
    sss = Shamir(p, 10, 5)
    sss.generate_shares()
    
    print("Here is 4 trusted shares :")
    shares = []
    for i in range(4):
        shares.append(sss.get_share(i))
    print({"p": p, "shares": shares})

    try:
        resp = json.loads(input("\nSend your share : "))
        xs, ys = int(resp['xs']), int(resp['ys'])
        assert 1 <= xs <= p-1 and 1 <= ys <= p-1
    except:
        print("You must send data using the expected format.")
        sys.exit()

    shares.append((xs, ys))
    if sss.reconstruct_secret(shares) == int(hash("gimme flag"), 16):
        print(f"Well done! Here is your flag {FLAG}")
    else:
        print("Not even close.")