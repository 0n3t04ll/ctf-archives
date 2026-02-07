import numpy as np
import base64

alphabet = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='

MOD = len(alphabet)
n = 16

def gen_key(n = n):
	A = np.random.randint(0, MOD, size = (n,n))
	b = np.random.randint(0, MOD, size = n)
	return A,b

def pad(msg : bytes, n = n):
	padlen = n - (len(msg) % n)
	return msg + b'=' * padlen

def encrypt(msg : bytes, A, b):
	if type(msg) == str: msg = msg.encode()
	msg = base64.b64encode(msg)
	msg = pad(msg)
	cipher = np.zeros(len(msg), dtype = np.int_)
	block = np.zeros(n, dtype = np.int_)
	for i in range(0,len(msg), n):
		for j in range(n): block[j] = alphabet.index(msg[i+j])
		cipher[i:i+n] = A @ block + b
	return cipher % MOD

if __name__ == '__main__':
	A,b = gen_key()
	msg = open('flag.txt','r').read().strip()
	cipher = encrypt(msg, A, b).tolist()
	print(cipher)
	while True:
		msg = input('enter your message (in hex): ').strip()
		if msg == 'exit': break
		msg = bytes.fromhex(msg)
		print(encrypt(msg, A, b).tolist())
