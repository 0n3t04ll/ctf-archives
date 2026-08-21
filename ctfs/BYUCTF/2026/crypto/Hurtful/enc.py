from Crypto.Util.number import bytes_to_long, getPrime
from flag import flag

ct = b"Congrats on making it all the way here. If you're looking at this challenge you obviously know a lot, just find the flag: " + flag
ct = bytes_to_long(ct)

e = 3
N = getPrime(1024) * getPrime(1024)

c = pow(ct, e, N)

print(f"N = {N}")
print(f"e = {e}")
print(f"c = {c}")