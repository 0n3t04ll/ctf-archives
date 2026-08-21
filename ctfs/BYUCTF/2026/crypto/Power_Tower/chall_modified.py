import random
import math
from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes
from time import time

# Globals
PRIME_BITS = 16
NUM_PRIMES = 25
NUM_EXPS = 1
EXP_UPPER_BOUND = 25
SECS = 1

def get_challenge():

    while True:
        # Generate NUM_PRIMES unique primes for RSA
        p = list([None]*NUM_PRIMES)
        for i in range(NUM_PRIMES):
            p[i] = getPrime(PRIME_BITS)
            assert p[i] <= 2**PRIME_BITS
            
        if len(set(p)) < NUM_PRIMES:
            continue
        n = math.prod(p)
    
        # Generate random message
        m = int.from_bytes(get_random_bytes(32)) % n

        # Generate a random power tower for exponents
        exps = list(range(3, EXP_UPPER_BOUND))
        random.shuffle(exps)
        assert len(exps) >= NUM_EXPS, "Upper bound is too low"
        
        # Ensure the exponent is valid
        exps = exps[:NUM_EXPS]
        if math.gcd(exps[0], math.prod([q-1 for q in p])) > 1:
            continue
        
        break

    # Compute c
    c = pow(m, exps[0], n)
    
    return [n, m, c, exps]

def main():
    with open("flag.txt", 'r') as file:
        flag = file.readline()
    
    print("It's a race against the clock to decrypt the secret value!")
    print(f"Decrypt the ciphertext within {SECS} second(s) to get the flag.")
    print(f"(Each factor of n is at most 2^{PRIME_BITS})")
    
    n, m, c, exponent_list = get_challenge()
    print(f"n = {n}")
    print(f"c = {c}")
    print(f"e = {"^".join([str(e) for e in exponent_list])}")
    
    start = time()
    guess = int(input("What is m? "))
    elapsed = time() - start
    if elapsed > SECS:
        print("Too slow!")
        exit()
    else:
        if guess != m:
            print("Guess incorrect.")
        else:
            print(f"Correct!!! Here's the flag: {flag}")

main()