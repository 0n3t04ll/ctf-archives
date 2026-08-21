from Crypto.Util.number import getPrime, bytes_to_long
from random import randint

FLAG = b'plfanzen{**** i forgor (removed) the flag sorry ****}'
p = getPrime(1024)
q = getPrime(1024)

n = p * q
print(f'{n = }')
e = 65537
print(f'{e = }')
φ = (p - 1) * (q - 1)
assert φ % e != 0

d = pow(e, -1, φ)
f = (e * d - 1) * randint(1<<2047, 1<<2048)

# uhh,. ............... . .. now we publish this, r- right?
print(f'{f = }')


# * * * * * * * * 
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *
# *


# * wait.. what was i doing?
# ...
# ... better generate a new prime
r = getPrime(1024)

n = n * r
print(f'{n = }')
e = 65537
φ = (p - 1) * (q - 1) * (r - 1)
print(f'{e = }')
assert φ % e != 0

d = pow(e, -1,  φ)
x = bytes_to_long(FLAG)
y = pow(x, e, n)
print(f'{y = }')
