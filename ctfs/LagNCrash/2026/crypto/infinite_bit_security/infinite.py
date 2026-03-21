from Crypto.Util.number import bytes_to_long, getPrime
from secret import flag
import os
from somewhere import GRAHAMS_NUMBER # eh eventually we'll figure out how to calculate it, right?

def fib(N):
    a, b = 0, 1
    for i in range(N):
        a, b = b, a + b
    return a

def gen_modulus(num):
    i = 1
    for _ in range(num):
        i *= getPrime(32)
    return i

def pad(bytestring, target_length):
    return bytestring + os.urandom(target_length - len(bytestring))

src = fib(GRAHAMS_NUMBER)
modulus = gen_modulus(10000) # yeah this should be enough
secret = bytes_to_long(pad(
    flag, modulus.bit_length() // 8
))
key = src % modulus
enc = secret ^ key

import sys
sys.set_int_max_str_digits(2 ** 20)
out = open('out.txt', 'w')
out.write(f'{enc = }\n')
out.write(f'{modulus = }')
out.close()
