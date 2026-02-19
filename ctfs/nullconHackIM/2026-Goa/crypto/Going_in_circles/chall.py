from Crypto.Util import number
BITS = 32

def reduce(a,f):
	while (l := a.bit_length()) > BITS:
		a ^= f << (l - BITS)
	return a

flag = int.from_bytes(open('flag.txt','r').read().strip().encode(), byteorder = 'big')
f = number.getRandomNBitInteger(BITS)
print(reduce(flag,f),f)
